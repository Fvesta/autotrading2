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
    def __init__(self, stockcode, quantity, average_buyprice):
        
        if not self.__validate(stockcode, quantity, average_buyprice):
            raise StockNotFoundException
        
        self.api = API()
        
    def __validate(self, *args):
        stockcode, quantity, average_buyprice = args
        
        if not isStock(stockcode):
            return False
        
        self.stockcode = getRegStock(stockcode)
        self.quantity = intOrZero(quantity)
        self.average_buyprice = intOrZero(average_buyprice)
        
        return True
        
    def getBuyAmount(self):
        return self.quantity * self.average_buyprice
    
    def getCurAmount(self):
        stockobj = self.api.getStockObj(self.stockcode)
        
        quantity = self.quantity
        cur_price = stockobj.cur_price
        
        return absIntOrZero(quantity * cur_price * (1 - TRADING_TAX / 100))
    
    def getIncomeRate(self):
        cur_amount = self.getCurAmount()
        buy_amount = self.getBuyAmount()
        
        try:
            income_rate = (cur_amount - buy_amount) / buy_amount * 100
        except ZeroDivisionError:
            logger.warning("Buy amount is zero")
            return None
        
        return round(income_rate, 2)
        

class Account(UseGlobal):
    accountCnt = 0
    
    def __init__(self, accno):
        UseGlobal.__init__(self)
        Account.accountCnt += 1
        
        self.api = API()
        self.accno = accno
        
        self.total_amount = 0
        self.rest_amount = 0
        self.month_income = 0
        self.today_income = 0
        
        self.holdings = {}
        
        # Auto trading
        self.trading = Trading(self)
        
        # Get acc info
        self.reqAccInfo()
    
    # data = {"total_amount": "00", "rest_amount": "00", "month_income": "00", "today_income": "00"}    
    def setAccInfo(self, data):
        
        total_amount = data.get("total_amount")
        if total_amount is not None:
            self.total_amount = intOrZero(total_amount)
            
        rest_amount = data.get("rest_amount")
        if rest_amount is not None:
            self.rest_amount = intOrZero(rest_amount)
        
        month_income = data.get("month_income")
        if month_income is not None:
            self.month_income = intOrZero(month_income)
            
        today_income = data.get("today_income")
        if today_income is not None:
            self.today_income = intOrZero(today_income)
        
    def reqAccInfo(self):
        acc_bal_info = self.api.sendTr("계좌평가현황요청", [self.accno, "", None, None])
        
        if isinstance(acc_bal_info, ErrorCode):
            logger.warning("Can\'t load account balance info")
            return
            
        single_data = acc_bal_info.get("single")
        multi_data = acc_bal_info.get("multi")
        
        total_amount = single_data.get("추정예탁자산")
        rest_amount = single_data.get("D+2추정예수금")
        month_income = single_data.get("당월투자손익")
        today_income = single_data.get("당일투자손익")
        
        self.setAccInfo({
            "total_amount": total_amount,
            "rest_amount": rest_amount,
            "month_income": month_income,
            "today_income": today_income
        })
        
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
                holding_info = holdingInfo(stockcode, quantity, average_buyprice)
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

        # Register real event
        real_manager.regReal(f"{self.accno}$holdings", list(self.holdings.keys()), self.changeHoldings)
        
    def changeHoldings(self, seed, stockcode, real_type, real_data):
        if real_type == "주식체결":
            stockcode = getRegStock(stockcode)
            if self.isHoldings(stockcode):
                total_cur_amount = self.getTotalCurAmount()
                
                total_amount = self.rest_amount + total_cur_amount
                self.total_amount = total_amount
                
                self.gstate.callUpdate(key=seed)
                
            
    def getTotalBuyAmount(self):
        
        total_buy_amount = 0
        for holding_info in self.holdings.values():
            total_buy_amount += holding_info.getBuyAmount()
            
        return total_buy_amount
    
    def getTotalCurAmount(self):
        
        total_cur_amount = 0
        for holding_info in self.holdings.values():
            total_cur_amount += holding_info.getCurAmount()
        
        return total_cur_amount
    
    def getTotalIncomeRate(self):
        total_buy_amount = self.getTotalBuyAmount()
        total_cur_amount = self.getTotalCurAmount()
        
        try:
            income_rate = (total_cur_amount - total_buy_amount) / total_buy_amount * 100
        except ZeroDivisionError:
            logger.warning("Buy amount is zero")
            return None
        
        return round(income_rate, 2)
    
    def isHoldings(self, stockcode):
        if stockcode in self.holdings:
            return True
        
        return False
        
        