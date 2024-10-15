from PySide2.QtWidgets import *
from PySide2.QtCore import Signal, Qt

from core.account import Account
from core.api import API
from core.autotrading.basic_options import ALGO_SHORT_HIT_BASIC_OPTION, TRADING_BASIC_OPTION
from core.errors import ErrorCode
from core.logger import logger
from core.stock import Stock
from core.condition import Condition
from core.real_processing import real_manager
from core.condition import cond_manager
from core.utils.utils import getAccnoFromObj
from style.utils import setTableSizeSameHor, setTableSizeSameVer
from style.colors import decimal_colors
from windows.balance_win.balance_win import BalanceWin
from windows.main_win.acc_info import newAccInfo
from windows.trade_log_win.trade_log_win import TradeLogWin
from windows.trade_setting.trade_setting import TradeSettingWin
from windows.win_abs import WindowAbs, showModal

class MainWin(WindowAbs):
    update = Signal(str, dict)
    
    def __init__(self, name, ui_path, css_path):
        WindowAbs.__init__(self, name, ui_path, css_path)
        
        self.api = API()
        
        self.initSetting()
        
    def initSetting(self):
        self.ui.setWindowTitle("AutoTrading v2")
        self.ui.title.setProperty("class", "tx-title")
        
    def updateStates(self, key="", extra={}):
        self.user_id, self.setUserId = self.gstate.useState("user_id")
        self.user_name, self.setUserName = self.gstate.useState("user_name")
        self.is_login, self.setIsLogin = self.gstate.useState("is_login")
        self.account_dict, self.setAccountDict = self.gstate.useState("account_dict")
        
        for accno in self.account_dict.keys():
            if key == f"{accno}$holdings" or key == f"{accno}$balance" or key == f"{accno}$rest":
                self.updateBalTable(accno)
        
        if key == "main_win_accholdings":
            accno = extra.get("accno")
            self.updateBalTable(accno)
    
    def eventReg(self):
        self.update.connect(self.updateStates)
        
    def eventTerm(self):
        self.update.disconnect(self.updateStates)

    def afterSetting(self):
        accounts = self.account_dict.keys()
        
        for accno in accounts:
            # Set text feature
            tradeset_label = getattr(self.ui, f"_{accno}_tradeset_label")
            tradeset_label.setProperty("class", "tx-tradeset-label")
            
            # Set combo box
            combobox = getattr(self.ui, f"_{accno}_comboBox")
            combobox.addItems(cond_manager.cond_dict.keys())
            
            combobox.currentTextChanged.connect(self.comboChanged)
            
            # Set account balance
            self.updateBalTable(accno)

        # Add additional btn event
        self.setBtnEvents()
        
        self.updateStyle()
        
        for accno in accounts:
            balance_table = getattr(self.ui, f"_{accno}_balance_table")
            
            # Change selection mode
            balance_table.setSelectionMode(QAbstractItemView.NoSelection)
            
            # Resize table
            setTableSizeSameHor(balance_table)
            setTableSizeSameVer(balance_table)
    
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
        
        # Load condition
        self.getCondition()
        
        # Set title to username
        self.ui.title.setText(self.user_name)
        
        # Add account ui group
        accounts = self.account_dict.keys()
        for accno in accounts:
            newAccInfo(self.ui, accno)
        
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.ui.verticalLayout_3.addItem(verticalSpacer)
        
        # Register real data
        stockcode_set = set()
        for acc in self.account_dict.values():
            stockcode_set.update(list(acc.holdings.keys()))
        
        real_manager.regReal("main_win_accholdings", list(stockcode_set), self.realEventCallback)

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
        
    def getCondition(self):
        load_success = self.api.loadCondition()
        
        if load_success:
            cond_list = self.api.getConditionNameList()
            
            for cond in cond_list:
                cidx, condname = cond.split("^")
                cond_manager.cond_dict[condname] = Condition(cidx, condname)
        
    def updateBalTable(self, accno):
        acc: Account = self.account_dict[accno]
        
        if not hasattr(self.ui, f"_{accno}_balance_table"):
            return
        
        table: QTableWidget = getattr(self.ui, f"_{accno}_balance_table")
        item1_0 = table.item(1, 0)
        item1_1 = table.item(1, 1)
        item1_2 = table.item(1, 2)
        item3_0 = table.item(3, 0)
        item3_1 = table.item(3, 1)
        item3_2 = table.item(3, 2)
        
        item1_0.setText(f"{acc.total_amount:,}")
        item1_1.setText(f"{acc.rest_amount:,}")
        item1_2.setText(f"{acc.today_income:+,}")
        
        if acc.today_income >= 0:
            item1_2.setForeground(decimal_colors["QT_LIGHT_RED"])
        else:
            item1_2.setForeground(decimal_colors["QTMATERIAL_PRIMARYCOLOR"])
        
        item3_0.setText(f"{acc.getTotalEvalAmount():,}")
        item3_1.setText(f"{acc.getTotalIncomeAmount():+,}")
        item3_2.setText(f"{acc.getTotalIncomeRate():+.2f}%")
        
    def setBtnEvents(self):
        def changeMouseCursor(obj, shape):
            def wrapper(event):
                obj.setCursor(shape)
            
            return wrapper
        
        def svgResize(obj, size):
            def wrapper(event):
                obj.setFixedSize(size, size)
                
            return wrapper
        
        def settingBtnRelease(btn, accno):
            def wrapper(event):            
                win_name = f"_{accno}_trade_setting"
                
                if win_name in self.gstate.activated_windows:
                    return
                
                new_winobj = TradeSettingWin(win_name, "GUI/trade_setting.ui", "style/trade_setting.css")
                new_winobj.show()
            
            return wrapper

        def playBtnEnter(btn, accno):
            def wrapper(event):
                btn.setCursor(Qt.PointingHandCursor)
                acc = self.api.getAccObj(accno)
                
                if acc.trading.running:
                    btn.load("style/assets/stop_icon_hover.svg")
                else:
                    btn.load("style/assets/play_icon_hover.svg")
            
            return wrapper
                    
        def playBtnLeave(btn, accno):
            def wrapper(event):
                btn.setCursor(Qt.ArrowCursor)
                acc = self.api.getAccObj(accno)
                
                if acc.trading.running:
                    btn.load("style/assets/stop_icon.svg")
                else:
                    btn.load("style/assets/play_icon.svg")
        
            return wrapper
        
        def playBtnRelease(btn, accno):
            def wrapper(event):
                btn.setFixedSize(40, 40)
                
                acc = self.api.getAccObj(accno)
                
                if acc.trading.running:
                    acc.trading.stop()
                    btn.load("style/assets/play_icon_hover.svg")
                else:
                    acc.trading.start()
                    btn.load("style/assets/stop_icon_hover.svg")
                
            return wrapper

        def pushButtonClick(obj, accno):
            def wrapper():
                text = obj.text()
                
                if text == "잔고":
                    win_name = f"_{accno}_balance_win"
                    
                    if win_name in self.gstate.activated_windows:
                        return
                    
                    new_winobj = BalanceWin(win_name, "GUI/balance_win.ui", "style/balance_win.css")
                    new_winobj.show()
                
                if text == "거래내역":
                    win_name = f"_{accno}_trade_log_win"
                    
                    if win_name in self.gstate.activated_windows:
                        return
                    
                    new_winobj = TradeLogWin(win_name, "GUI/trade_log_win.ui", "style/trade_log_win.css")
                    new_winobj.show()
                    
            return wrapper
        
        accounts = self.account_dict.keys()
        for accno in accounts:
            # Setting button svg click event 
            setting_btn = getattr(self.ui, f"_{accno}_setting_btn")
            setting_btn.enterEvent = changeMouseCursor(setting_btn, Qt.PointingHandCursor)
            setting_btn.leaveEvent = changeMouseCursor(setting_btn, Qt.ArrowCursor)
            
            setting_btn.mouseReleaseEvent = settingBtnRelease(setting_btn, accno)
            
            # Play button events
            play_btn = getattr(self.ui, f"_{accno}_play_btn")
            play_btn.enterEvent = playBtnEnter(play_btn, accno)
            play_btn.leaveEvent = playBtnLeave(play_btn, accno)
            
            play_btn.mousePressEvent = svgResize(play_btn, 35)
            play_btn.mouseReleaseEvent = playBtnRelease(play_btn, accno)
            
            # Balance button event
            balance_btn = getattr(self.ui, f"_{accno}_balance_btn")
            balance_btn.clicked.connect(pushButtonClick(balance_btn, accno))
            
            # Trading log event
            trade_log_btn = getattr(self.ui, f"_{accno}_trade_log_btn")
            trade_log_btn.clicked.connect(pushButtonClick(trade_log_btn, accno))
            
    def comboChanged(self, text):
        obj_name = self.sender().objectName()
        accno = getAccnoFromObj(obj_name)
        
        if isinstance(accno, ErrorCode):
            return
        
        acc = self.api.getAccObj(accno)
        
        option = dict(TRADING_BASIC_OPTION)

        short_hit_base_option = dict(ALGO_SHORT_HIT_BASIC_OPTION)
        short_hit_base_option["condition"] = text
        
        option["base_algorithm"]["option"] = short_hit_base_option
        acc.trading.setOption(option)

    def realEventCallback(self, seed, stockcode, real_type, real_data):
        if real_type == "주식체결":
            for accno, acc in self.account_dict.items():
                if acc.isHoldings(stockcode):
                    self.update.emit(seed, {"accno": accno})
