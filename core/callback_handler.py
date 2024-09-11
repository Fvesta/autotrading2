from PySide2.QtCore import SIGNAL
from PySide2.QtAxContainer import QAxWidget

from core.constants import TR_RETURN_MAP
from core.scr_manager import scr_manager
from core.real_processing import real_manager
from core.api import API
from core.global_state import UseGlobal
from core.stock import Stock
from core.utils.utils import isStock

signal_map = {
    "OnEventConnect": SIGNAL("OnEventConnect(int)"),
    "OnReceiveTrData": SIGNAL("OnReceiveTrData(QString, QString, QString, QString, QString, int, QString, QString, QString)"),
    "OnReceiveRealData": SIGNAL("OnReceiveRealData(QString, QString, QString)"),
    "OnReceiveConditionVer": SIGNAL("OnReceiveConditionVer(int, QString)"),
    "OnReceiveTrCondition": SIGNAL("OnReceiveTrCondition(QString, QString, QString, int, int)")
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
        self.ocx.connect(signal_map["OnReceiveConditionVer"], self.loadConditionSuccess)
        self.ocx.connect(signal_map["OnReceiveTrCondition"], self.getCondStockSuccess)
        self.ocx.connect(signal_map["OnReceiveTrData"], self.trCallback)
        self.ocx.connect(signal_map["OnReceiveRealData"], self.realEventCallback)
        
    # OnEventConnect
    def loginSuccess(self, retcode):
        if retcode == 0:
            self.gstate.unlock(True)
        else:
            self.gstate.unlock(False)
            
    def loadConditionSuccess(self, success, msg):
        if success:
            self.gstate.unlock(True)
        else:
            self.gstate.unlock(False)
            
    def getCondStockSuccess(self, scrno, cond_stocks, condname, cidx, next):
        
        cond_stock_list = cond_stocks.split(";")[:-1]
        self.gstate.unlock(cond_stock_list)
            
    def trCallback(self, scrno, rqname, trcode, record, next, *args):
        
        scr_manager.deAct(scrno)
        
        if rqname == "계좌평가현황요청":
            single_data = self.api.getTrData(rqname, trcode, record, TR_RETURN_MAP["계좌평가현황요청"]["single"])
            multi_data = self.api.getTrData(rqname, trcode, record, TR_RETURN_MAP["계좌평가현황요청"]["multi"], True)
        
            filtered_multi_data = list(filter(lambda row_data: isStock(row_data.get("종목코드")), multi_data))
            
            ret_data = {
                "single": single_data,
                "multi": filtered_multi_data
            }
            
        self.gstate.unlock(ret_data)
        
    def realEventCallback(self, stockcode, real_type, data):
        
        stockobj: Stock = self.api.getStockObj(stockcode)
        
        real_data = {}
        if real_type == "주식체결":
            real_data = self.api.getRealData(stockcode, real_type)
            
            cur_price = real_data["현재가"]
            today_updown_rate = real_data["등락율"]
            today_trans_amount = real_data["누적거래대금"]
            
            stockobj.setStockInfo({
                "cur_price": cur_price,
                "today_updown_rate": today_updown_rate,
                "today_trans_amount": today_trans_amount,
            })
            
        real_manager.addEvent((stockcode, real_type, real_data))