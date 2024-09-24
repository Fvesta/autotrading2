from PySide2.QtCore import Signal, QObject

from core.constants import REAL_NO_MAP, REAL_RET_MAP, TRCODE_DICT
from core.kiwoom import Kiwoom
from core.logger import logger
from core.errors import ErrorCode, KiwoomException
from core.scr_manager import scr_manager
from core.global_state import UseGlobal
from core.utils.utils import getRegStock

class API(UseGlobal, QObject):
    update = Signal(str, dict)
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(API, cls).__new__(cls)
            
        return cls.instance
    
    def __init__(self, kiwoom=None):
        if hasattr(self, "initialized"):
            return
        
        QObject.__init__(self)
        UseGlobal.__init__(self)
        self.kiwoom: Kiwoom = kiwoom
        self.ocx = self.kiwoom.ocx
        
        self.stateReg()
        self.updateStates()
        self.eventReg()
        
        self.initialized = True
        
    def eventReg(self):
        self.update.connect(self.updateStates)
        
    def updateStates(self, key="", extra={}):
        self.account_dict = self.gstate.getState("account_dict")
    
    ############################################
    # Login
    ############################################
    
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
    
    def getAccObj(self, accno):
        if accno not in self.account_dict:
            logger.warning("accno is not in account_dict")
            return None
        
        return self.account_dict[accno]
    
    ############################################
    # Stocks
    ############################################
    
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

    def getStockObj(self, stockcode):
        stockcode = getRegStock(stockcode)
        
        if stockcode in self.gstate.kospi_stocks:
            return self.gstate.kospi_stocks[stockcode]
        elif stockcode in self.gstate.kosdaq_stocks:
            return self.gstate.kosdaq_stocks[stockcode]
        
        return None
    
    ############################################
    # Conditions
    ############################################
    
    def loadCondition(self):
        self.kiwoom.getConditionLoad()
        load_success = self.gstate.lock()
        
        return load_success
    
    def getConditionNameList(self):
        ret = self.kiwoom.getConditionNameList()
        cond_list = ret.split(";")[:-1]
        
        return cond_list
    
    def sendCondition(self, *args):
        
        tr_timer = self.gstate.tr_timer
        tr_loop = self.gstate._eventloop["tr_loop"]
        
        if tr_timer.isWait():
            tr_loop.exec_()

        tr_timer.startWait()
    
        self.kiwoom.sendCondition(*args)
        
    def sendConditionStop(self, *args):
        self.kiwoom.sendConditionStop(*args)
        
        
    ############################################
    # Tr functions
    ############################################
    
    def sendTr(self, rqname, inputs, next=False):
        trcode = TRCODE_DICT[rqname]
        
        tr_timer = self.gstate.tr_timer
        tr_loop = self.gstate._eventloop["tr_loop"]
        
        if tr_timer.isWait():
            tr_loop.exec_()

        tr_timer.startWait()
        
        if rqname == "계좌평가현황요청":
            if len(inputs) != 4:
                return ErrorCode.OP_INPUT_ERROR
            
            accno, password, _, _ = inputs
            self.kiwoom.setInputValue("계좌번호", accno)
            self.kiwoom.setInputValue("비밀번호", password)
            self.kiwoom.setInputValue("상장폐지조회구분", 1)
            self.kiwoom.setInputValue("비밀번호입력매체구분", "00")
            
        if rqname == "주식기본정보요청":
            if len(inputs) != 1:
                return ErrorCode.OP_INPUT_ERROR
            
            stockcode = inputs
            self.kiwoom.setInputValue("종목코드", stockcode)
            
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
    
    def getTrData(self, rqname, trcode, record, info_list, multi=False):
        
        if multi:
            rows = self.kiwoom.getRepeatCnt(trcode, record)
            if rows == 0:
                rows = 1
                
            data_list = []
            for row in range(rows):
                data = {}
                for info in info_list:
                    data[info] = self.kiwoom.getCommData(rqname, trcode, row, info)
                    
                data_list.append(data)
            
            return data_list
        
        data = {}
        for info in info_list:
            data[info] = self.kiwoom.getCommData(rqname, trcode, 0, info) 

        return data
    
    ############################################
    # Real functions
    ############################################
    
    def setRealReg(self, *args):
        self.kiwoom.setRealReg(*args)
        
    def getRealData(self, stockcode, real_type):
        
        data = {}
        for data_type in REAL_RET_MAP[real_type]:
            data[data_type] = self.kiwoom.getCommRealData(stockcode, REAL_NO_MAP[data_type])    
        
        return data
    
    ############################################
    # Order request
    ############################################
    
    def sendOrder(self, *args):
        
        order_timer = self.gstate.order_timer
        order_loop = self.gstate._eventloop["order_loop"]
        
        if order_timer.isWait():
            order_loop.exec_()

        order_timer.startWait()
        
        try:
            self.kiwoom.sendOrder(*args)
            single_data = self.gstate.lock()
        except KiwoomException as e:
            logger.warning(e)
            return ErrorCode.OP_KIWOOM_ERROR

        orderno = single_data.get("주문번호", "")
        if orderno == "":
            return ErrorCode.OP_ERROR
        
        return orderno
    
    def getChejanData(self, tradetype):    
        # 주문체결
        data = {}
        if tradetype == "0":
            for data_type in REAL_RET_MAP["주문체결"]:
                data[data_type] = self.kiwoom.getChejanData(REAL_NO_MAP[data_type])
        
        # 잔고
        elif tradetype == "1":
            for data_type in REAL_RET_MAP["잔고"]:
                data[data_type] = self.kiwoom.getChejanData(REAL_NO_MAP[data_type])
                
        return data
