from PySide2.QtCore import Signal, QObject

from core.logger import logger
from core.api import API
from core.condition import cond_manager
from core.order_processing import order_manager
from core.autotrading.basic_options import ALGO_SHORT_HIT_BASIC_OPTION
from core.global_state import UseGlobal
from core.utils.stock_util import getRegStock

class ShortHit(QObject, UseGlobal):
    update = Signal(str, dict)
    
    def __init__(self, acc):
        QObject.__init__(self)
        UseGlobal.__init__(self)
        self.acc = acc
        
        self.api = API()
        
    def updateStates(self, key="", extra={}):
        
        if key == f"{self.acc.accno}$short_hit":
            try:
                stockcode = extra["stockcode"]
                one_time_amount = self.order["one_time_amount"]
                buy_same_stock = self.order["buy_same_stock"]
                order_type = self.order["order_type"]
            
            except KeyError as e:
                logger.error(f"{self.acc.accno} algorithm option not correct: {e}")
                return                     
            
            if not buy_same_stock:
                # Stockcode repeat => ignore
                for log in self.acc.real_exec_log:
                    if log["stockcode"] == stockcode and log["exec_gubun"] == "매수":
                        return 
            
            # If there is no money to buy, set one_time_amount to limit amount
            if self.acc.rest_amount < one_time_amount:
                one_time_amount = self.acc.rest_amount
            
            stockobj = self.api.getStockObj(stockcode)
            stockobj.reqStockInfo()
            cur_price = stockobj.cur_price
            
            try:
                quantity = int(one_time_amount / cur_price)
            except TypeError as e:
                logger.error(e)
                return
            except ZeroDivisionError as e:
                logger.error(e)
                return
                
            if order_type == "market_price":
                order_manager.buyStockNow(self.acc.accno, stockcode, quantity)
    
    def eventReg(self):
        self.update.connect(self.updateStates)
        
    def eventTerm(self):
        self.update.disconnect(self.updateStates)
    
    def setOption(self, option={}):
        
        # Update options
        self.condition = option.get("condition", ALGO_SHORT_HIT_BASIC_OPTION["condition"])
        self.max_stock_cnt = option.get("max_stock_cnt", ALGO_SHORT_HIT_BASIC_OPTION["max_stock_cnt"])
        self.just_today = option.get("just_today", ALGO_SHORT_HIT_BASIC_OPTION["just_today"])
        self.order = option.get("order", ALGO_SHORT_HIT_BASIC_OPTION["order"])
        
    def start(self):
        
        self.stateReg()
        self.updateStates()
        self.eventReg()
        
        cond_manager.regCondReal(f"{self.acc.accno}$short_hit", [self.condition], self.condRealCallback)
        
    def stop(self):
        
        self.eventTerm()
        self.stateTerm()
        cond_manager.termCondReal(f"{self.acc.accno}$short_hit")
        
    def condRealCallback(self, seed, stockcode, tag, condname, cidx):

        if tag == "I":
            try:
                stockcode = getRegStock(stockcode)
            except:
                logger.debug("There is not stockcode")
            
            # Already holding => ignore
            if self.acc.isHoldings(stockcode):
                return
            
            # If already 10 stocks => ignore
            if len(self.acc.holdings.keys()) >= self.max_stock_cnt:
                return
            
            self.update.emit(seed, {
                "stockcode": stockcode
            })
