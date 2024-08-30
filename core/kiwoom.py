class Kiwoom:
    def __init__(self, ocx):
        self.ocx = ocx
    
    # Login
    def commConnect(self):
        self.ocx.dynamicCall("CommConnect()")
        
    def getLoginInfo(self, tag):
        ret = self.ocx.dynamicCall("GetLoginInfo(QString)", [tag])
        return ret
    
    def getMasterCodeName(self, stock_code):
        ret = self.ocx.dynamicCall("GetMasterCodeName(QString)", [stock_code])
        return ret 
    
    def getConnectState(self):
        ret = self.ocx.dynamicCall("GetConnectState()")
        return ret