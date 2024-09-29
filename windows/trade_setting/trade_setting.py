from PySide2.QtCore import Signal

from core.errors import ErrorCode
from core.logger import logger
from core.api import API
from core.utils.utils import getAccnoFromObj
from windows.win_abs import WindowAbs, showModal


class TradeSettingWin(WindowAbs):
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
        self.ui.title.setProperty("class", "tx-title")
    
    def afterSetting(self):
        self.updateStyle()
        
    def updateStates(self, key='', extra={}):
        pass
    
    def eventReg(self):
        self.update.connect(self.updateStates)
    
    def eventTerm(self):
        self.update.disconnect(self.updateStates)
    
    @showModal
    def show(self):
        
        # Register States, add events
        self.stateReg()
        self.updateStates()
        self.eventReg()
        