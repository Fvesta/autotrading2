from PySide2.QtWidgets import *
from PySide2.QtCore import QTimer, Signal, Qt, QObject

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
        pass
    
    def show(self):
        
        self.stateReg()
        self.updateStates()
        self.eventReg()
        
        self.callback_handler.watch()
        
        self.login()
        
        self.getAccountInfo()
        # newAccInfo(self.ui, "123")
        
        # verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # self.ui.verticalLayout_3.addItem(verticalSpacer)
        
        # tbData = [
        #     ["예탁자산", "당월실현손익", "당일실현손익"],
        #     ["1000", "1000", "1000"],
        #     ["총매입가", "총평가금", "수익률"],
        #     ["1000", "1000", "1000"]
        # ]
        # for i in range(len(tbData)):
        #     for j in range(3):
        #         item = QTableWidgetItem(str(tbData[i][j]))
        #         item.setTextAlignment(Qt.AlignCenter)
        #         self.ui.tableWidget.setItem(i, j, item)
                
    
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
            account_dict[acc_no] = Account(self.api, acc_no) 
        
        for acc in account_dict.values():
            acc.comboBoxSet = {
                "condCombo1": "선택안됨",
                "condCombo2": "선택안됨",
                "condCombo3": "선택안됨",
            }
            
        self.setUserName(user_name)
        self.setUserId(user_id)
        self.setAccountDict(account_dict)