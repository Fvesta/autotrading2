from core.autotrading.basic_options import TRADING_BASIC_OPTION
from core.autotrading.trailingstop import TrailingStop


class Trading:
    def __init__(self, acc):
        self.acc = acc
        
        self.trailing_stop = TrailingStop(self.acc)
        self.option = TRADING_BASIC_OPTION
        
    def start(self):
        
        # Trailing Stop
        trailing_stop_option = self.option.get("trailing_stop")
        
        if trailing_stop_option and trailing_stop_option.get("used"):
            self.trailing_stop.setOption(trailing_stop_option.get("option"))
            self.trailing_stop.start()
            