from PySide2.QtWidgets import *
from PySide2.QtCore import QTimer, Signal, QObject

from core.account import Account
from core.api import API
from core.errors import ErrorCode
from core.global_state import UseGlobal
from core.logger import logger
from core.stock import Stock
from style.utils import setTableSizeSameHor, setTableSizeSameVer
from windows.main_win.acc_info import newAccInfo
from windows.trade_setting.trade_setting import TradeSettingWin
from windows.win_abs import WindowAbs, showModal

class MainWin(WindowAbs, UseGlobal, QObject):
    update = Signal(str, dict)
    
    def __init__(self, name, ui_path, css_path):
        QObject.__init__(self)
        WindowAbs.__init__(self, name, ui_path, css_path)
        UseGlobal.__init__(self)
        
        self.api = API()
        
        self.initSetting()
        
    def initSetting(self):
        self.ui.setWindowTitle("AutoTrading v2")
        self.ui.title.setProperty("class", "tx-title")
        
    def updateStates(self, key='', extra={}):
        self.user_id, self.setUserId = self.gstate.useState("user_id")
        self.user_name, self.setUserName = self.gstate.useState("user_name")
        self.is_login, self.setIsLogin = self.gstate.useState("is_login")
        self.account_dict, self.setAccountDict = self.gstate.useState("account_dict")
    
    def eventReg(self):
        self.update.connect(self.updateStates)

    def afterSetting(self):
        self.updateStyle()
        
        accounts = self.account_dict.keys()
        
        for accno in accounts:
            balanceTable = getattr(self.ui, f"_{accno}_balanceTable")
            setTableSizeSameHor(balanceTable)
            setTableSizeSameVer(balanceTable)
    
    @showModal
    def show(self):
        
        # Register States, add events
        self.stateReg()
        self.updateStates()
        self.eventReg()
        
        # Login
        if isinstance(self.login(), ErrorCode):
            self.ui.show()
            return
        
        # Get market stocks list
        self.getMarketStocks()

        # Account setting
        self.getAccountInfo()
        
        # Set title to username
        self.ui.title.setText(self.user_name)
        
        # Add account ui group
        accounts = self.account_dict.keys()
        for accno in accounts:
            newAccInfo(self.ui, accno)
        
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.ui.verticalLayout_3.addItem(verticalSpacer)
        
        # Add additional btn event
        self.setBtnEvents()
        
        # Get account balance
        for accno, acc in self.account_dict.items():
            acc.reqAccInfo()
            self.updateBalTable(accno)

    def login(self):
        login_success = self.api.login()
        
        if isinstance(login_success, ErrorCode):
            self.setIsLogin(False)
            logger.error("로그인에 실패했습니다")
            return ErrorCode.OP_ERROR
        
        self.setIsLogin(True)
        logger.debug("로그인에 성공했습니다")
        return 0
    
    def getMarketStocks(self):
        kospi_list = self.api.getCodeListByMarket('kospi')
        kosdaq_list = self.api.getCodeListByMarket('kosdaq')
        
        for stockcode in kospi_list:
            stockname = self.api.getStockName(stockcode)
            self.gstate.kospi_stocks[stockcode] = Stock(stockcode, stockname)
            
        for stockcode in kosdaq_list:
            stockname = self.api.getStockName(stockcode)
            self.gstate.kosdaq_stocks[stockcode] = Stock(stockcode, stockname)
            
    def getAccountInfo(self):
        acc_list, user_id, user_name = self.api.getLoginInfo()
        
        account_dict = {}
        for acc_no in acc_list:
            account_dict[acc_no] = Account(acc_no) 
            
        self.setUserName(user_name)
        self.setUserId(user_id)
        self.setAccountDict(account_dict)
        
    def updateBalTable(self, accno):
        acc: Account = self.account_dict[accno]
        
        table: QTableWidget = getattr(self.ui, f"_{accno}_balanceTable")
        item1_0 = table.item(1, 0)
        item1_1 = table.item(1, 1)
        item1_2 = table.item(1, 2)
        item3_0 = table.item(3, 0)
        item3_1 = table.item(3, 1)
        item3_2 = table.item(3, 2)
        
        item1_0.setText(str(acc.total_amount))
        item1_1.setText(str(acc.month_income))
        item1_2.setText(str(acc.today_income))
        
        item3_0.setText(str(acc.getTotalBuyAmount()))
        item3_1.setText(str(acc.getTotalCurAmount()))
        item3_2.setText(str(acc.getTotalIncomeRate()))
        
    def setBtnEvents(self):
        accounts = self.account_dict.keys()
        for accno in accounts:
            setting_btn = getattr(self.ui, f"_{accno}_pushButton")
            setting_btn.clicked.connect(self.newWindow)

    def newWindow(self):
        eventObj: QPushButton = self.sender()
        
        name = eventObj.objectName()
        accno = name.split("_")[1]
        
        text = eventObj.text()
        
        if text == "매매설정":
            win_name = f"_{accno}_trade_setting"
            
            if win_name in self.gstate.activated_windows:
                return
            
            new_winobj = TradeSettingWin(win_name, "GUI/trade_setting.ui", "style/trade_setting.css")
            new_winobj.show()
