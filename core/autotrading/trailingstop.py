from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from core.autotrading.basic_options import TRAILING_STOP_BASIC_OPTION


class TrailingStop:
    def __init__(self, acc):
        self.acc = acc
        self.standard = "each"
        
        self.trailingScheduler = BackgroundScheduler(timezone="Asia/Seoul")

        self.setOption()
    
    def setOption(self, option={}):
        if option == None:
            return
        
        # Update options
        self.standard = option.get("standard", TRAILING_STOP_BASIC_OPTION["standard"])
        self.tick = option.get("tick", TRAILING_STOP_BASIC_OPTION["tick"])
        self.lines = option.get("lines", TRAILING_STOP_BASIC_OPTION["lines"])
        self.division = option.get("division", TRAILING_STOP_BASIC_OPTION["division"])
        
        # Update tick, modify of add job
        job = self.trailingScheduler.get_job("trailingAlgo")
        ticktype = self.tick.get("type", "seconds")
        tickval = self.tick.get("val", 30)
        
        if job:
            if ticktype == "seconds":
                job.modify(trigger=IntervalTrigger(seconds=tickval))
            elif ticktype == "minutes":
                job.modify(trigger=IntervalTrigger(minutes=tickval))
        
        else:
            if ticktype == "seconds":
                self.trailingScheduler.add_job(self.trailingAlgo, "interval", id="trailingAlgo", seconds=tickval)
            if ticktype == "minutes":
                self.trailingScheduler.add_job(self.trailingAlgo, "interval", id="trailingAlgo", minutes=tickval)
    
    def trailingAlgo(self):
        print(datetime.now())
    
    def start(self):
        
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
            
        self.trailingScheduler.modify_job('trailingAlgo', next_run_time=next_run)
        
        # Start scheduler
        if self.trailingScheduler.running:
            self.trailingScheduler.resume("trailingAlgo")
        else:
            self.trailingScheduler.start()
        
    def stop(self):
        
        self.trailingScheduler.pause_job("trailingAlgo")
        