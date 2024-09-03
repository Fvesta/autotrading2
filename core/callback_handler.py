from PySide2.QtCore import SIGNAL
from PySide2.QtAxContainer import QAxWidget

from core.constants import TR_RETURN_MAP
from core.scr_manager import scr_manager
from core.api import API
from core.global_state import UseGlobal
from core.utils.utils import isStock

signal_map = {
    "OnEventConnect": SIGNAL("OnEventConnect(int)"),
    "OnReceiveTrData": SIGNAL("OnReceiveTrData(QString, QString, QString, QString, QString, int, QString, QString, QString)"),
}

class CallbackHandler(UseGlobal):
    def __init__(self):
        super().__init__()
        self.api = API()
        self.ocx: QAxWidget = self.api.ocx
        
    def watch(self):
        self.eventReg()
        
    def eventReg(self):
        self.ocx.connect(signal_map["OnEventConnect"], self.loginSuccess)
        self.ocx.connect(signal_map["OnReceiveTrData"], self.trCallback)
        
    # OnEventConnect
    def loginSuccess(self, retcode):
        if retcode == 0:
            self.gstate.unlock(True)
        else:
            self.gstate.unlock(False)
            
    def trCallback(self, scrno, rqname, trcode, record, next, *args):
        
        scr_manager.deAct(scrno)
        
        if rqname == "계좌평가현황요청":
            single_data = self.api.getData(rqname, trcode, record, TR_RETURN_MAP["계좌평가현황요청"]["single"])
            multi_data = self.api.getData(rqname, trcode, record, TR_RETURN_MAP["계좌평가현황요청"]["multi"], True)
        
            filtered_multi_data = list(filter(lambda row_data: isStock(row_data.get("종목코드")), multi_data))
            
            ret_data = {
                "single": single_data,
                "multi": filtered_multi_data
            }
            
        self.gstate.unlock(ret_data)
        