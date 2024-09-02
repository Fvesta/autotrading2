from core.constants import TRCODE_DICT
from core.logger import logger
from core.errors import ErrorCode, KiwoomException
from core.scr_manager import scr_manager
from core.global_state import UseGlobal
from core.util_func import getRegStock

class API(UseGlobal):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(API, cls).__new__(cls)
            
        return cls.instance
    
    def __init__(self, kiwoom=None):
        if hasattr(self, "initialized"):
            return
        
        super().__init__()
        self.kiwoom = kiwoom
        self.ocx = self.kiwoom.ocx
        
        self.initialized = True
        
    def login(self):
        self.kiwoom.commConnect()
        login_success = self.gstate.lock()
        
        if login_success:
            return 0

        return ErrorCode.OP_ERROR

    def getLoginInfo(self):
        acc_total = self.kiwoom.getLoginInfo("ACCNO")
        acc_list = acc_total.split(";")[:-1]
        
        user_id = self.kiwoom.getLoginInfo("USER_ID")
        user_name = self.kiwoom.getLoginInfo("USER_NAME")
        
        return [acc_list, user_id, user_name]
    
    def getStockName(self, stockcode):
        stockcode = getRegStock(stockcode)
        
        return self.kiwoom.getMasterCodeName(stockcode)
    
    def getCodeListByMarket(self, market):
        marketcode = 0
        
        if market == 'kospi':
            marketcode = 0
        if market == 'kosdaq':
            marketcode = 10
        
        return self.kiwoom.getCodeListByMarket(marketcode)

    def sendTr(self, rqname, inputs, next=False):
        trcode = TRCODE_DICT[rqname]
        
        tr_timer = self.gstate.tr_timer
        tr_loop = self.gstate._eventloop["tr_loop"]
        
        if tr_timer.isWait():
            tr_loop.exec_()

        tr_timer.startWait()
        
        if trcode == "opw00004":
            if len(inputs) != 4:
                return ErrorCode.OP_INPUT_ERROR
            
            accno, password, _, _ = inputs
            self.kiwoom.setInputValue("계좌번호", accno)
            self.kiwoom.setInputValue("비밀번호", password)
            self.kiwoom.setInputValue("상장폐지조회구분", 1)
            self.kiwoom.setInputValue("비밀번호입력매체구분", "00")
            
        if next:
            try:
                self.kiwoom.commRqData(rqname, trcode, 2, scr_manager.scrAct(trcode.lower()))
            except KiwoomException as e:
                logger.warning(e)
                return ErrorCode.OP_KIWOOM_ERROR
            
            ret = self.gstate.lock()
            return ret
        
        try:
            self.kiwoom.commRqData(rqname, trcode, 0, scr_manager.scrAct(trcode.lower()))
        except KiwoomException as e:
            logger.warning(e)
            return ErrorCode.OP_KIWOOM_ERROR
        
        ret = self.gstate.lock()
        return ret
    
    def getData(self, rqname, trcode, record, info_list, multi=False):
        
        if multi:
            rows = self.kiwoom.getRepeatCnt(trcode, record)
            if rows == 0:
                rows = 1
                
            data_list = []
            for row in range(rows):
                data = []
                for info in info_list:
                    data.append(self.kiwoom.getCommData(rqname, trcode, row, info))
                    
                data_list.append(data)
            
            return data_list
        
        data = []
        for info in info_list:
            data.append(self.kiwoom.getCommData(rqname, trcode, 0, info))
        
        return data
                
        