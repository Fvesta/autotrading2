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
            "tr_loop": QEventLoop()
        }
        self._return = {}
        
        # Tr request wait timer
        self.tr_timer = WaitTimer("tr_timer", 300, lambda: self.__quitEventLoop("tr_loop"))
        
        
        self.initialized = True
        
        # One direction state binding
        self.consumers = set()
        
        # Window state
        self.activated_windows = {}
    
    ############################################
    # Main eventloop block
    ############################################
    def lock(self, seed="main_block", timer=False, time=2000):
        self._eventloop[seed] = QEventLoop()
        self._return[seed] = None
        
        if timer:
            QTimer.singleShot(time, partial(self.timeout, seed))
            
        self._eventloop[seed].exec_()
        
        return self.getRet(seed)
    
    def getRet(self, seed):
        if not seed in self._return:
            return None
        
        ret = self._return[seed]
        del self._return[seed]
        return ret
    
    def unlock(self, ret=None, seed="main_block"):
        self._return[seed] = ret
        
        if not seed in self._eventloop:
            return
        
        self._eventloop[seed].quit()
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
    
    ############################################
    # Kiwoom limit dealing
    ############################################
    
    def __quitEventLoop(self, key):
        try:
            event_loop = self._eventloop[key]
        
            event_loop.quit()
        except:
            logger.debug("Eventloop not executing")
    