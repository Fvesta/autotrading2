from PySide2.QtWidgets import *
from PySide2.QtCore import QTimer

from core.api import API
from core.callback_handler import CallbackHandler
from core.errors import LoginFailedException
from core.logger import logger
from style.utils import setTableSizeSameHor, setTableSizeSameVer
from windows.main_win.acc_info import newAccInfo
from windows.win_abs import WindowAbs

class MainWin(WindowAbs):
    def __init__(self, name, ui_path, css_path):
        WindowAbs.__init__(self, name, ui_path, css_path)
        self.api = API()
        
        self.callback_handler = CallbackHandler()
        
        self.initSetting()
        
    def initSetting(self):
        
        newAccInfo(self.ui, "123")
        
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.ui.verticalLayout_3.addItem(verticalSpacer)
        
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
                
        self.updateStyle()
        
    def afterSetting(self):
        pass
    
    def show(self):
        self.callback_handler.watch()
        self.login()
    
        self.ui.show()
        
        # If ui is loaded, calculate table once after loading
        QTimer.singleShot(0, self.afterSetting)
        
    def login(self):
        login_success = self.api.login()
        
        try:
            if login_success:
                logger.error("로그인에 성공했습니다")
            else:
                raise LoginFailedException
        except LoginFailedException as e:
            logger.error(e)