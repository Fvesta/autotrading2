from PySide2.QtWidgets import *
from PySide2.QtCore import Signal

from core.api import API
from core.logger import logger
from windows.win_abs import WindowAbs, showModal


class SelectAccWin(WindowAbs):
    update = Signal(str, dict)
    
    def __init__(self, name, ui_path, css_path):
        WindowAbs.__init__(self, name, ui_path, css_path)
        
        self.api = API()
        
        self.acc_check_list = []
        
        self.initSetting()
        
    def initSetting(self):
        self.ui.setWindowTitle(f"계좌선택")
        self.ui.announce_label.setProperty("class", "tx-bold")
        
    def updateStates(self, key="", extra={}):
        self.account_list, self.setAccountList = self.gstate.useState("account_list")
    
    def eventReg(self):
        self.update.connect(self.updateStates)
        self.ui.select_done_btn.clicked.connect(self.selectDone)
    
    def eventTerm(self):
        self.update.disconnect(self.updateStates)
        self.ui.select_done_btn.clicked.disconnect(self.selectDone)
        
    @showModal
    def show(self):
        self.stateReg()
        self.updateStates()
        self.eventReg()
        
        # Set accounts
        for acc in self.account_list:
            acc_check = QCheckBox(acc, self.ui.scrollArea)
            self.acc_check_list.append(acc_check)
            
            self.ui.verticalLayout_2.addWidget(acc_check)
            
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.ui.verticalLayout_2.addItem(verticalSpacer)
            
    def close(self):
        self.ui.close()
    
    def selectDone(self):
        
        new_acc_list = []
        for checkbox in self.acc_check_list:
            if checkbox.isChecked():
                new_acc_list.append(checkbox.text())
                
        self.setAccountList(new_acc_list)
        
        # Login loop quit
        try:
            login_loop = self.gstate._eventloop["login_loop"]
        
            login_loop.exit()
        except:
            logger.debug("Eventloop not executing")
        