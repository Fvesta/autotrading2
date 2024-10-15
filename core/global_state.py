from functools import partial
from PySide2.QtCore import QEventLoop, QTimer, QObject

from core.logger import logger
from core.wait_timer import WaitTimer

class UseGlobal:
    def __init__(self):
        self.gstate = GlobalState()
    
    def updateStates(self, key='', extra={}):
        pass
    
    def stateReg(self):
        self.gstate.addConsumer(self)
    
    def stateTerm(self):
        self.gstate.delConsumer(self)

class GlobalState:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(GlobalState, cls).__new__(cls)
            
        return cls.instance
    
    def __init__(self):
        if hasattr(self, "initialized"):
            return
        
        # User states
        self._state = {}
        
        self._state["user_id"] = None
        self._state["user_name"] = None
        self._state["is_login"] = False
        self._state["account_dict"] = {}
        
        # Market stocks
        self.kospi_stocks = {}
        self.kosdaq_stocks = {}
        
        # Loop block
        self._eventloop = {
            "tr_loop": QEventLoop(),
            "order_loop": QEventLoop()
        }
        self._return = {}
        
        # Tr request wait timer
        self.tr_timer = WaitTimer("tr_timer", 400, lambda: self.__exitEventLoop("tr_loop"))
        
        # Order request wait timer
        self.order_timer = WaitTimer("order_timer", 400, lambda: self.__exitEventLoop("order_loop"))
        
        # One direction state binding
        self.consumers = set()
        
        # Window state
        self.activated_windows = {}
        
        # Lock sendtr, sendorder
        self.tr_used = False
        self.order_used = False
        
        self.initialized = True
    
    ############################################
    # Main eventloop block
    ############################################
    def trLock(self):
        loop = QEventLoop()
        
        def get_lock():
            if not self.tr_used:
                self.tr_used = True
                loop.quit()
                
        timer = QTimer()
        timer.timeout.connect(get_lock)
        timer.start(100)
        
        loop.exec_()
        
    def trUnlock(self):
        self.tr_used = False
        
    def orderLock(self):
        loop = QEventLoop()
        
        def get_lock():
            if not self.order_used:
                self.order_used = True
                loop.quit()
                
        timer = QTimer()
        timer.timeout.connect(get_lock)
        timer.start(100)
        
        loop.exec_()
        
    def orderUnlock(self):
        self.order_used = False
    
    def lock(self, seed="main_block", timer=False, time=2000):
        self._eventloop[seed] = QEventLoop()
        self._return[seed] = None
        
        if timer:
            QTimer.singleShot(time, partial(self.timeout, seed))
        
        if not self._eventloop[seed].isRunning():
            self._eventloop[seed].exec_()
        
        ret = self.getRet(seed)
        if ret == None:
            logger.error("Request error")
            
        return ret
    
    def getRet(self, seed):
        if seed not in self._return:
            return None
        
        ret = self._return[seed]
        del self._return[seed]
        return ret
    
    def unlock(self, ret=None, seed="main_block"):
        self._return[seed] = ret
        
        if seed not in self._eventloop:
            return
        
        self._eventloop[seed].exit()
        del self._eventloop[seed]
        
    ############################################
    # One Direction state binding
    ############################################
    
    def addConsumer(self, obj):
        self.consumers.add(obj)
        
    def delConsumer(self, obj):
        self.consumers.remove(obj)
    
    def __setUpdateState(self, key, update_key, extra, value):
        # If user set key
        if update_key == None:
            update_key = key
        
        self._state[key] = value
        for obj in self.consumers:
            obj.update.emit(update_key, extra)
    
     # If state[key] is changed, update all local states in self.consumers
    def useState(self, key):
        if key not in self._state:
            raise KeyError("Key does not exist in gstate")
            
        return [self._state[key], lambda value, update_key=None, extra={}: self.__setUpdateState(key, update_key, extra, value)]
    
    def getState(self, key):
        return self._state[key]
    
    def callUpdate(self, key=None, extra={}):
        for obj in self.consumers:
            obj.update.emit(key, extra)
    
    ############################################
    # Kiwoom limit dealing
    ############################################
    
    def __exitEventLoop(self, key):
        try:
            event_loop = self._eventloop[key]
        
            event_loop.exit()
        except:
            logger.debug("Eventloop not executing")
