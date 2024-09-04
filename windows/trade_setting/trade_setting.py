from PySide2.QtCore import Signal, QTimer

from core.api import API
from core.global_state import UseGlobal
from windows.win_abs import WindowAbs


class TradeSettingWin(WindowAbs, UseGlobal):
    update = Signal(str, dict)
    
    def __init__(self, name, ui_path, css_path):
        WindowAbs.__init__(self, name, ui_path, css_path)
        UseGlobal.__init__(self)
        
        self.api = API()
        
        self.initSetting()
        
    def initSetting(self):
        self.updateStyle()
        
    def updateStates(self, key='', extra={}):
        pass
    
    def eventReg(self):
        pass
    
    def afterSetting(self):
        pass
        
    def show(self):
        
        # Register States, add events
        self.stateReg()
        self.updateStates()
        self.eventReg()
        
        self.ui.show()
        
        # If ui is loaded, calculate table once after loading
        QTimer.singleShot(0, self.afterSetting)