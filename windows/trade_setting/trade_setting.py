from PySide2.QtCore import Signal, QTimer

from core.logger import logger
from core.api import API
from style.utils import setTableSizeSameHor, setTableSizeSameVer
from windows.win_abs import WindowAbs, showModal


class TradeSettingWin(WindowAbs):
    update = Signal(str, dict)
    
    def __init__(self, name, ui_path, css_path):
        WindowAbs.__init__(self, name, ui_path, css_path)
        try:
            self.accno = self.name.split("_")[1]
        except ValueError:
            logger.error("Wrong window name")
            return
        
        self.api = API()
        
        self.initSetting()
        
    def initSetting(self):
        self.ui.title.setProperty("class", "tx-title")
    
    def afterSetting(self):
         self.updateStyle()
        
    def updateStates(self, key='', extra={}):
        pass
    
    def eventReg(self):
        pass
    
    @showModal
    def show(self):
        
        # Register States, add events
        self.stateReg()
        self.updateStates()
        self.eventReg()
        