from PySide2.QtCore import Signal, Qt
from PySide2.QtWidgets import *

from core import logger
from core.account import Account
from core.utils.stock_util import getRegStock
from core.utils.utils import getAccnoFromObj
from core.errors import ErrorCode
from core.api import API
from core.order_processing import order_manager
from style.utils import setTableSizeSameHor
from windows.win_abs import WindowAbs, showModal

class TradeLogWin(WindowAbs):
    update = Signal(str, dict)
    
    def __init__(self, name, ui_path, css_path):
        WindowAbs.__init__(self, name, ui_path, css_path)
        accno = getAccnoFromObj(name)
        
        if isinstance(accno, ErrorCode):
            return
        
        self.accno = accno
        self.api = API()
        
        self.initSetting()
        
    def initSetting(self):
        self.ui.setWindowTitle(f"거래내역: {self.accno}")
        
    def afterSetting(self):
        self.updateStyle()
        
        balance_log_table = self.ui.balance_log_table
        exec_log_table = self.ui.exec_log_table
        
        setTableSizeSameHor(balance_log_table)
        setTableSizeSameHor(exec_log_table)
        
    def updateStates(self, key="", extra={}):
        if key == f"{self.accno}$trade_log":
            order_status = extra.get("order_status")
            
            if order_status == "접수":
                self.setNotCompletedData()
                
            if order_status == "체결":
                self.setBalanceLogData()
                self.setExecData()
                self.setNotCompletedData()
    
    def eventReg(self):
        self.update.connect(self.updateStates)
        order_manager.regOrderReal(f"{self.accno}$trade_log", self.orderCallback)
        
    def eventTerm(self):
        self.update.disconnect(self.updateStates)
        order_manager.termOrderReal(f"{self.accno}$trade_log")
        
    @showModal
    def show(self):
        
        self.stateReg()
        self.updateStates()
        self.eventReg()
        
        self.setBalanceLogData()
        self.setExecData()
        self.setNotCompletedData()
        
    def orderCallback(self, seed, tradetype, order_data):
        accno = order_data.get("계좌번호")
        if accno != self.accno:
            return
        
        if tradetype == "0":     
            order_status = order_data.get("주문상태")
            
            self.update.emit(seed, {
                "order_status": order_status
            })
    
    def setBalanceLogData(self):
        # 종목이름
        # 매수평균가
        # 매수수량
        # 매수금액
        # 매도평균가
        # 매도수량
        # 매도금액
        # 매수평가금
        # 세금, 수수료
        # 실현손익
        # 손익율
        acc: Account = self.api.getAccObj(self.accno)
        balance_log = acc.calculateBalLog()
        bal_stockcode_list = list(balance_log.keys())
        
        tb_data = []
        self.ui.balance_log_table.setRowCount(len(bal_stockcode_list))
        for stockcode in bal_stockcode_list:
            
            try:
                stockcode = getRegStock(stockcode)
            except:
                logger.debug("There is not stockcode")
                continue
            
            stockobj = self.api.getStockObj(stockcode)
            
            balance_log_info = balance_log[stockcode]
            
            today_average_buy_price = balance_log_info["today_average_buy_price"]
            today_buy_quantity = balance_log_info["today_buy_quantity"]
            today_buy_amount = balance_log_info["today_buy_amount"]
            today_average_sell_price = balance_log_info["today_average_sell_price"]
            today_sell_quantity = balance_log_info["today_sell_quantity"]
            today_sell_amount = balance_log_info["today_sell_amount"]
            today_total_tax_fee = balance_log_info["today_total_tax_fee"]
            buy_origin_amount = balance_log_info["buy_origin_amount"]
            today_income = balance_log_info["today_income"]
            today_income_rate = balance_log_info["today_income_rate"]
            
            tb_data.append((
                stockobj.name,
                today_average_buy_price,
                today_buy_quantity,
                today_buy_amount,
                today_average_sell_price,
                today_sell_quantity,
                today_sell_amount,
                buy_origin_amount,
                today_total_tax_fee,
                today_income,
                today_income_rate
            ))
        
        for i in range(len(tb_data)):
            for j in range(len(tb_data[0])):
                item = QTableWidgetItem(str(tb_data[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
        
                self.ui.balance_log_table.setItem(i, j, item)
            
    def setExecData(self):
        # 주문번호
        # 종목이름
        # 매도수구분
        # 체결금액
        # 체결수량
        # 체결가격
        # 체결시간
        acc: Account = self.api.getAccObj(self.accno)
        exec_log = list(acc.exec_log)
        
        tb_data = []
        self.ui.exec_log_table.setRowCount(len(exec_log))
        for log in exec_log:
            stockcode = log["stockcode"]
            
            try:
                stockcode = getRegStock(stockcode)
            except:
                logger.debug("There is not stockcode")
                continue
            
            stockobj = self.api.getStockObj(stockcode)
            
            exec_orderno = log["exec_orderno"]
            exec_gubun = log["exec_gubun"]
            exec_amount = log["exec_amount"]
            exec_quantity = log["exec_quantity"]
            exec_price = log["exec_price"]
            exec_time = log["exec_time"]
            
            tb_data.append((exec_orderno, stockobj.name, exec_gubun, exec_amount, exec_quantity, exec_price, exec_time))
        
        for i in range(len(tb_data)):
            for j in range(len(tb_data[0])):
                item = QTableWidgetItem(str(tb_data[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
        
                self.ui.exec_log_table.setItem(i, j, item)    

    def setNotCompletedData(self):
        # 주문번호
        # 종목이름
        # 매도수구분
        # 주문수량
        # 미체결수량
        # 주문시간
        # 주문가격
        acc: Account = self.api.getAccObj(self.accno)
        not_completed_orderno_list = list(acc.not_completed_order.keys())
        
        tb_data = []
        self.ui.not_completed_table.setRowCount(len(not_completed_orderno_list))
        for orderno in not_completed_orderno_list:
            order_info = acc.not_completed_order[orderno]
            
            stockcode = order_info["stockcode"]
            
            try:
                stockcode = getRegStock(stockcode)
            except:
                logger.debug("There is not stockcode")
                continue
            
            stockobj = self.api.getStockObj(stockcode)
            
            order_gubun = order_info["order_gubun"]
            order_quantity = order_info["order_quantity"]
            rest_quantity = order_info["rest_quantity"]
            order_price = order_info["order_price"]
            order_time = order_info["order_time"]
            
            tb_data.append((orderno, stockobj.name, order_gubun, order_quantity, rest_quantity, order_price, order_time))
            
        for i in range(len(tb_data)):
            for j in range(len(tb_data[0])):
                item = QTableWidgetItem(str(tb_data[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
        
                self.ui.not_completed_table.setItem(i, j, item)
                
                