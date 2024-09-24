from PySide2.QtCore import Signal

from core.logger import logger
from core.api import API
from core.condition import cond_manager
from core.order_processing import order_manager
from core.autotrading.basic_options import ALGO_SHORT_HIT_BASIC_OPTION
from core.global_state import UseGlobal

class ShortHit(UseGlobal):
    update = Signal(str, dict)
    
    def __init__(self, acc):
        UseGlobal.__init__(self)
        self.acc = acc
        
        self.api = API()
        
    def updateStates(self, key="", extra={}):
        
        if key == f"{self.acc.accno}$short_hit":
            try:
                stockcode = extra["stockcode"]
                one_timer_amount = self.order["one_time_amount"]
                buy_same_stock = self.order["buy_same_stock"]
                order_type = self.order["order_type"]
            except KeyError as e:
                logger.error(f"{self.acc.accno} algorithm option not correct: {e}")
                return
            
            stockobj = self.api.getStockObj(stockcode)
            
                
            if order_type == "market_price":
                
                
                order_manager.buyStockNow
    
    def setOption(self, option={}):
        
        # Update options
        self.condition = option.get("condition", ALGO_SHORT_HIT_BASIC_OPTION["condition"])
        self.max_stock_cnt = option.get("max_stock_cnt", ALGO_SHORT_HIT_BASIC_OPTION["max_stock_cnt"])
        self.just_today = option.get("just_today", ALGO_SHORT_HIT_BASIC_OPTION["just_today"])
        self.order = option.get("order", ALGO_SHORT_HIT_BASIC_OPTION["order"])
        
    def start(self):
        
        self.stateReg()
        self.updateStates()
        
        cond_manager.regCondReal(f"{self.acc.accno}$short_hit", [self.condition], self.orderCallback)
        
    def condRealCallback(self, seed, stockcode, tag, condname, cidx):

        if tag == "I":
            # Already holding => ignore
            if self.acc.isHoldings(stockcode):
                return
            
            self.gstate.callUpdate(seed, extra={
                "stockcode": stockcode
            })
            
            