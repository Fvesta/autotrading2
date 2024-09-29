from apscheduler.schedulers.background import BackgroundScheduler

from core.autotrading.stoploss import StopLoss
from core.errors import ErrorCode
from core.logger import logger
from core.autotrading.basic_options import TRADING_BASIC_OPTION
from core.autotrading.short_hit import ShortHit
from core.autotrading.trailingstop import TrailingStop


class Trading:
    def __init__(self, acc):
        self.acc = acc
        
        self.running = False
        self.scheduler = BackgroundScheduler(timezone="Asia/Seoul")
        self.option = None
        
        # Trailing stop
        self.trailing_stop = TrailingStop(self.acc, self.scheduler)
        
        # Stop loss
        self.stop_loss = StopLoss(self.acc)
        
        # Base algorithm
        self.algorithm_dict = {
            "short_hit": ShortHit(self.acc)
        }
        self.algo = None
        
    def setOption(self, option=TRADING_BASIC_OPTION):
        self.option = option
        
        # Get options
        option_trailing_stop = self.option.get("trailing_stop")
        option_stop_loss = self.option.get("stop_loss")
        option_base_algorithm = self.option.get("base_algorithm")
        
        # Trailing stop
        if option_trailing_stop and option_trailing_stop.get("used"):
            self.trailing_stop.setOption(True, option_trailing_stop.get("option", {}))
        else:
            self.trailing_stop.setOption(False)
        
        # Stop loss
        if option_stop_loss and option_stop_loss.get("used"):
            self.stop_loss.setOption(True, option_stop_loss.get("option", {}))
        else:
            self.stop_loss.setOption(False)
        
        # Base Algorithm
        try:
            self.algo = option_base_algorithm["algo"]
        except KeyError:
            logger.error("Not correct algorithm")
            return ErrorCode.OP_INPUT_ERROR
        
        if self.algo == "short_hit":
            self.algorithm_dict[self.algo].setOption(option_base_algorithm.get("option", {}))
        
         
    def start(self):
              
        # Trailing stop setting
        if self.trailing_stop.used:
            self.trailing_stop.calcStartTime()
            
        # Base algorithm
        if self.algo == "short_hit":
            algo_obj = self.algorithm_dict[self.algo]
            algo_obj.start()
            
        # Stop loss
        if self.stop_loss.used:
            self.stop_loss.start()
                   
        # # Start scheduler
        # if self.scheduler.running:
        #     # for job in self.scheduler.get_jobs():
        #     #     self.scheduler.resume(job.id)
        #     self.scheduler.resume()
        # else:
        #     self.scheduler.start()
        
        self.running = True          
            
    def stop(self):
        if self.stop_loss.used:
            self.stop_loss.stop()
            
        if self.algo == "short_hit":
            algo_obj = self.algorithm_dict[self.algo]
            algo_obj.stop()
            
        # self.scheduler.pause()
        self.running = False