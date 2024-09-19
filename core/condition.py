from PySide2.QtCore import QThread
import debugpy
import queue

from core.errors import KiwoomException
from core.global_state import UseGlobal
from core.logger import logger
from core.utils.stock_util import getRegStock
from core.wait_timer import WaitTimer
from core.scr_manager import scr_manager 

class Condition:
    
    def __init__(self, cidx, condname):
        self.cidx = cidx
        self.condname = condname
        self.req_timer = WaitTimer(self.condname, 61000)
        self.cond_stocks = set()
        
    def addStock(self, stockcode):
        try:
            stockcode = getRegStock(stockcode)
        except ValueError as e:
            logger.warning("addStock: Wrong stockcode")
        
        self.cond_stocks.add(stockcode)
        
    def removeStock(self, stockcode):
        try:
            stockcode = getRegStock(stockcode)
            self.cond_stocks.remove(stockcode)
        except ValueError as e:
            logger.warning("removeStock: Wrong stockcode")
        except KeyError as e:
            logger.debug("removeStock: already removed")
        
    
class CondManager(QThread, UseGlobal):
    def __new__(cls, *args):
        if not hasattr(cls, "instance"):
            cls.instance = super(CondManager, cls).__new__(cls)
            
        return cls.instance
    
    def __init__(self):
        
        if hasattr(self, "initialized"):
            return
        
        QThread.__init__(self)
        UseGlobal.__init__(self)
        
        self.event_queue = queue.Queue()
        
        self.api = None
        self.reg_count = 0
        self.cond_dict = {}

        self.reg_cond_dict = {}
        self.seed_callback_dict = {}
        
        self.initialized = True
        
    def run(self):
        debugpy.debug_this_thread()
        
        while True:
            event = self.event_queue.get()
            
            if event == None:
                break
            
            self.condBackgroundProcess(event)
    
    def ready(self, API):
        self.api = API
    
    def stop(self):
        self.event_queue.put(None)
    
    def addEvent(self, event):
        self.event_queue.put(event)
        
    def condBackgroundProcess(self, event):
        stockcode, tag, condname, cidx = event
        
        if condname not in self.reg_cond_dict:
            return
        
        callback_seed_set = self.reg_cond_dict[condname]
        
        for seed in callback_seed_set:
            callback = self.seed_callback_dict[seed]
            callback(seed, stockcode, tag, condname, cidx)
        
    ############################################
        # User functions
    ############################################
        
    def regCondReal(self, seed, condname_list, callback):
        self.seed_callback_dict[seed] = callback
        
        for condname in condname_list:
            if condname in self.reg_cond_dict:
                self.reg_cond_dict[condname].add(seed)
            else:
                self.reg_cond_dict[condname] = set([seed])
                
            # If new reg condname
            if len(self.reg_cond_dict[condname]) == 1:
                condobj: Condition = self.cond_dict[condname]
                
                if condobj.req_timer.isWait():
                    continue
                
                condobj.req_timer.startWait()
                try:
                    self.api.sendCondition(scr_manager.scrAct("sendCondition"), condname, condobj.cidx, 1)
                    self.reg_count += 1
                
                    cond_stock_list = self.gstate.lock()
                    
                    condobj.cond_stocks = set(cond_stock_list)
                except KiwoomException as e:
                    logger.warning(e)
    
    def termCondReal(self, seed):
        
        for condname in self.reg_cond_dict.keys():
            if seed in self.reg_cond_dict[condname]:

                self.reg_cond_dict[condname].remove(seed)
                
                if len(self.reg_cond_dict[condname]) == 0:
                    condobj: Condition = self.cond_dict[condname]
                    
                    self.api.sendConditionStop(scr_manager.getNo("sendCondition"), condname, condobj.cidx)
                    self.reg_count -= 1
                
        if seed in self.seed_callback_dict:
            del self.seed_callback_dict[seed]
            
cond_manager = CondManager()
