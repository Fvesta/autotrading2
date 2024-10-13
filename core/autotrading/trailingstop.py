import math
from PySide2.QtCore import Signal, QObject

from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from core.logger import logger
from core.api import API
from core.autotrading.basic_options import TRAILING_STOP_BASIC_OPTION
from core.global_state import UseGlobal
from core.order_processing import order_manager


class TrailingStop(QObject, UseGlobal):
    update = Signal(str, dict)
    
    def __init__(self, acc, scheduler):
        QObject.__init__(self)
        UseGlobal.__init__(self)
        self.acc = acc
        self.scheduler = scheduler
        
        self.api = API()
        self.jobid = "trailing_algo"
        self.used = False
        
        # Algo states
        self.prev_info = {}
        
        self.observe_condition = {}
        
    def updateStates(self, key="", extra={}):
        # If balance updated
        if key == f"{self.acc.accno}$balance":
            cur_holdings = dict(self.acc.holdings)
            
            # If new stock is added, add sell conditions
            for stockcode in cur_holdings.keys():
                if stockcode not in self.observe_condition:
                    self.observe_condition[stockcode] = list(self.division)
                    
            # If There are conditions of stockcode, but is not holdings => delete conditions
            observed_stocks_set = set(list(self.observe_condition.keys()))
            holding_stocks_set = set(list(cur_holdings.keys()))
            
            ignore_stocks_set = observed_stocks_set - holding_stocks_set
            for stockcode in ignore_stocks_set:
                del self.observe_condition[stockcode]
        
        if key == "trailing_sell":
            stockcode = extra.get("stockcode")
            sell_percent = extra.get("sell_percent")
            
            if self.acc.isHoldings(stockcode):
                holding_info = self.acc.holdings[stockcode]
                
                # Calculate quantity
                total_quantity = holding_info.quantity
                sell_quantity = math.ceil(total_quantity * (sell_percent) / 100)
                
                order_manager.sellStockNow(self.acc.accno, stockcode, sell_quantity)
    
    def eventReg(self):
        self.update.connect(self.updateStates)
        
    def eventTerm(self):
        self.update.disconnect(self.updateStates)
    
    def setOption(self, used, option={}):
        self.used = used
        
        job = self.scheduler.get_job(self.jobid)
        
        if not self.used:
            # If job exist, remove
            if job:
                self.scheduler.remove_job(job.id)
            return
        
        # Update options
        self.standard = option.get("standard", TRAILING_STOP_BASIC_OPTION["standard"])
        self.tick = option.get("tick", TRAILING_STOP_BASIC_OPTION["tick"])
        self.line_opt = option.get("line_opt", TRAILING_STOP_BASIC_OPTION["line_opt"])
        self.division = option.get("division", TRAILING_STOP_BASIC_OPTION["division"])
        
        # Update tick, modify of add job
        ticktype = self.tick.get("type", "seconds")
        tickval = self.tick.get("val", 30)
        
        if job:
            if ticktype == "seconds":
                job.modify(trigger=IntervalTrigger(seconds=tickval))
            elif ticktype == "minutes":
                job.modify(trigger=IntervalTrigger(minutes=tickval))
        
        else:
            if ticktype == "seconds":
                self.scheduler.add_job(self.trailingAlgo, "interval", id=self.jobid, seconds=tickval)
            if ticktype == "minutes":
                self.scheduler.add_job(self.trailingAlgo, "interval", id=self.jobid, minutes=tickval)
    
    def trailingAlgo(self):
        cur_holdings = dict(self.acc.holdings)
        
        next_prev_info = {}
        for stockcode, holding_info in cur_holdings.items():
            
            cur_average_buyprice = holding_info.average_buyprice
            cur_income_rate = holding_info.getIncomeRate()
            
            # Set prevholdings info
            next_prev_info[stockcode] = {
                "average_buyprice": cur_average_buyprice,
                "income_rate": cur_income_rate,
            }
            
            # If stockcode not in prev holdings => ignore
            if stockcode not in self.prev_info:
                continue
            
            # Decide trailing or not
            stock_prev_info = self.prev_info[stockcode]
            
            prev_average_buyprice = stock_prev_info.get("average_buyprice")
            prev_income_rate = stock_prev_info.get("income_rate")
            
            # If balance is changed in time, ignore
            if prev_average_buyprice != cur_average_buyprice:
                continue
            
            # if prev is up, cur is down, operating
            line_type = self.line_opt.get("type")
            lines = []
            if line_type == "manual":
                lines = list(self.line_opt.get("lines"))
            elif line_type == "auto":
                pass
            
            prev_line = -101
            cur_line = -101
            for line in lines:
                if prev_income_rate >= line: 
                    prev_line = line
                if cur_income_rate >= line:
                    cur_line = line
            
            # stop
            if prev_line > cur_line:
                conditions = self.observe_condition[stockcode]
                try:
                    cur_condition = conditions[0]
                    new_observe_condition = conditions[1:]
                    
                    sell_percent = cur_condition["sell_percent"]
                               
                    self.update.emit("trailing_sell", {
                        "stockcode": stockcode,
                        "sell_percent": sell_percent
                    })
                    
                    self.observe_condition[stockcode] = new_observe_condition
                except KeyError:
                    logger.error(f"There is no other condition in stock: {stockcode}")
            
        self.prev_info = next_prev_info
            
    def calcStartTime(self):
        
        # Set next run time
        ticktype = self.tick.get("type", "seconds")
        tickval = self.tick.get("val", 30)
        
        next_run = datetime.now()
        if ticktype == "seconds":
            now = datetime.now()
            rest = tickval - now.second % tickval

            next_run = now + timedelta(seconds=rest) - timedelta(seconds=1)
        elif ticktype == "minutes":
            now = datetime.now()
            rest = tickval - now.minute % tickval
            
            next_run = now - timedelta(seconds=now.second) + timedelta(minutes=rest) - timedelta(seconds=1)
        
        # Init setting
        self.prev_info = {}
        self.scheduler.modify_job(self.jobid, next_run_time=next_run)
        
    def start(self):
        self.stateReg()
        self.updateStates()
        self.eventReg()
        
        self.calcStartTime()
        
        # Set default sell conditions
        observe_condition = {}
        cur_holdings = dict(self.acc.holdings)
        for stockcode in cur_holdings.keys():
            if stockcode in self.observe_condition:
                observe_condition[stockcode] = self.observe_condition[stockcode]
                continue
            
            observe_condition[stockcode] = list(self.division)
            
        self.observe_condition = observe_condition
        
        self.scheduler.resume_job(self.jobid)
        
    def stop(self):
        self.eventTerm()
        self.stateTerm()
        
        self.scheduler.pause_job(self.jobid)
        