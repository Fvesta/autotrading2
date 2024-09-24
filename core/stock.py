from core.logger import logger
from core.api import API
from core.errors import ErrorCode
from core.utils.type_util import absIntOrZero, floatOrZero
from core.utils.utils import intOrZero


class Stock:
    def __init__(self, stockcode, stockname):
        self.stockcode = stockcode
        self.name = stockname
        self.cur_price = 0              # 현재가
        self.today_updown_rate = 0      # 등락률
        self.today_trans_count = 0     # 거래량 
        self.buy_rate = 0               # 매수비율
        self.chart = {}
        
        self.api = API()
    
    # cur_price, today_updown_rate, today_trans_count, buy_rate    
    def setStockInfo(self, data):
        
        cur_price = data.get("cur_price")
        if cur_price is not None:
            self.cur_price = absIntOrZero(cur_price)
            
        today_updown_rate = data.get("today_updown_rate")
        if today_updown_rate is not None:
            self.today_updown_rate = floatOrZero(today_updown_rate)
            
        today_trans_count = data.get("today_trans_count")
        if today_trans_count is not None:
            self.today_trans_count = absIntOrZero(today_trans_count)
        
        buy_rate = data.get("buy_rate")
        if buy_rate is not None:
            self.buy_rate = buy_rate
            
    def reqStockInfo(self):
        stock_info = self.api.sendTr("주식기본정보요청", [self.stockcode])
        
        if isinstance(stock_info, ErrorCode):
            logger.warning("Can\'t load stock info")
            
        single_data = stock_info.get("single")
        
        cur_price = single_data.get("현재가")
        today_updown_rate = single_data.get("등락율")
        today_trans_count = single_data.get("거래량")
        
        self.setStockInfo({
            "cur_price": cur_price,
            "today_updown_rate": today_updown_rate,
            "today_trans_count": today_trans_count
        })
            