from core.errors import KiwoomException
from PySide2.QtAxContainer import QAxWidget


class Kiwoom:
    def __init__(self, ocx):
        self.ocx: QAxWidget = ocx
    
    ############################################
    # Login
    ############################################
    
    def commConnect(self):
        self.ocx.dynamicCall("CommConnect()")
        
    def getLoginInfo(self, tag):
        ret = self.ocx.dynamicCall("GetLoginInfo(QString)", [tag])
        return ret
    
    ############################################
    # Utis
    ############################################
    
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
    
    ############################################
    # Condition
    ############################################
    
    def getConditionLoad(self):
        self.ocx.dynamicCall("GetConditionLoad()")
        
    def getConditionNameList(self):
        ret = self.ocx.dynamicCall("GetConditionNameList()")
        return ret
    
    def sendCondition(self, scrno, condname, cidx, tag):
        ret = self.ocx.dynamicCall("SendCondition(QString, QString, int, int)", [scrno, condname, cidx, tag])
        
        if ret == 0:
            raise KiwoomException(-10, "Load condstocks fail")
        
    def sendConditionStop(self, scrno, condname, cidx):
        self.ocx.dynamicCall("SednConditionStop(QString, QString, int)", [scrno, condname, cidx])
    
    ############################################
    # Tr request
    ############################################
    
    def setInputValue(self, tid, value):
        self.ocx.dynamicCall("SetInputValue(QString, QString)", [tid, value])
    
    def commRqData(self, rqname, trcode, next, scrno):
        
        kiwoom_retcode = self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", [rqname, trcode, next, scrno])
        
        if kiwoom_retcode == -200 or kiwoom_retcode == -201 or kiwoom_retcode == -202:
            raise KiwoomException(kiwoom_retcode)
        
    def commKwRqData(self, rqname, stockcode_list, next, scrno):
        
        stockcode_input=""
        for stockcode in stockcode_list:
            stockcode_input += f"{stockcode};"
        
        kiwoom_retcode = self.ocx.dynamicCall("CommKwRqData(QString, int, int, int, QString, QString)", [stockcode_input, next, len(stockcode_list), 0, rqname, scrno])
        
        if kiwoom_retcode == -202:
            raise KiwoomException(kiwoom_retcode)
        
    def getRepeatCnt(self, trcode, record):
        rows = self.ocx.dynamicCall("GetRepeatCnt(QString, QString)", [trcode, record])
        return rows
        
    def getCommData(self, rqname, trcode, idx, item):
        data = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", [trcode, rqname, idx, item])
        return data.strip()
    
    ############################################
    # Real request
    ############################################
    
    def setRealReg(self, scrno, stockcode_list, fid_list, tag):
        self.ocx.dynamicCall("SetRealReg(QString, QString, QString, QString)", [scrno, stockcode_list, fid_list, tag])
        
    def getCommRealData(self, stockcode, fid):
        data = self.ocx.dynamicCall("GetCommRealData(QString, int)", [stockcode, fid])
        return data
    
    ############################################
    # Order request
    ############################################
    
    # orderType => 1: 신규매수, 2: 신규매도, 3: 매수취소, 4: 매도취소, 5:매수정정, 6: 매도정정
    # tradeType => 00:지정가, 03:시장가, 05:조건부지정가, 06:최유리지정가, 07:최우선지정가, 10:지정
    # 가IOC, 13:시장가IOC, 16:최유리IOC, 20:지정가FOK, 23:시장가FOK, 26:최유리FOK, 61:장전시간
    # 외종가, 62:시간외단일가, 81:장후시간외종가
    def sendOrder(self, rqname, scrno, accno, ordertype, stockcode, quantity, price, tradetype, org_orderno):
        
        kiwoom_retcode = self.ocx.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QStromg)",
                                   [rqname, scrno, accno, ordertype, stockcode, quantity, price, tradetype, org_orderno])

        if kiwoom_retcode != 0:
            raise KiwoomException(kiwoom_retcode)
        
    def getChejanData(self, fid):
        data = self.ocx.dynamicCall("GetChejanData(int)", fid)
        return data
        