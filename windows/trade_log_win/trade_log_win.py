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
        
        income_log_table = self.ui.income_log_table
        exec_log_table = self.ui.exec_log_table
        
        setTableSizeSameHor(income_log_table)
        setTableSizeSameHor(exec_log_table)
        
    def updateStates(self, key="", extra={}):
        if key == f"{self.accno}$trade_log":
            order_status = extra.get("order_status")
            
            if order_status == "접수":
                self.setIncomeData()
                self.setNotCompletedData()
                
            if order_status == "체결":
                self.setIncomeData()
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
        
        self.setIncomeData()
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
    
    def setIncomeData(self):
        pass
    
    def setExecData(self):
        # 종목코드
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
            
            exec_gubun = log["exec_gubun"]
            exec_amount = log["exec_amount"]
            exec_quantity = log["exec_quantity"]
            exec_price = log["exec_price"]
            exec_time = log["exec_time"]
            
            tb_data.append((stockcode, stockobj.name, exec_gubun, exec_amount, exec_quantity, exec_price, exec_time))
        
        for i in range(len(tb_data)):
            for j in range(len(tb_data[0])):
                item = QTableWidgetItem(str(tb_data[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
        
                self.ui.exec_log_table.setItem(i, j, item)    

    def setNotCompletedData(self):
        # 주문번호
        # 종목코드
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
            
            tb_data.append((orderno, stockcode, stockobj.name, order_gubun, order_quantity, rest_quantity, order_price, order_time))
            
        for i in range(len(tb_data)):
            for j in range(len(tb_data[0])):
                item = QTableWidgetItem(str(tb_data[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
        
                self.ui.not_completed_table.setItem(i, j, item)
                
                