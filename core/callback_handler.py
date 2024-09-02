from PySide2.QtCore import SIGNAL

from core.scr_manager import scr_manager
from core.api import API
from core.global_state import UseGlobal
from core.util_func import isStock

signal_map = {
    "OnEventConnect": SIGNAL("OnEventConnect(int)"),
    "OnReceiveTrData": SIGNAL("OnReceiveTrData(QString, QString, QString, QString, QString, int, QString, QString, QString)"),
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
            single_data = self.api.getData(rqname, trcode, record, ["추정예탁자산", "당월투자손익", "당일투자손익", "D+2추정예수금"])
            multi_data = self.api.getData(rqname, trcode, record, ["종목코드", "종목명", "보유수량", "평균단가", "매입금액", "현재가", "평가금액", "손익율"], True)
        
            filtered_multi_data = list(filter(lambda row_data: isStock(row_data[0]), multi_data))
            
            ret_data = {
                "single": single_data,
                "multi": filtered_multi_data
            }
            
        self.gstate.unlock(ret_data)
        