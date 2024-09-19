from PySide2.QtCore import QThread, Signal
import debugpy
import queue

from core.logger import logger
from core.constants import ORDER_TAG, ORDER_TYPE
from core.errors import ErrorCode
from core.scr_manager import scr_manager
from core.wait_timer import WaitTimer

class OrderManager(QThread):
    acc_update_signal = Signal()
    
    def __new__(cls, *args):
        if not hasattr(cls, "instance"):
            cls.instance = super(OrderManager, cls).__new__(cls)
            
            return cls.instance
        
    def __init__(self):
        
        if hasattr(self, "initialized"):
            return
        
        super().__init__()
        
        self.event_queue = queue.Queue()
        
        self.api = None
        self.seed_callback_dict = {}
        
        # Essential account callback
        self.event_accno_set = set()
        self.account_timer = WaitTimer("account_timer", 1000, self.accTimerCallback)
        
        self.initialized = True
        
    def eventReg(self):
        self.acc_update_signal.connect(self.updateAccounts)
        
    def run(self):
        # Debug setting
        debugpy.debug_this_thread()
        
        while True:
            event = self.event_queue.get()
            
            if event == None:
                break
            
            self.orderBackgroundProcess(event)
        
    def ready(self, API):
        self.api = API
        
    def stop(self):
        self.event_queue.put(None)
        
    def addEvent(self, event):
        self.event_queue.put(event)
        
    def updateAccounts(self):
        
        for accno in self.event_accno_set:
            acc = self.api.getAccObj(accno)
            acc.reqAccInfo()
        
    def accTimerCallback(self):
        if len(self.event_accno_set) == 0:
            return
        
        # Update accounts
        self.acc_update_signal.emit()
            
        # initialize event_accno_set
        self.event_accno_set = set()
        
    def orderBackgroundProcess(self, event):
        tradetype, order_data = event
        
        accno = order_data.get("계좌번호", "")
        if accno == "":
            logger.warning("주문에 계좌번호 정보가 없습니다.")
            return
        
        if not self.account_timer.isWait():
            self.account_timer.startWait()
            
        self.event_accno_set.add(accno)
        
        for seed in self.seed_callback_dict.keys():
            callback = self.seed_callback_dict[seed]
            callback(seed, tradetype, order_data)
    
    ############################################
        # User functions
    ############################################
    
    def regOrderReal(self, seed, callback):
        self.seed_callback_dict[seed] = callback
        
    def termOrderReal(self, seed):
        if seed in self.seed_callback_dict:
            del self.seed_callback_dict[seed]
    
    def buyStockNow(self, accno, stockcode, quantity):
        
        orderno = self.api.sendOrder("주문요청", scr_manager.scrAct("buystock"), accno, ORDER_TYPE["신규매수"], stockcode, quantity, 0, ORDER_TAG["시장가"], "")
    
        if isinstance(orderno, ErrorCode):
            logger.error(f"accno: {accno}, 주문요청에 실패했습니다.")
    
    def buyStockFix(self, accno, stockcode, quantity, ask_step, cancel=False, cancel_buy=False, cancel_time_sec=0):
        pass
    
    def sellStockNow(self, accno, stockcode, quantity):
        pass
    
    def sellStockFix(self, acccno, stockcode, quantity, ask_step, cancel=False, cancel_sell=False, cancel_time_sec=0):
        pass
    
order_manager = OrderManager()
