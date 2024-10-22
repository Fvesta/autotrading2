from PySide2.QtCore import Signal, Qt
from PySide2.QtWidgets import *

from core.account import Account, holdingInfo
from core.api import API
from core.constants import MAX_TABLE_COL, MAX_TABLE_ROW
from core.errors import ErrorCode
from core.stock import Stock
from core.utils.stock_util import getRegStock
from core.utils.utils import getAccnoFromObj
from core.order_processing import order_manager
from core.real_processing import real_manager
from style.utils import setTableSizeSameHor
from windows.win_abs import WindowAbs, showModal
from style.colors import decimal_colors


class BalanceWin(WindowAbs):
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
        self.ui.splitter.setSizes([950, 450])
        self.ui.setWindowTitle(f"잔고: {self.accno}")
    
    def afterSetting(self):
        self.updateStyle()
        
        setTableSizeSameHor(self.ui.holding_table)
        setTableSizeSameHor(self.ui.not_completed_table)
        setTableSizeSameHor(self.ui.real_exec_table)
        
    def updateHoldings(self):
        self.setBalanceEval()
        self.setHoldingsData()
            
    def updateStates(self, key="", extra={}):
        if key == f"{self.accno}$balance":
            self.updateHoldings()
            
        if key == f"{self.accno}$holdings":
            # If last called time is n sec before
            if real_manager.notCalledInTime(f"{self.accno}$holdings", interval=0.3, post_callback=self.updateHoldings):
                self.updateHoldings()
            
        if key == f"{self.accno}$balance_win_order":
            tradetype = extra.get("tradetype")
            order_status = extra.get("order_status")
            
            # 주문체결
            if tradetype == "0":
                if order_status == "접수":
                    self.setBalanceEval()
                    self.setNotCompletedData()
                    
                if order_status == "체결":
                    self.setRealExecData()
                    self.setNotCompletedData()
            
            # 잔고
            if tradetype == "1":
                self.setBalanceEval()
                self.setHoldingsData()
            
                
    def eventReg(self):
        self.ui.splitter.splitterMoved.connect(self.resizeTable)
        self.update.connect(self.updateStates)
        order_manager.regOrderReal(f"{self.accno}$balance_win_order", self.orderCallback)
    
    def eventTerm(self):
        self.ui.splitter.splitterMoved.disconnect(self.resizeTable)
        self.update.disconnect(self.updateStates)
        order_manager.termOrderReal(f"{self.accno}$balance_win_order")
        
    def resizeTable(self):
        setTableSizeSameHor(self.ui.holding_table)
        setTableSizeSameHor(self.ui.not_completed_table)
        setTableSizeSameHor(self.ui.real_exec_table)
    
    @showModal
    def show(self):
        
        # Register States, add events
        self.stateReg()
        self.updateStates()
        self.eventReg()
        
        self.setBalanceEval()
        self.setHoldingsData()
        self.setNotCompletedData()
        self.setRealExecData()
    
    def setHoldingsData(self):
        acc: Account = self.api.getAccObj(self.accno)
        stock_list = list(acc.holdings.keys())
        
        tb_data = []
        for stockcode in stock_list:
            stockobj: Stock = self.api.getStockObj(stockcode)
            info: holdingInfo = acc.holdings[stockcode]
            
            stockname = stockobj.name
            quantity = info.quantity
            today_updown_rate = f"{stockobj.today_updown_rate:+.2f}%"
            cur_price = stockobj.cur_price
            
            cur_amount = info.getCurAmount()
            cur_amount_formatted = f"{cur_amount:,}"
            
            average_buy_price = info.average_buyprice
            
            income_rate = info.getIncomeRate()
            income_formatted = f"{income_rate:+.2f}%" 
            
            tb_data.append((stockcode, stockname, quantity, today_updown_rate, cur_price, cur_amount_formatted, average_buy_price, income_formatted))
        
        self.ui.holding_table.setRowCount(len(tb_data))
        for i in range(len(tb_data)):
            for j in range(len(tb_data[0])):
                
                # If field is income_rate
                if j == 7:
                    item = QTableWidgetItem(str(tb_data[i][j]))
                    item.setTextAlignment(Qt.AlignCenter)
                    
                    income_formatted = tb_data[i][j]
                    if income_formatted[0] == "+":
                        item.setForeground(decimal_colors["QT_LIGHT_RED"])
                    else:
                        item.setForeground(decimal_colors["QT_LIGHT_BLUE"])
                    
                    self.ui.holding_table.setItem(i, j, item)
                else:
                    item = QTableWidgetItem(str(tb_data[i][j]))
                    item.setTextAlignment(Qt.AlignCenter)
                    
                    self.ui.holding_table.setItem(i, j, item)

    def setBalanceEval(self):
        # 보유종목수    holding_cnt_label
        # 총매입금      total_buy_label
        # 총평가금      total_eval_label
        # 평가손익      income_label
        # 수익률        income_rate_label
        # 당일종목수    today_stock_label
        
        acc: Account = self.api.getAccObj(self.accno)
        
        holding_cnt = len(acc.holdings)
        total_buy_amount = acc.getTotalBuyAmount()
        total_eval_amount = acc.getTotalEvalAmount()
        income_amount = acc.getTotalIncomeAmount()
        income_rate = acc.getTotalIncomeRate()
        today_stock_cnt = len(acc.today_buy_stocks)
        
        self.ui.today_stock_label.setText(f"당일매수종목수:    {today_stock_cnt}")
        self.ui.holding_cnt_label.setText(f"당일보유종목수:    {holding_cnt}")
        self.ui.total_buy_label.setText(f"총매입금:    {total_buy_amount:,}")
        self.ui.total_eval_label.setText(f"총평가금:    {total_eval_amount:,}")
        
        self.ui.today_income_label.setText(f"실현손익:    ")
        self.ui.today_income_label_val.setText(f"{acc.today_income:+,}")
        if acc.today_income >= 0:
            self.ui.today_income_label_val.setProperty("class", "tx-light-red")
        else:
            self.ui.today_income_label_val.setProperty("class", 'tx-light-blue')
        
        self.ui.eval_income_label.setText(f"평가손익:    ")
        self.ui.eval_income_label_val.setText(f"{income_amount:+,} ({income_rate:+.2f}%)")
        if income_amount >= 0:
            self.ui.eval_income_label_val.setProperty("class", "tx-light-red")
        else:
            self.ui.eval_income_label_val.setProperty("class", 'tx-light-blue')
        
        self.updateStyle()
                    
    def setRealExecData(self):
        # 체결시간
        # 종목이름
        # 매도수구분
        # 체결수량
        # 체결가격
        acc: Account = self.api.getAccObj(self.accno)
        real_exec_log = list(acc.real_exec_log)
        real_exec_log.reverse()
        
        tb_data = []
        for log in real_exec_log:
            stockcode = log["stockcode"] 
            stockcode = getRegStock(stockcode)
            
            stockobj = self.api.getStockObj(stockcode)
            
            exec_time = log["exec_time"]
            exec_time_formatted = exec_time.strftime("%d/%H:%M:%S")
            
            exec_gubun = log["exec_gubun"]
            exec_quantity = log["exec_quantity"]
            exec_price = log["exec_price"]
            
            tb_data.append((exec_time_formatted, stockobj.name, exec_gubun, exec_quantity, exec_price))
        
        self.ui.real_exec_table.setRowCount(len(tb_data))
        for i in range(len(tb_data)):
            for j in range(len(tb_data[0])):
                
                if j == 2:
                    item = QTableWidgetItem(str(tb_data[i][j]))
                    item.setTextAlignment(Qt.AlignCenter)
                    
                    order_gubun = tb_data[i][j]
                    if order_gubun == "매수":
                        item.setForeground(decimal_colors["QT_LIGHT_RED"])
                    elif order_gubun == "매도":
                        item.setForeground(decimal_colors["QT_LIGHT_BLUE"])
                    
                    self.ui.real_exec_table.setItem(i, j, item)
                else:
                    item = QTableWidgetItem(str(tb_data[i][j]))
                    item.setTextAlignment(Qt.AlignCenter)
            
                    self.ui.real_exec_table.setItem(i, j, item)
                    
    def setNotCompletedData(self):
        # 주문번호
        # 종목이름
        # 매도수구분
        # 주문수량
        # 미체결수량
        # 주문가격
        # 주문시간
        acc: Account = self.api.getAccObj(self.accno)
        not_completed_orderno_list = list(acc.not_completed_order.keys())
        
        tb_data = []
        for orderno in not_completed_orderno_list:
            order_info = acc.not_completed_order[orderno]
            
            stockcode = order_info["stockcode"]
            stockcode = getRegStock(stockcode)
            
            stockobj = self.api.getStockObj(stockcode)
            
            order_gubun = order_info["order_gubun"]
            order_quantity = order_info["order_quantity"]
            rest_quantity = order_info["rest_quantity"]
            order_price = order_info["order_price"]
            
            order_time = order_info["order_time"]
            order_time_formatted = order_time.strftime("%d/%H:%M:%S")
            
            tb_data.append((orderno, stockobj.name, order_gubun, order_quantity, rest_quantity, order_price, order_time_formatted))
        
        self.ui.not_completed_table.setRowCount(len(tb_data))
        for i in range(len(tb_data)):
            for j in range(len(tb_data[0])):
                item = QTableWidgetItem(str(tb_data[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
        
                self.ui.not_completed_table.setItem(i, j, item)
            
    def orderCallback(self, seed, tradetype, order_data):
        accno = order_data.get("계좌번호")
        if accno != self.accno:
            return
        
        # 주문체결
        if tradetype == "0":     
            order_status = order_data.get("주문상태")
            
            self.update.emit(seed, {
                "tradetype": tradetype,
                "order_status": order_status
            })
            
        if tradetype == "1":
            self.update.emit(seed, {
                "tradetype": tradetype
            })
            