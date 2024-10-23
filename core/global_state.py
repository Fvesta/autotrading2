import pythoncom
from PySide2.QtCore import QTimer

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
        self._state["total_acc_list"] = []
        self._state["selected_acc_list"] = []
        self._state["account_dict"] = {}
        
        # GUI states
        self.text_size = "13px"
        
        # Market stocks
        self.kospi_stocks = {}
        self.kosdaq_stocks = {}
        
        # Time block
        self._return = {}
        
        self.login_block = False
        self.tr_block = False
        self.order_block = False
        
        # One direction state binding
        self.consumers = set()
        
        # Window state
        self.activated_windows = {}
        
        self.initialized = True
    
    ############################################
    # Main block
    ############################################
    
    def trTimeBlock(self):
        def timeDone():
            self.tr_block = False
            
        # Time check(kiwoom limitation)
        while self.tr_block:
            pythoncom.PumpWaitingMessages()
            
        self.tr_block = True
        QTimer.singleShot(300, timeDone)
        
    def orderTimeBlock(self):
        def timeDone():
            self.order_block = False
            
        # Time check(kiwoom limitation)
        while self.order_block:
            pythoncom.PumpWaitingMessages()
            
        self.order_block = True
        QTimer.singleShot(300, timeDone)
    
    def lock(self, seed="main_block"):
        if seed not in self._return:
            self._return[seed] = None

        while self._return[seed] == None:
            pythoncom.PumpWaitingMessages()
        
        ret = self._return[seed]
        self._return[seed] = None
        
        return ret
    
    def unlock(self, ret={}, seed="main_block"):
        self._return[seed] = ret
        
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
