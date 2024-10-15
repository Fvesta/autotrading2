from datetime import datetime
from PySide2.QtCore import Signal, Qt
from PySide2.QtWidgets import *

from core import logger
from core.account import Account
from core.utils.stock_util import getRegStock
from core.utils.type_util import absIntOrZero, floatOrZero, intOrZero
from core.utils.utils import getAccnoFromObj
from core.errors import ErrorCode
from core.api import API
from core.order_processing import order_manager
from style.utils import setTableSizeSameHor
from windows.win_abs import WindowAbs, showModal

class TradeLogWin(WindowAbs):
    update = Signal(str, dict)
    
    def __init__(self, name, ui_path, css_path):
        WindowAbs.__init__(self, name, ui_path, css_path)
        accno = getAccnoFromObj(name)
        
        if isinstance(accno, ErrorCode):
            return
        
        self.accno = accno
        self.api = API()
        
        self.initSetting()
        
    def initSetting(self):
        self.ui.setWindowTitle(f"거래내역: {self.accno}")
        self.ui.sell_label.setProperty("class", "tx-12")
        self.ui.buy_label.setProperty("class", "tx-12")
        self.ui.tax_label.setProperty("class", "tx-12")
        self.ui.diff_label.setProperty("class", "tx-12")
        self.ui.income_label.setProperty("class", "tx-12")
        self.ui.count_label.setProperty("class", "tx-12")
        
    def afterSetting(self):
        self.updateStyle()
        
        balance_log_table = self.ui.balance_log_table
        exec_log_table = self.ui.exec_log_table
        
        setTableSizeSameHor(balance_log_table)
        setTableSizeSameHor(exec_log_table)
        
    def updateStates(self, key="", extra={}):
        pass
    
    def eventReg(self):
        self.update.connect(self.updateStates)
        self.ui.lookup_btn.clicked.connect(self.getTodayInfo)
        
    def eventTerm(self):
        self.update.disconnect(self.updateStates)
        self.ui.lookup_btn.clicked.disconnect(self.getTodayInfo)
        
    @showModal
    def show(self):
        
        self.stateReg()
        self.updateStates()
        self.eventReg()
        
    def getTodayInfo(self):
        # Balance log
        self.setBalanceLogData()
        
        # Exec log
        self.setExecLogData()
    
    def setBalanceLogData(self):
        # 종목이름
        # 매수평균가
        # 매수수량
        # 매수금액
        # 매도평균가
        # 매도수량
        # 매도금액
        # 세금,수수료
        # 실현손익
        # 손익율
        
        today_trade_log = self.api.sendTr("당일매매일지요청", [self.accno, "", "", None, None])
        
        single_data = today_trade_log.get("single")
        multi_data = today_trade_log.get("multi")
        
        today_sell_amount = absIntOrZero(single_data.get("총매도금액"))
        today_buy_amount = absIntOrZero(single_data.get("총매수금액"))
        today_total_tax_fee = intOrZero(single_data.get("총수수료_세금"))
        today_diff = intOrZero(single_data.get("총정산금액"))
        today_income = intOrZero(single_data.get("총손익금액"))
        
        self.ui.sell_label.setText(f"총매도금액:    {today_sell_amount:,}")
        self.ui.buy_label.setText(f"총매수금액:    {today_buy_amount:,}")
        self.ui.tax_label.setText(f"수수료/세금:    {today_total_tax_fee:,}")
        self.ui.diff_label.setText(f"정산금액:    {today_diff:+,}")
        self.ui.income_label.setText(f"실현손익:    {today_income:+,}")
        
        tb_data = []
        self.ui.balance_log_table.setRowCount(len(multi_data))
        total_stock_count = 0
        for data in multi_data:
            
            stockname = data.get("종목명")
            
            if stockname == "":
                continue
            
            total_stock_count += 1
            
            today_average_buy_price = absIntOrZero(data.get("매수평균가"))
            today_buy_quantity = absIntOrZero(data.get("매수수량"))  
            today_buy_amount = absIntOrZero(data.get("매수금액"))
            today_average_sell_price = absIntOrZero(data.get("매도평균가"))
            today_sell_quantity = absIntOrZero(data.get("매도수량"))
            today_sell_amount = absIntOrZero(data.get("매도금액"))
            today_tax_fee = intOrZero(data.get("수수료_제세금"))
            today_income = intOrZero(data.get("손익금액"))
            today_income_rate = floatOrZero(data.get("수익률"))
            
            tb_data.append((
                stockname,
                today_average_buy_price,
                today_buy_quantity,
                today_buy_amount,
                today_average_sell_price,
                today_sell_quantity,
                today_sell_amount,
                today_tax_fee,
                today_income,
                today_income_rate
            ))
            
        self.ui.count_label.setText(f"매도종목수:    {total_stock_count}")
        
        for i in range(len(tb_data)):
            for j in range(len(tb_data[0])):
                item = QTableWidgetItem(str(tb_data[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
        
                self.ui.balance_log_table.setItem(i, j, item)
            
    def setExecLogData(self):
        # 주문번호
        # 종목이름
        # 구분
        # 주문가격
        # 주문수량
        # 체결가격
        # 체결수량
        # 체결금액
        # 미체결
        # 원주문번호
        # 주문시간
        now = datetime.now()
        today_date = now.strftime("%Y%m%d")
        
        trade_log = self.api.sendTr("계좌별주문체결내역상세요청", [today_date, self.accno, "", "00", 1, 1, 0, "", ""])
        
        multi_merged_data = trade_log.get("multi")
        next = trade_log.get("next")
        
        while(next == "2"):
            trade_log = self.api.sendTr("계좌별주문체결내역상세요청", [today_date, self.accno, "", "00", 1, 1, 0, "", ""], True)

            multi_data = trade_log.get("multi")
            next = trade_log.get("next")
            
            multi_merged_data.extend(multi_data)
            
        tb_data = []
        self.ui.exec_log_table.setRowCount(len(multi_merged_data))
        for data in multi_merged_data:
            
            stockname = data.get("종목명")

            order_gubun = data.get("주문구분")
            fix_cancel = data.get("정정취소")
            exec_gubun = ""
            if order_gubun == "현금매수":
                exec_gubun = "매수"
                if fix_cancel == "정정":
                    exec_gubun = "매수정정"
                elif fix_cancel == "취소":
                    exec_gubun = "매수취소"
            elif order_gubun == "현금매도":
                exec_gubun = "매도"
                if fix_cancel == "정정":
                    exec_gubun = "매도정정"
                elif fix_cancel == "취소":
                    exec_gubun = "매도취소"
            
            orderno = data.get("주문번호")
            order_price = intOrZero(data.get("주문단가"))
            order_quantity = intOrZero(data.get("주문수량"))
            order_amount = order_price * order_quantity
            exec_price = intOrZero(data.get("체결단가"))
            exec_quantity = intOrZero(data.get("체결수량"))
            exec_amount = exec_price * exec_quantity
            nc_quantity = intOrZero(data.get("주문잔량"))
            origin_orderno = data.get("원주문")
            order_time = data.get("주문시간")
            
            tb_data.append((orderno, stockname, exec_gubun, order_price, order_quantity, exec_price, exec_quantity, exec_amount, nc_quantity, origin_orderno, order_time))
        
        for i in range(len(tb_data)):
            for j in range(len(tb_data[0])):
                item = QTableWidgetItem(str(tb_data[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
        
                self.ui.exec_log_table.setItem(i, j, item)    
                