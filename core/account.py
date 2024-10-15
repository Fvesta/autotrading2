from datetime import datetime
import math

from core.autotrading.trading import Trading
from core.constants import TRADING_TAX
from core.global_state import UseGlobal
from core.logger import logger
from core.api import API
from core.errors import ErrorCode, StockNotFoundException
from core.utils.type_util import absIntOrZero
from core.utils.utils import isStock, intOrZero, getRegStock
from core.real_processing import real_manager

class holdingInfo:
    def __init__(self, stockcode, quantity, possible_quantity, average_buyprice):
        
        if not self.__validate(stockcode, quantity, possible_quantity, average_buyprice):
            raise StockNotFoundException
        
        self.api = API()
        
    def __validate(self, *args):
        stockcode, quantity, possible_quantity, average_buyprice = args
        
        if not isStock(stockcode):
            return False
        
        self.stockcode = getRegStock(stockcode)
        self.quantity = intOrZero(quantity)
        self.possible_quantity = intOrZero(possible_quantity)
        self.average_buyprice = intOrZero(average_buyprice)
        
        return True
        
    def getBuyAmount(self):
        return self.quantity * self.average_buyprice
    
    def getCurAmount(self):
        stockobj = self.api.getStockObj(self.stockcode)
        
        quantity = self.quantity
        cur_price = stockobj.cur_price
        
        return quantity * cur_price - absIntOrZero(self.average_buyprice * quantity * (TRADING_TAX / 100))
    
    def getIncomeRate(self):
        cur_amount = self.getCurAmount()
        buy_amount = self.getBuyAmount()
        
        try:
            income_rate = (cur_amount - buy_amount) / buy_amount * 100
        except ZeroDivisionError:
            logger.warning("Buy amount is zero")
            return None
        
        return income_rate
        

class Account(UseGlobal):
    accountCnt = 0
    
    def __init__(self, accno):
        UseGlobal.__init__(self)
        Account.accountCnt += 1
        
        self.api = API()
        self.accno = accno
        
        self.total_amount = 0   # 예탁자금
        self.rest_amount = 0    # 매수가능금액
        self.d2_depos_amount = 0  # D+2 추정예수금
        self.today_income = 0   # 당일실현손익
        self.today_buy_stocks = set() # 당일 매수종목
        
        # Order info
        self.holdings = {}
        self.not_completed_order = {}
        
        self.real_exec_log = []
        
        # Auto trading
        self.trading = Trading(self)
        
        # Set rest_amount, d2_depos_amount
        self.getRestAmount()
        
        # Get acc balance info
        self.reqAccInfo(init=True)
        
        # Get not completed order
        self.getNCLog()
        
        # Get today income
        self.getTodayIncome()
        
        # Test Tr
        
    
    # data = {"total_amount": "00", "rest_amount": "00", "d2_depos_amount": "00", "today_income": "00"}    
    def setAccInfo(self, data):
        
        total_amount = data.get("total_amount")
        if total_amount is not None:
            self.total_amount = intOrZero(total_amount)
            
        rest_amount = data.get("rest_amount")
        if rest_amount is not None:
            self.rest_amount = intOrZero(rest_amount)
            
        d2_depos_amount = data.get("d2_depos_amount")
        if d2_depos_amount is not None:
            self.d2_depos_amount = intOrZero(d2_depos_amount)
            
        today_income = data.get("today_income")
        if today_income is not None:
            self.today_income = intOrZero(today_income)
    
    # Add not completed order
    def addNCOrder(self, op_time, orderno, stockcode, order_op, order_quantity, rest_quantity, order_price):
        today = datetime.now()
        time_tmp = datetime.strptime(op_time, "%H%M%S")
        order_time = today.replace(hour=time_tmp.hour, minute=time_tmp.minute, second=time_tmp.second)
        
        order_gubun = ""
        if order_op == "1":
            order_gubun = "매도"
        elif order_op == "2":
            order_gubun = "매수"
        
        self.not_completed_order[orderno] = {
            "stockcode": stockcode,
            "order_gubun": order_gubun,                # 매도수구분
            "order_quantity": order_quantity,          # 주문수량
            "rest_quantity": rest_quantity,           # 미체결수량
            "order_price": order_price,                # 주문가격
            "order_time": order_time,                  # 주문시간
        }

    def addExecLog(self, op_time, orderno, stockcode, exec_op, exec_price, exec_quantity, exec_fee, exec_tax):
        today = datetime.now()
        time_tmp = datetime.strptime(op_time, "%H%M%S")
        exec_time = today.replace(hour=time_tmp.hour, minute=time_tmp.minute, second=time_tmp.second)
        
        exec_gubun = ""
        if exec_op == "1":
            exec_gubun = "매도"
        elif exec_op == "2":
            exec_gubun = "매수"

        self.real_exec_log.append({
            "stockcode": stockcode,                     # 종목코드
            "exec_orderno": orderno,                    # 주문번호
            "exec_gubun": exec_gubun,                   # 매도수구분
            "exec_amount": exec_quantity * exec_price,  # 체결금액
            "exec_quantity": exec_quantity,             # 체결수량
            "exec_price": exec_price,                   # 체결가격
            "exec_fee": exec_fee,                       # 수수료
            "exec_tax": exec_tax,                       # 세금
            "exec_time": exec_time,                     # 체결시간
        })
        
    def calculateBalLog(self):
        balance_log = {}
        
        today_merged_log = {}
        
        for log in self.real_exec_log:
            stockcode = log["stockcode"]
            
            try:
                stockcode = getRegStock(stockcode)
            except:
                logger.debug("There is not stockcode")
                continue
            
            # Init stock
            if stockcode not in today_merged_log:
                today_merged_log[stockcode] = {
                    "today_buy_quantity": 0,
                    "today_buy_amount": 0,
                    "today_sell_quantity": 0,
                    "today_sell_amount": 0,
                    "buy_origin_amount": 0,
                    "today_fee_log_dict": {},
                    "today_tax_log_dict": {},
                } 
            
            exec_orderno = log["exec_orderno"]
            exec_gubun = log["exec_gubun"]
            exec_amount = log["exec_amount"]
            exec_quantity = log["exec_quantity"]
            exec_fee = log["exec_fee"]
            exec_tax = log["exec_tax"]
            average_buyprice = log["average_buyprice"]
            
            # Calculate quantity
            if exec_gubun == "매수":
                today_merged_log[stockcode]["today_buy_quantity"] += exec_quantity
                today_merged_log[stockcode]["today_buy_amount"] += exec_amount
            elif exec_gubun == "매도":
                today_merged_log[stockcode]["today_sell_quantity"] += exec_quantity
                today_merged_log[stockcode]["today_sell_amount"] += exec_amount
                today_merged_log[stockcode]["buy_origin_amount"] += average_buyprice * exec_quantity
                
            # Calculate tax, fee
            today_merged_log[stockcode]["today_fee_log_dict"][exec_orderno] = exec_fee
            today_merged_log[stockcode]["today_tax_log_dict"][exec_orderno] = exec_tax
            
        for stockcode in today_merged_log.keys():
            merged_log = today_merged_log[stockcode]
            
            # Buy info
            today_buy_quantity = merged_log["today_buy_quantity"]
            today_buy_amount = merged_log["today_buy_amount"]
            try:    
                today_average_buy_price = math.floor(today_buy_amount / today_buy_quantity)
            except ZeroDivisionError:
                today_average_buy_price = 0

            # Sell info
            today_sell_quantity = merged_log["today_sell_quantity"]
            today_sell_amount = merged_log["today_sell_amount"]
            try:    
                today_average_sell_price = math.floor(today_sell_amount / today_sell_quantity)
            except ZeroDivisionError:
                today_average_sell_price = 0
                
            # Calculate fee, tax
            today_total_fee = 0
            for each_fee in merged_log["today_fee_log_dict"].values():
                today_total_fee += each_fee
                
            today_total_tax = 0
            for each_tax in merged_log["today_tax_log_dict"].values():
                today_total_tax += each_tax
            
            today_total_tax_fee = today_total_tax + today_total_fee
            
            # Calculate income rate
            buy_origin_amount = merged_log["buy_origin_amount"]
            today_income = today_sell_amount - buy_origin_amount - today_total_tax_fee
            try:
                today_income_rate = (today_income / buy_origin_amount) * 100
            except ZeroDivisionError:
                today_income_rate = 0
                
            balance_log[stockcode] = {
                "today_average_buy_price": today_average_buy_price,     # 매수평균가
                "today_buy_quantity": today_buy_quantity,               # 매수수량
                "today_buy_amount": today_buy_amount,                   # 매수금액
                "today_average_sell_price": today_average_sell_price,   # 매도평균가
                "today_sell_quantity": today_sell_quantity,             # 매도수량
                "today_sell_amount": today_sell_amount,                 # 매도금액
                "buy_origin_amount": buy_origin_amount,                 # 매입평가금
                "today_total_tax_fee": today_total_tax_fee,             # 세금, 수수료
                "today_income": today_income,                           # 실현손익
                "today_income_rate": today_income_rate                  # 손익율
            }
        
        return balance_log
    
    def getRestAmount(self):
        deposit_info = self.api.sendTr("예수금상세현황요청", [self.accno, "", None, None])
        
        single_data = deposit_info.get("single")
        
        rest_amount = single_data.get("주문가능금액")
        d2_depos_amount = single_data.get("d+2추정예수금")
        
        self.setAccInfo({
            "rest_amount": rest_amount,
            "d2_depos_amount": d2_depos_amount
        })
        
        self.gstate.callUpdate(key=f"{self.accno}$rest")
    
    def reqAccInfo(self, init=False):
        
        if init:
            
            acc_bal_info = self.api.sendTr("계좌평가현황요청", [self.accno, "", None, None])
        
            if isinstance(acc_bal_info, ErrorCode):
                logger.warning("Can\'t load account balance info")
                return
                
            multi_data = acc_bal_info.get("multi")
            
            # Set holdings data
            holdings = {}
            for row_data in multi_data:
                stockcode = row_data.get("종목코드")
                try:
                    stockcode = getRegStock(stockcode)
                except:
                    logger.debug("There is not stockcode")
                
                quantity = row_data.get("보유수량")
                average_buyprice = row_data.get("평균단가")
                
                try:
                    holding_info = holdingInfo(stockcode, quantity, quantity, average_buyprice)
                except StockNotFoundException as e:
                    logger.error(e)
                    continue
                
                holdings[stockcode] = holding_info
                
            self.holdings = holdings
        
        stocks_info = self.api.sendTrMany("관심종목정보요청", list(self.holdings.keys()))
        
        if isinstance(stocks_info, ErrorCode):
            logger.warning("Can\'t load each holdings info")
            return
        
        multi_data = stocks_info.get("multi")
        for row_data in multi_data:
            stockcode = row_data.get("종목코드")
            
            if stockcode == '':
                continue
            
            cur_price = row_data.get("현재가")
            today_updown_rate = row_data.get("등락율")
            today_trans_count = row_data.get("거래량")
            buy_sell_strength = row_data.get("체결강도")
            
            stockobj = self.api.getStockObj(stockcode)
            stockobj.setStockInfo({
                "cur_price": cur_price,
                "today_updown_rate": today_updown_rate,
                "today_trans_count": today_trans_count,
                "buy_sell_strength": buy_sell_strength,
            })
            
        # Calculate total_amount
        total_eval_amount = self.getTotalEvalAmount()
        total_amount = self.d2_depos_amount + total_eval_amount
        self.total_amount = total_amount
        
        # Announce changed to all objects
        self.gstate.callUpdate(key=f"{self.accno}$balance")

        # Register real event
        real_manager.regReal(f"{self.accno}$holdings", list(self.holdings.keys()), self.changeHoldings)
        
    def changeHoldings(self, seed, stockcode, real_type, real_data):
        if real_type == "주식체결":
            stockcode = getRegStock(stockcode)
            if self.isHoldings(stockcode):
                total_eval_amount = self.getTotalEvalAmount()
                
                total_amount = self.rest_amount + total_eval_amount
                self.total_amount = total_amount
                
                self.gstate.callUpdate(key=seed)
                
    def getTodayIncome(self):
        # Set Today income
        today_trade_log = self.api.sendTr("당일매매일지요청", [self.accno, "", "", None, None])
        
        single_data = today_trade_log.get("single")
        multi_data = today_trade_log.get("multi")
        
        today_income = single_data.get("총손익금액")
        
        self.setAccInfo({
            "today_income": today_income,
        })
        
        for data in multi_data:
            stockcode = data.get("종목코드")
            
            if stockcode == '':
                continue

            stockcode = getRegStock(stockcode)
            today_buy_quantity = data.get("매수수량")  
            if today_buy_quantity != "0":
                self.today_buy_stocks.add(stockcode)
        
    def getNCLog(self):
        nc_log = self.api.sendTr("미체결요청", [self.accno, None, None, None, None])
        
        multi_data = nc_log.get("multi")
        
        for data in multi_data:
            stockcode = data.get("종목코드")
            
            if stockcode == '':
                continue

            stockcode = getRegStock(stockcode)
            
            orderno = data.get("주문번호")
            order_gubun = data.get("주문구분")
            
            order_op = ""
            if order_gubun == "-매도" or order_gubun == "-매도정정":
                order_op = "1"
            elif order_gubun == "+매수" or order_gubun == "+매수정정":
                order_op = "2"
            
            order_quantity = intOrZero(data.get("주문수량"))
            order_price = intOrZero(data.get("주문가격"))
            rest_quantity = intOrZero(data.get("미체결수량"))
            order_time = data.get("시간")
            
            self.addNCOrder(order_time, orderno, stockcode, order_op, order_quantity, rest_quantity, order_price)
            
    def getTotalBuyAmount(self):
        
        total_buy_amount = 0
        for holding_info in self.holdings.values():
            total_buy_amount += holding_info.getBuyAmount()
            
        return total_buy_amount
    
    def getTotalEvalAmount(self):
        
        total_cur_amount = 0
        for holding_info in self.holdings.values():
            total_cur_amount += holding_info.getCurAmount()
        
        return total_cur_amount
    
    def getTotalIncomeAmount(self):
        total_buy_amount = self.getTotalBuyAmount()
        total_eval_amount = self.getTotalEvalAmount()
        
        return total_eval_amount - total_buy_amount
    
    def getTotalIncomeRate(self):
        total_buy_amount = self.getTotalBuyAmount()
        total_eval_amount = self.getTotalEvalAmount()
        
        try:
            income_rate = (total_eval_amount - total_buy_amount) / total_buy_amount * 100
        except ZeroDivisionError:
            logger.warning("Buy amount is zero")
            return None
        
        return income_rate
    
    def isHoldings(self, stockcode):
        if stockcode in self.holdings:
            return True
        
        return False
    
    ############################################
    # Test TR functions
    ############################################
