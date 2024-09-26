from PySide2.QtCore import Signal, Qt
from PySide2.QtWidgets import QTableWidgetItem

from core.account import Account, holdingInfo
from core.api import API
from core.errors import ErrorCode
from core.stock import Stock
from core.utils.utils import getAccnoFromObj
from style.utils import setTableSizeSameHor, setTableSizeSameVer
from windows.win_abs import WindowAbs, showModal


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
        self.ui.setWindowTitle(f"잔고: {self.accno}")
    
    def afterSetting(self):
        self.updateStyle()
        
        holding_table = self.ui.holding_table
        setTableSizeSameHor(holding_table)
        
    def updateStates(self, key='', extra={}):
        if key == f"{self.accno}$holdings":
            self.setHoldingsData()
                
    
    def eventReg(self):
        self.update.connect(self.updateStates)
    
    @showModal
    def show(self):
        
        # Register States, add events
        self.stateReg()
        self.updateStates()
        self.eventReg()
        
        self.setHoldingsData()
    
    def setHoldingsData(self):
        acc: Account = self.api.getAccObj(self.accno)
        stock_list = list(acc.holdings.keys())
        
        tb_data = []
        self.ui.holding_table.setRowCount(len(stock_list))
        for stockcode in stock_list:
            stockobj: Stock = self.api.getStockObj(stockcode)
            info: holdingInfo = acc.holdings[stockcode]
            
            stockname = stockobj.name
            quantity = info.quantity
            today_updown_rate = stockobj.today_updown_rate
            cur_price = stockobj.cur_price
            cur_amount = info.getCurAmount()
            average_buy_price = info.average_buyprice
            income_rate = info.getIncomeRate()
            
            income_formatted = ""
            if income_rate >= 0:
                income_formatted = f"+{income_rate}%"
            else:
                income_formatted = f"{income_rate}%"
            
            tb_data.append((stockcode, stockname, quantity, today_updown_rate, cur_price, cur_amount, average_buy_price, income_formatted))
        
        for i in range(len(tb_data)):
            for j in range(len(tb_data[0])):
                item = QTableWidgetItem(str(tb_data[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.holding_table.setItem(i, j, item)            
            