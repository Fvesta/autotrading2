from PySide2.QtCore import SIGNAL

from core.api import API
from core.global_state import UseGlobal

signal_map = {
    "OnEventConnect": SIGNAL("OnEventConnect(int)")     
}

class CallbackHandler(UseGlobal):
    def __init__(self):
        super().__init__()
        self.api = API()
        self.ocx = self.api.ocx
        
    def watch(self):
        self.eventReg()
        
    def eventReg(self):
        self.ocx.connect(signal_map["OnEventConnect"], self.loginSuccess)
        
    # OnEventConnect
    def loginSuccess(self, code):
        if code == 0:
            self.gstate.unlock(True)
        else:
            self.gstate.unlock(False)