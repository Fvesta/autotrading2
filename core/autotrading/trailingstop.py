from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from copy import deepcopy

from core.api import API
from core.autotrading.basic_options import TRAILING_STOP_BASIC_OPTION
from core.real_processing import real_manager


class TrailingStop:
    def __init__(self, acc, scheduler):
        self.acc = acc
        self.scheduler = scheduler
        
        self.api = API()
        self.jobid = "trailing_algo"
        self.used = False
        
        # Algo states
        self.prev_info = {}
    
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
        self.lines = option.get("lines", TRAILING_STOP_BASIC_OPTION["lines"])
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
        cur_holdings = deepcopy(self.acc.holdings)
        
        next_prev_info = {}
        for stockcode, holding_info in cur_holdings.items():
            
            # Set prevholdings info
            next_prev_info[stockcode] = {
                "average_buyprice": holding_info.average_buyprice,
                "income_rate": holding_info.incomeRate()
            }
            
            # If stockcode not in prev holdings => ignore
            if stockcode not in self.prev_info:
                continue
            
            # Decide trailing or not
            
            prev_average_buyprice = self.prev_info.get("average_buyprice")
            prev_income_rate = self.prev_info.get("imcome_rate")
            
            curobj = self.api.getStockObj(stockcode)
            
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
        
    def stop(self):
        
        self.scheduler.pause_job(self.jobid)
        