class Stock:
    def __init__(self, stockcode, stockname):
        self.stockcode = stockcode
        self.name = stockname
        self.cur_price = None           # 현재가
        self.today_updown_rate = 0      # 등락률
        self.today_trans_amount = 0     # 거래대금 
        self.buy_rate = 0               # 매수비율
        self.chart = {}