from PySide2.QtCore import QThread
import debugpy
import queue
import sys

from core.constants import REAL_NO_MAP
from core.scr_manager import scr_manager 
        
class RealManager(QThread):
    def __new__(cls, *args):
        if not hasattr(cls, "instance"):
            cls.instance = super(RealManager, cls).__new__(cls)
            
        return cls.instance
    
    def __init__(self):
        
        if hasattr(self, "initialized"):
            return

        super().__init__()
        
        self.event_queue = queue.Queue()
        
        self.api = None
        self.reg_stock_dict = {}
        self.seed_callback_dict = {}
        
        self.fid_set = ""
        for data_type in REAL_NO_MAP.keys():
            self.fid_set += f"{REAL_NO_MAP[data_type]};"
        
        self.initialized = True
    
    def run(self):
        # Debug setting
        if not (getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')): 
            debugpy.debug_this_thread()
        
        while True:
            event = self.event_queue.get()
            
            if event == None:
                break
            
            self.realBackgroundProcess(event)
        
    def ready(self, API):
        self.api = API
    
    def stop(self):
        self.event_queue.put(None)
        
    def addEvent(self, event):
        self.event_queue.put(event)
        
    def realBackgroundProcess(self, event):
        stockcode, real_type, real_data = event
        
        if stockcode not in self.reg_stock_dict:
            return
        
        callback_seed_set = self.reg_stock_dict[stockcode]
        
        for seed in callback_seed_set:
            callback = self.seed_callback_dict[seed]
            callback(seed, stockcode, real_type, real_data)
            
    ############################################
        # User functions
    ############################################
    
    # callback args: seed, stockcode, real_type, real_data
    def regReal(self, seed, stockcode_list, callback = lambda: None):
        self.seed_callback_dict[seed] = callback
        
        # Delete prev seed
        for stockcode in self.reg_stock_dict.keys():
            if seed in self.reg_stock_dict[stockcode]:
                self.reg_stock_dict[stockcode].remove(seed)
        
        # Add new seed
        for stockcode in stockcode_list:
            if stockcode in self.reg_stock_dict:
                self.reg_stock_dict[stockcode].add(seed)
            else:
                self.reg_stock_dict[stockcode] = set([seed])
        
        self.updateReg()
          
    def termReal(self, seed):
        
        # Delete seed
        for stockcode in self.reg_stock_dict.keys():
            if seed in self.reg_stock_dict[stockcode]:
                self.reg_stock_dict[stockcode].remove(seed)

        # Remove callback
        if seed in self.seed_callback_dict:
            del self.seed_callback_dict[seed]
            
        self.updateReg()
            
    def updateReg(self):
        stock_input_split = []
        stock_input = ""
        cnt = 0
        for stockcode in self.reg_stock_dict.keys():
            seed_set = self.reg_stock_dict[stockcode]
            
            # If there is no registered seed, ignore stockcode
            if len(seed_set) == 0:
                continue
            
            cnt += 1
            stock_input += f"{stockcode};"
            
            if cnt > 98:
                stock_input_split.append(stock_input)
                stock_input = ""
                cnt = 0
        
        if cnt > 0:
            stock_input_split.append(stock_input)
                
        for idx, stock_input in enumerate(stock_input_split): 
            
            self.api.setRealReg(scr_manager.scrAct(f"real_processing_{idx}"), stock_input, self.fid_set, 0)
            
real_manager: RealManager = RealManager()
