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
    
    def __init__(self, acc, scheduler):
        QObject.__init__(self)
        UseGlobal.__init__(self)
        self.acc = acc
        self.scheduler = scheduler
        
        self.api = API()
        self.jobid = "short_hit"
        
    def updateStates(self, key="", extra={}):
        
        if key == "sell_all":
            holdings = dict(self.acc.holdings)
        
            for stockcode in holdings.keys():
                holding_info = holdings[stockcode]
                
                quantity = holding_info.possible_quantity
                
                order_manager.sellStockNow(self.acc.accno, stockcode, quantity)
        
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
                # If today buy => ignore
                if stockcode in self.acc.today_buy_stocks:
                    return 
                
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
        self.today_max_cnt = option.get("today_max_cnt", ALGO_SHORT_HIT_BASIC_OPTION["today_max_cnt"])
        self.max_bal_cnt = option.get("max_bal_cnt", ALGO_SHORT_HIT_BASIC_OPTION["max_bal_cnt"])
        self.just_today = option.get("just_today", ALGO_SHORT_HIT_BASIC_OPTION["just_today"])
        self.order = option.get("order", ALGO_SHORT_HIT_BASIC_OPTION["order"])
        
    def start(self):
        
        self.stateReg()
        self.updateStates()
        self.eventReg()
        
        if self.just_today:
            self.scheduler.add_job(self.sellCall, "cron", day_of_week="mon-fri", id=self.jobid, hour=15, minute=25)
        
        cond_manager.regCondReal(f"{self.acc.accno}$short_hit", [self.condition], self.condRealCallback)
        
    def stop(self):
        
        self.eventTerm()
        self.stateTerm()
        
        if self.just_today:
            self.scheduler.remove_job(self.jobid)
        
        cond_manager.termCondReal(f"{self.acc.accno}$short_hit")
        
    def sellCall(self):
       self.update.emit("sell_all", {})
        
    def condRealCallback(self, seed, stockcode, tag, condname, cidx):

        if tag == "I":
            stockcode = getRegStock(stockcode)
            
            # Already holding => ignore
            if self.acc.isHoldings(stockcode):
                return
            
            # If already max cnt exceed
            if len(self.acc.today_buy_stocks) >= self.today_max_cnt:
                return
            
            # If already 10 stocks => ignore
            if len(self.acc.holdings.keys()) >= self.max_bal_cnt:
                return
            
            # If stock is already buy ordered, not completed => ignore
            not_completed_orderno_list = list(self.acc.not_completed_order.keys())
            
            for orderno in not_completed_orderno_list:
                order_info = self.acc.not_completed_order[orderno]
            
                nc_stockcode = order_info["stockcode"]
                nc_stockcode = getRegStock(stockcode)
                
                order_gubun = order_info["order_gubun"]
                
                if nc_stockcode == stockcode and order_gubun == "매수":
                    return
                
            self.update.emit(seed, {
                "stockcode": stockcode
            })
