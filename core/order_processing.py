from PySide2.QtCore import QThread, Signal
import debugpy
import queue
import sys

from core.global_state import UseGlobal
from core.logger import logger
from core.constants import ORDER_TAG, ORDER_TYPE
from core.errors import ErrorCode, OrderFailedException
from core.scr_manager import scr_manager
from core.utils.type_util import intOrZero
from core.wait_timer import WaitTimer

class OrderManager(UseGlobal, QThread):
    acc_update_signal = Signal()
    acc_rest_signal = Signal(str)
    timer_start_signal = Signal()
    
    def __new__(cls, *args):
        if not hasattr(cls, "instance"):
            cls.instance = super(OrderManager, cls).__new__(cls)
            
            return cls.instance
        
    def __init__(self):
        
        if hasattr(self, "initialized"):
            return
        
        QThread.__init__(self)
        UseGlobal.__init__(self)
        
        self.event_queue = queue.Queue()
        
        self.api = None
        self.seed_callback_dict = {}
        
        # Essential account callback
        self.event_accno_set = set()
        self.account_timer = WaitTimer("account_timer", 1000, self.accTimerCallback)
        
        self.initialized = True
        
    def eventReg(self):
        self.acc_update_signal.connect(self.updateAccounts)
        self.acc_rest_signal.connect(self.updateAccRest)
        self.timer_start_signal.connect(self.orderTimerStart)
        
    def run(self):
        self.eventReg()
        # Debug setting
        if not (getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')): 
            debugpy.debug_this_thread()
        
        while True:
            event = self.event_queue.get()
            
            if event == None:
                break
            
            self.orderBackgroundProcess(event)
        
    def ready(self, API):
        self.api = API
        
    def stop(self):
        self.event_queue.put(None)
        
    def addEvent(self, event):
        self.event_queue.put(event)
        
    def updateAccRest(self, accno):
        acc = self.api.getAccObj(accno)
        acc.getRestAmount()
        
    def updateAccounts(self):
        
        for accno in self.event_accno_set:
            acc = self.api.getAccObj(accno)
            acc.getRestAmount()
            acc.reqAccInfo()
        
    def accTimerCallback(self):
        if len(self.event_accno_set) == 0:
            return
        
        # Update accounts
        self.acc_update_signal.emit()
            
        # initialize event_accno_set
        self.event_accno_set = set()
        
    def orderTimerStart(self):
        self.account_timer.startWait()
        
    def orderBackgroundProcess(self, event):
        tradetype, order_data = event
        
        accno = order_data.get("계좌번호", "")
        if accno == "":
            logger.warning("주문에 계좌번호 정보가 없습니다.")
            return
        
        if tradetype == "0":
            order_status = order_data.get("주문상태")
            order_gubun = order_data.get("주문구분")
            order_quantity = intOrZero(order_data.get("주문수량"))
            rest_quantity = intOrZero(order_data.get("미체결수량"))
            
            if order_status == "접수" and order_gubun == "+매수":
                self.acc_rest_signal.emit(accno)
                
            if order_status == "확인" and order_gubun == "+매수정정":
                # If first fix order => ignore
                if order_quantity != rest_quantity:
                    self.acc_rest_signal.emit(accno)
                
            if order_status == "체결" and not self.account_timer.isWait():
                self.timer_start_signal.emit()
            
        self.event_accno_set.add(accno)
        
        for seed in self.seed_callback_dict.keys():
            callback = self.seed_callback_dict[seed]
            callback(seed, tradetype, order_data)
    
    ############################################
        # User functions
    ############################################
    
    def regOrderReal(self, seed, callback):
        self.seed_callback_dict[seed] = callback
        
    def termOrderReal(self, seed):
        if seed in self.seed_callback_dict:
            del self.seed_callback_dict[seed]
    
    def buyStockNow(self, accno, stockcode, quantity):
        logger.debug("시장가 매수 호출")
        buy_success_info = self.api.sendOrder("주문요청", scr_manager.scrAct("buystock"), accno, ORDER_TYPE["신규매수"], stockcode, quantity, 0, ORDER_TAG["시장가"], "")

        if isinstance(buy_success_info, ErrorCode):
            logger.error(f"accno: {accno}, 매수 주문 함수 실행에 실패했습니다.")
        
        single_data = buy_success_info.get("single")
        try:
            orderno = single_data["주문번호"]
            if orderno == "":
                raise OrderFailedException("매수")
        except KeyError as e:
            logger.error(f"accno: {accno}, 주문번호가 존재하지 않습니다.")
        except OrderFailedException as e:
            logger.error(f"accno: {accno}, 매수 주문요청에 실패했습니다.")
        
    def buyStockFix(self, accno, stockcode, quantity, ask_step, cancel=False, cancel_buy=False, cancel_time_sec=0):
        pass
    
    def sellStockNow(self, accno, stockcode, quantity):
        logger.debug("시장가 매도 호출")
        order_success_info = self.api.sendOrder("주문요청", scr_manager.scrAct("sellstock"), accno, ORDER_TYPE["신규매도"], stockcode, quantity, 0, ORDER_TAG["시장가"], "")

        if isinstance(order_success_info, ErrorCode):
            logger.error(f"accno: {accno}, 매도 주문 함수 실행에 실패했습니다.")
            
        if order_success_info == None:
            logger.error(f"accno: {accno}, stockcode: {stockcode}, quantity: {quantity} 주문과정에서 문제가 생겼습니다.")
            
        single_data = order_success_info.get("single")
        try:
            orderno = single_data["주문번호"]
            if orderno == "":
                raise OrderFailedException("매도")
        except KeyError as e:
            logger.error(f"accno: {accno}, 주문번호가 존재하지 않습니다.")
        except OrderFailedException as e:
            logger.error(f"accno: {accno}, 매도 주문요청에 실패했습니다.")
            
    def sellStockFix(self, acccno, stockcode, quantity, ask_step, cancel=False, cancel_sell=False, cancel_time_sec=0):
        pass
    
order_manager: OrderManager = OrderManager()
