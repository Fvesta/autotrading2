from functools import partial
from PySide2.QtCore import QEventLoop, QTimer

class UseGlobal:
    def __init__(self):
        self.gstate = GlobalState()

class GlobalState:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(GlobalState, cls).__new__(cls)
            
        return cls.instance
    
    def __init__(self):
        if hasattr(self, "initialized"):
            return
        
        self._state = {}
        
        # Loop block
        self._eventloop = {}
        self._return = {}
        
        self.initialized = True
    
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
        