from datetime import datetime, time, timedelta
from PySide2.QtCore import Signal, Qt
from PySide2.QtWidgets import *

from core import logger
from core.account import Account
from core.utils.type_util import absIntOrZero, floatOrZero, intOrZero
from core.utils.utils import getAccnoFromObj
from core.errors import ErrorCode
from core.api import API
from style.utils import setTableSizeSameHor
from style.colors import decimal_colors
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
        
        self.exec_logs = []
        
        self.initSetting()
        
    def initSetting(self):
        self.ui.setWindowTitle(f"거래내역: {self.accno}")
        
        self.ui.balance_log_label.setProperty("class", "tx-bold")
        self.ui.exec_log_label.setProperty("class", "tx-bold")
        
        # Set header color
        balance_horizontal_headers = [self.ui.balance_log_table.horizontalHeaderItem(i) for i in range(self.ui.balance_log_table.columnCount())]
        exec_horizontal_headers = [self.ui.exec_log_table.horizontalHeaderItem(i) for i in range(self.ui.exec_log_table.columnCount())]
        
        for col, header in enumerate(balance_horizontal_headers):
            if col == 1 or col == 2 or col == 3:
                header.setForeground(decimal_colors["QT_RED"])
            elif col == 4 or col == 5 or col == 6:
                header.setForeground(decimal_colors["QTMATERIAL_PRIMARYCOLOR"])
            else:
                header.setForeground(decimal_colors["QT_DARKWHITE"])
        
        for header in exec_horizontal_headers:
            header.setForeground(decimal_colors["QT_DARKWHITE"])
        
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
        self.ui.balance_log_table.itemSelectionChanged.connect(self.selectStock)
        
    def eventTerm(self):
        self.update.disconnect(self.updateStates)
        self.ui.lookup_btn.clicked.disconnect(self.getTodayInfo)
        self.ui.balance_log_table.itemSelectionChanged.disconnect(self.selectStock)
        
    @showModal
    def show(self):
        
        self.stateReg()
        self.updateStates()
        self.eventReg()
        
    def selectStock(self):
        selected_items = self.ui.balance_log_table.selectedItems()
        
        try:
            find_name = selected_items[0].text()
            
            self.setExecLogData(find_name)
        except KeyError:
            logger.warning("No selected item")
            
    def getTodayInfo(self):
        # Balance log
        self.setBalanceLogData()
        
        # Exec log
        self.getExecLogData()
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
        today_income = intOrZero(single_data.get("총손익금액"))
        
        self.ui.sell_label.setText(f"{'총매도금액:':<10}{today_sell_amount:,}")
        self.ui.buy_label.setText(f"{'총매수금액:':<10}{today_buy_amount:,}")
        self.ui.tax_label.setText(f"{'수수료/세금:':<10}{today_total_tax_fee:,}")
        self.ui.income_label.setText(f"{'손익금액:':<10}{today_income:+,}")
        
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
                f"{today_average_buy_price:,}",
                f"{today_buy_quantity}",
                f"{today_buy_amount:,}",
                f"{today_average_sell_price:,}",
                f"{today_sell_quantity}",
                f"{today_sell_amount:,}",
                f"{today_tax_fee:,}",
                f"{today_income:+,}",
                f"{today_income_rate:+}%"
            ))
            
        acc: Account = self.api.getAccObj(self.accno)
        
        self.ui.diff_label.setText(f"{'매수종목수:':<10}{len(acc.today_buy_stocks)}")
        self.ui.count_label.setText(f"{'매도종목수:':<10}{total_stock_count}")
        
        for i in range(len(tb_data)):
            for j in range(len(tb_data[0])):
                
                # 실현손익, 손익율
                if j == 8 or j == 9:
                    item = QTableWidgetItem(str(tb_data[i][j]))
                    item.setTextAlignment(Qt.AlignCenter)
                    
                    data_formatted = tb_data[i][j]
                    if data_formatted[0] == "+":
                        item.setForeground(decimal_colors["QT_RED"])
                    else:
                        item.setForeground(decimal_colors["QTMATERIAL_PRIMARYCOLOR"])
                    
                    self.ui.balance_log_table.setItem(i, j, item)
                
                else:
                    item = QTableWidgetItem(str(tb_data[i][j]))
                    item.setTextAlignment(Qt.AlignCenter)
            
                    self.ui.balance_log_table.setItem(i, j, item)
            
    def getExecLogData(self):
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
        req_date = now.strftime("%Y%m%d")
        
        # 00:00:00
        start_time = time(0, 0, 0)
        # 05:00:00
        end_time = time(5, 0, 0)
        
        cur_time = now.time()
        
        if start_time <= cur_time <= end_time:
            yesterday = now - timedelta(days=1)
            req_date = yesterday.strftime("%Y%m%d")
        
        trade_log = self.api.sendTr("계좌별주문체결내역상세요청", [req_date, self.accno, "", "00", 1, 1, 0, "", ""])
        
        multi_merged_data = trade_log.get("multi")
        next = trade_log.get("next")
        
        while(next == "2"):
            trade_log = self.api.sendTr("계좌별주문체결내역상세요청", [req_date, self.accno, "", "00", 1, 1, 0, "", ""], True)

            multi_data = trade_log.get("multi")
            next = trade_log.get("next")
            
            multi_merged_data.extend(multi_data)
        
        self.exec_logs = multi_merged_data 
    
    def setExecLogData(self, stockname=None):
        find_name = stockname
        
        tb_data = []
        for data in self.exec_logs:
            
            stockname = data.get("종목명")
            
            if stockname == "":
                continue
            
            if (find_name != None) and (stockname != find_name):
                continue

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
            exec_price = intOrZero(data.get("체결단가"))
            exec_quantity = intOrZero(data.get("체결수량"))
            exec_amount = exec_price * exec_quantity
            nc_quantity = intOrZero(data.get("주문잔량"))
            
            origin_orderno = data.get("원주문")
            if origin_orderno == "0000000":
                origin_orderno = ""
            
            order_time = data.get("주문시간")
            
            tb_data.append((
                orderno,
                stockname,
                exec_gubun,
                f"{order_price:,}",
                f"{order_quantity}",
                f"{exec_price:,}",
                f"{exec_quantity}",
                f"{exec_amount:,}",
                f"{nc_quantity}",
                origin_orderno,
                order_time
            ))
        
        self.ui.exec_log_table.setRowCount(len(tb_data))
        for i in range(len(tb_data)):
            for j in range(len(tb_data[0])):
                item = QTableWidgetItem(str(tb_data[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
        
                self.ui.exec_log_table.setItem(i, j, item)   