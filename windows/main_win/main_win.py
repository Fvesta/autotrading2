from PySide2.QtWidgets import *
from PySide2.QtCore import QTimer, Signal, QObject

from core.account import Account
from core.api import API
from core.callback_handler import CallbackHandler
from core.errors import LoginFailedException
from core.global_state import UseGlobal
from core.logger import logger
from style.utils import setTableSizeSameHor, setTableSizeSameVer
from windows.main_win.acc_info import newAccInfo
from windows.win_abs import WindowAbs

class MainWin(WindowAbs, UseGlobal, QObject):
    update = Signal(str, dict)
    
    def __init__(self, name, ui_path, css_path):
        QObject.__init__(self)
        WindowAbs.__init__(self, name, ui_path, css_path)
        UseGlobal.__init__(self)
        
        self.api = API()
        
        self.callback_handler = CallbackHandler()
        
        self.initSetting()
        
    def updateStates(self, key='', extra={}):
        self.user_id, self.setUserId = self.gstate.useState("user_id")
        self.user_name, self.setUserName = self.gstate.useState("user_name")
        self.is_login, self.setIsLogin = self.gstate.useState("is_login")
        self.account_dict, self.setAccountDict = self.gstate.useState("account_dict")
    
    def eventReg(self):
        self.update.connect(self.updateStates)

    def afterSetting(self):
        accounts = self.account_dict.keys()
        
        for accno in accounts:
            balanceTable = getattr(self.ui, f"_{accno}_balanceTable")
            setTableSizeSameHor(balanceTable)
            setTableSizeSameVer(balanceTable)
    
    def show(self):
        
        self.stateReg()
        self.updateStates()
        self.eventReg()
        
        self.callback_handler.watch()
        
        self.login()
        
        self.getAccountInfo()
        
        accounts = self.account_dict.keys()
        for accno in accounts:
            newAccInfo(self.ui, accno)
        
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.ui.verticalLayout_3.addItem(verticalSpacer)
    
        self.ui.show()
        
        # If ui is loaded, calculate table once after loading
        QTimer.singleShot(0, self.afterSetting)
        
    def login(self):
        login_success = self.api.login()
        
        try:
            if login_success:
                self.setIsLogin(True)
                logger.debug("로그인에 성공했습니다")
            else:
                raise LoginFailedException
        except LoginFailedException as e:
            self.setIsLogin(False)
            logger.error(e)
            
    def getAccountInfo(self):
        acc_list, user_id, user_name = self.api.getLoginInfo()
        
        account_dict = {}
        for acc_no in acc_list:
            account_dict[acc_no] = Account(acc_no) 
            
        self.setUserName(user_name)
        self.setUserId(user_id)
        self.setAccountDict(account_dict)