from PySide2.QtCore import SIGNAL, QObject
from PySide2.QtAxContainer import QAxWidget

from core.account import holdingInfo
from core.errors import StockNotFoundException
from core.logger import logger
from core.constants import TR_RETURN_MAP
from core.scr_manager import scr_manager
from core.real_processing import real_manager
from core.condition import Condition, cond_manager
from core.order_processing import order_manager
from core.api import API
from core.global_state import UseGlobal
from core.stock import Stock
from core.utils.type_util import intOrZero
from core.utils.utils import isStock, getRegStock

signal_map = {
    "OnEventConnect": SIGNAL("OnEventConnect(int)"),
    "OnReceiveTrData": SIGNAL("OnReceiveTrData(QString, QString, QString, QString, QString, int, QString, QString, QString)"),
    "OnReceiveRealData": SIGNAL("OnReceiveRealData(QString, QString, QString)"),
    "OnReceiveConditionVer": SIGNAL("OnReceiveConditionVer(int, QString)"),
    "OnReceiveTrCondition": SIGNAL("OnReceiveTrCondition(QString, QString, QString, int, int)"),
    "OnReceiveRealCondition": SIGNAL("OnReceiveRealCondition(QString, QString, QString, QString)"),
    "OnReceiveMsg": SIGNAL("OnReceiveMsg(QString, QString, QString, QString)"),
    "OnReceiveChejanData": SIGNAL("OnReceiveChejanData(QString, int, QString)")
}

class CallbackHandler(UseGlobal, QObject):
    def __init__(self):
        QObject.__init__(self)
        UseGlobal.__init__(self)
        self.api = API()
        self.ocx: QAxWidget = self.api.ocx
        
    def watch(self):
        self.eventReg()
        
    def eventReg(self):
        self.ocx.connect(signal_map["OnEventConnect"], self.loginCallback)
        self.ocx.connect(signal_map["OnReceiveConditionVer"], self.loadCondCallback)
        self.ocx.connect(signal_map["OnReceiveTrCondition"], self.condTrCallback)
        self.ocx.connect(signal_map["OnReceiveRealCondition"], self.condRealCallback)
        self.ocx.connect(signal_map["OnReceiveTrData"], self.trCallback)
        self.ocx.connect(signal_map["OnReceiveRealData"], self.realCallback)
        self.ocx.connect(signal_map["OnReceiveMsg"], self.orderMsgCallback)
        self.ocx.connect(signal_map["OnReceiveChejanData"], self.orderCallback)
        
    # OnEventConnect
    def loginCallback(self, retcode):
        if retcode == 0:
            self.gstate.unlock(True)
        else:
            self.gstate.unlock(False)
            
    def loadCondCallback(self, success, msg):
        if success:
            self.gstate.unlock(True)
        else:
            self.gstate.unlock(False)
            
    def condTrCallback(self, scrno, cond_stocks, condname, cidx, next):
        
        cond_stock_list = cond_stocks.split(";")[:-1]
        self.gstate.unlock(cond_stock_list)
        
    def condRealCallback(self, stockcode, tag, condname, cidx):
        condobj: Condition = cond_manager.cond_dict[condname]
        
        # If stockcode enter
        if tag == "I":
            condobj.addStock(stockcode)
        elif tag == "D":
            condobj.removeStock(stockcode)
            
        cond_manager.addEvent((stockcode, tag, condname, cidx))
            
    def trCallback(self, scrno, rqname, trcode, record, next, *args):
        
        scr_manager.deAct(scrno)
        
        ret_data = {}
        
        if rqname == "계좌평가현황요청":
            single_data = self.api.getTrData(rqname, trcode, record, TR_RETURN_MAP["계좌평가현황요청"]["single"])
            multi_data = self.api.getTrData(rqname, trcode, record, TR_RETURN_MAP["계좌평가현황요청"]["multi"], True)
        
            filtered_multi_data = list(filter(lambda row_data: isStock(row_data.get("종목코드")), multi_data))
            
            ret_data = {
                "single": single_data,
                "multi": filtered_multi_data
            }
            
        if rqname == "주식기본정보요청":
            single_data = self.api.getTrData(rqname, trcode, record, TR_RETURN_MAP["주식기본정보요청"]["single"])
            
            ret_data = {
                "single": single_data
            }
            
        if rqname == "관심종목정보요청":
            multi_data = self.api.getTrData(rqname, trcode, record, TR_RETURN_MAP["관심종목정보요청"]["multi"], True)

            ret_data = {
                "multi": multi_data
            }
            
        if rqname == "주문요청":
            single_data = self.api.getTrData(rqname, trcode, record, TR_RETURN_MAP["주문요청"]["single"])
            
            ret_data = {
                "single": single_data
            }
        
        if rqname == "계좌별주문체결내역상세요청":
            single_data = self.api.getTrData(rqname, trcode, record, TR_RETURN_MAP["계좌별주문체결내역요청"]["single"])
            multi_data = self.api.getTrData(rqname, trcode, record, TR_RETURN_MAP["계좌별주문체결내역요청"]["multi"], True)
            
            ret_data = {
                "single": single_data,
                "multi": multi_data,
                "next": next
            }
            
        if rqname == "미체결요청":
            multi_data = self.api.getTrData(rqname, trcode, record, TR_RETURN_MAP["미체결요청"]["multi"], True)
            
            ret_data = {
                "multi": multi_data,
                "next": next
            }
            
        if rqname == "당일매매일지요청":
            single_data = self.api.getTrData(rqname, trcode, record, TR_RETURN_MAP["당일매매일지요청"]["single"])
            multi_data = self.api.getTrData(rqname, trcode, record, TR_RETURN_MAP["당일매매일지요청"]["multi"], True)
            
            ret_data = {
                "single": single_data,
                "multi": multi_data
            }
            
        if rqname == "예수금상세현황요청":
            single_data = self.api.getTrData(rqname, trcode, record, TR_RETURN_MAP["예수금상세현황요청"]["single"])
            
            ret_data = {
                "single": single_data
            }
        
        if rqname == "당일실현손익상세요청":
            single_data = self.api.getTrData(rqname, trcode, record, TR_RETURN_MAP["당일실현손익상세요청"]["single"])
            multi_data = self.api.getTrData(rqname, trcode, record, TR_RETURN_MAP["당일실현손익상세요청"]["multi"], True)
            
            ret_data = {
                "single": single_data,
                "multi": multi_data
            }
            
        self.gstate.unlock(ret_data)
        
    def realCallback(self, stockcode, real_type, data):
        
        stockobj: Stock = self.api.getStockObj(stockcode)
        
        real_data = {}
        if real_type == "주식체결":
            real_data = self.api.getRealData(stockcode, real_type)
            
            cur_price = real_data["현재가"]
            today_updown_rate = real_data["등락율"]
            today_trans_count = real_data["누적거래량"]
            buy_sell_strength = real_data["체결강도"]
            
            stockobj.setStockInfo({
                "cur_price": cur_price,
                "today_updown_rate": today_updown_rate,
                "today_trans_count": today_trans_count,
                "buy_sell_strength": buy_sell_strength
            })
            
        real_manager.addEvent((stockcode, real_type, real_data))
        
    def orderMsgCallback(self, scrno, rqname, trcode, msg):
        # if rqname == "주문요청":
        #     self.gstate.unlock(msg, "order_msg")
        
        pass
        
    def orderCallback(self, tradetype, itemcnt, datalist):
        # 매수 시 주문체결(접수) - 주문체결(체결) 잔고,
        # 매도 시 주문체결(접수) - 잔고(기존보유수량) - 주문체결(체결) - 잔고(체결이후 보유수량)
        order_data = {}
        
        # 주문체결
        if tradetype == "0":
            order_data = self.api.getChejanData(tradetype)
            
            accno = order_data.get("계좌번호")
            orderno = order_data.get("주문번호")
            stockcode = order_data.get("종목코드,업종코드")
            order_quantity = intOrZero(order_data.get("주문수량"))
            rest_quantity = intOrZero(order_data.get("미체결수량"))
            order_price = intOrZero(order_data.get("주문가격"))
            order_status = order_data.get("주문상태")
            order_op = order_data.get("매도수구분")         # 1 is 매도, 2 is 매수
            order_gubun = order_data.get("주문구분")
            op_time = order_data.get("주문/체결시간")    # ex) 121252
            
            stockcode = getRegStock(stockcode)
            
            acc = self.api.getAccObj(accno)
            if order_status == "접수":
                if order_gubun == "+매수" or order_gubun == "-매도":
                    if rest_quantity == 0:
                        del acc.not_completed_order[orderno]
                    else:
                        acc.addNCOrder(op_time, orderno, stockcode, order_op, order_quantity, rest_quantity, order_price)
                    
                    if order_gubun == "매수":
                        acc.today_buy_stocks.add(stockcode)
            
            if order_status == "확인":
                if order_gubun == "+매수정정" or order_gubun == "-매도정정":
                    if rest_quantity == 0:
                        del acc.not_completed_order[orderno]
                    else:
                        acc.addNCOrder(op_time, orderno, stockcode, order_op, order_quantity, rest_quantity, order_price)
            
            elif order_status == "체결":
                # Add 체결 log
                exec_price = intOrZero(order_data.get("단위체결가"))
                exec_quantity = intOrZero(order_data.get("단위체결량"))
                exec_fee = intOrZero(order_data.get("당일매매수수료"))
                exec_tax = intOrZero(order_data.get("당일매매세금"))
                
                acc.addExecLog(op_time, orderno, stockcode, order_op, exec_price, exec_quantity, exec_fee, exec_tax)
                
                # Fix not completed order info
                new_nc_order = dict(acc.not_completed_order[orderno])
                new_nc_order["rest_quantity"] = rest_quantity
                
                if rest_quantity == 0:
                    del acc.not_completed_order[orderno]
                else:
                    acc.not_completed_order[orderno] = new_nc_order
                
        # 잔고
        elif tradetype == "1":
            order_data = self.api.getChejanData(tradetype)
            
            accno = order_data.get("계좌번호")
            stockcode = order_data.get("종목코드,업종코드")
            quantity = order_data.get("보유수량")
            possible_quantity = order_data.get("주문가능수량")
            average_buyprice = order_data.get("매입단가")
            today_income = order_data.get("당일실현손익(유가)")

            stockcode = getRegStock(stockcode)

            acc = self.api.getAccObj(accno)
                       
            # Update today income
            acc.setAccInfo({
                "today_income": today_income
            })
            
            # Update holdings
            holdings = dict(acc.holdings)
            try:
                quantity = int(quantity)
            except TypeError as e:
                logger.warning(e)
            
            if quantity <= 0:
                del holdings[stockcode]
            else:
                try:
                    holding_info = holdingInfo(stockcode, quantity, possible_quantity, average_buyprice)
                except StockNotFoundException as e:
                    logger.error(e)
                
                holdings[stockcode] = holding_info
                
            acc.holdings = holdings
        
        order_manager.addEvent((tradetype, order_data))
