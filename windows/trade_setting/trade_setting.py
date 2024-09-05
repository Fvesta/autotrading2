from PySide2.QtCore import Signal, QTimer

from core.logger import logger
from core.api import API
from core.global_state import UseGlobal
from style.utils import setTableSizeSameHor, setTableSizeSameVer
from windows.win_abs import WindowAbs, showModal


class TradeSettingWin(WindowAbs, UseGlobal):
    update = Signal(str, dict)
    
    def __init__(self, name, ui_path, css_path):
        WindowAbs.__init__(self, name, ui_path, css_path)
        UseGlobal.__init__(self)
        try:
            self.accno = self.name.split("_")[1]
        except ValueError:
            logger.error("Wrong window name")
            return
        
        self.api = API()
        
        self.initSetting()
        
    def initSetting(self):
        self.updateStyle()
        
    def updateStates(self, key='', extra={}):
        pass
    
    def eventReg(self):
        pass
    
    def afterSetting(self):
        tableWidget = self.ui.tableWidget
        tableWidget2 = self.ui.tableWidget_2
        
        setTableSizeSameHor(tableWidget)
        setTableSizeSameVer(tableWidget)
        setTableSizeSameHor(tableWidget2)
        setTableSizeSameVer(tableWidget2)
    
    @showModal
    def show(self):
        
        # Register States, add events
        self.stateReg()
        self.updateStates()
        self.eventReg()
        