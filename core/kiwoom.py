from core.logger import logger
from core.errors import KiwoomException


class Kiwoom:
    def __init__(self, ocx):
        self.ocx = ocx
    
    # Login
    def commConnect(self):
        self.ocx.dynamicCall("CommConnect()")
        
    def getLoginInfo(self, tag):
        ret = self.ocx.dynamicCall("GetLoginInfo(QString)", [tag])
        return ret
    
    # Utils
    def getMasterCodeName(self, stockcode):
        ret = self.ocx.dynamicCall("GetMasterCodeName(QString)", [stockcode])
        return ret 
    
    def getConnectState(self):
        ret = self.ocx.dynamicCall("GetConnectState()")
        return ret
    
    def getCodeListByMarket(self, marketcode):
        ret = self.ocx.dynamicCall("GetCodeListByMarket(QString)", [marketcode])
        stockcodes = ret.split(";")[:-1]
        return stockcodes
    
    # TR request
    def setInputValue(self, tid, value):
        self.ocx.dynamicCall("SetInputValue(QString, QString)", [tid, value])
    
    def commRqData(self, rqname, trcode, next, scrno):
        
        kiwoom_retcode = self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", [rqname, trcode, next, scrno])
        
        if kiwoom_retcode == -200 or kiwoom_retcode == -201 or kiwoom_retcode == -202:
            raise KiwoomException(kiwoom_retcode)
        
    def getRepeatCnt(self, trcode, record):
        rows = self.ocx.dynamicCall("GetRepeatCnt(QString, QString)", [trcode, record])
        return rows
        
    def getCommData(self, rqname, trcode, idx, item):
        data = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", [trcode, rqname, idx, item])
        return data.strip()