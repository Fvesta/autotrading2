from core.utils.type_util import absIntOrZero, floatOrZero
from core.utils.utils import intOrZero


class Stock:
    def __init__(self, stockcode, stockname):
        self.stockcode = stockcode
        self.name = stockname
        self.cur_price = 0              # 현재가
        self.today_updown_rate = 0      # 등락률
        self.today_trans_amount = 0     # 거래대금 
        self.buy_rate = 0               # 매수비율
        self.chart = {}
    
    # cur_price, today_updown_rate, today_trans_amount, buy_rate    
    def setStockInfo(self, data):
        
        cur_price = data.get("cur_price")
        if cur_price is not None:
            self.cur_price = absIntOrZero(cur_price)
            
        today_updown_rate = data.get("today_updown_rate")
        if today_updown_rate is not None:
            self.today_updown_rate = floatOrZero(today_updown_rate)
            
        today_trans_amount = data.get("today_trans_amount")
        if today_trans_amount is not None:
            self.today_trans_amount = absIntOrZero(today_trans_amount)
        
        buy_rate = data.get("buy_rate")
        if buy_rate is not None:
            self.buy_rate = buy_rate
            