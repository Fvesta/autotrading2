import math
from PySide2.QtCore import Signal, QObject

from core.global_state import UseGlobal
from core.logger import logger
from core.api import API
from core.real_processing import real_manager
from core.order_processing import order_manager
from core.autotrading.basic_options import STOP_LOSS_BASIC_OPTION
from core.utils.stock_util import getRegStock


class StopLoss(QObject, UseGlobal):
    update = Signal(str, dict)
    
    def __init__(self, acc):
        QObject.__init__(self)
        UseGlobal.__init__(self)
        self.acc = acc
        
        self.api = API()
        
        self.observe_condition = {}
        
    def updateStates(self, key="", extra={}):
        # If balance updated
        if key == f"{self.acc.accno}$balance":
            cur_holdings = dict(self.acc.holdings)
            
            # If new stock is added, add sell conditions
            for stockcode in cur_holdings.keys():
                if stockcode not in self.observe_condition:
                    self.observe_condition[stockcode] = list(self.division)
            
            # If There are conditions of stockcode, but is not holdings => delete conditions
            observed_stocks_set = set(list(self.observe_condition.keys()))
            holding_stocks_set = set(list(cur_holdings.keys()))
            
            ignore_stocks_set = observed_stocks_set - holding_stocks_set
            for stockcode in ignore_stocks_set:
                del self.observe_condition[stockcode]
                
            # ReReg real event
            real_manager.regReal(f"{self.acc.accno}$stoploss", list(cur_holdings.keys()), self.realEventCallback)
        
        if key == "stoploss_sell":
            stockcode = extra.get("stockcode")
            sell_percent = extra.get("sell_percent")
            cond_income_rate = extra.get("cond_income_rate")
            
            logger.debugSessionStart(f"Stoploss 실행: {cond_income_rate}%")
            
            if self.acc.isHoldings(stockcode):
                holding_info = self.acc.holdings[stockcode]
            
                # Calculate quantity
                total_quantity = holding_info.possible_quantity
                sell_quantity = math.ceil(total_quantity * (sell_percent / 100))
                
                order_manager.sellStockNow(self.acc.accno, stockcode, sell_quantity)
            else:
                logger.warning(f"{self.acc.accno}: 현재 잔고에 {stockcode}가 존재하지 않습니다")
                logger.debugSessionFin("Stoploss 종료")
    
    def eventReg(self):
        self.update.connect(self.updateStates)
    
    def eventTerm(self):
        self.update.disconnect(self.updateStates)
        
    def setOption(self, used, option={}):
        self.used = used
        self.division = option.get("division", STOP_LOSS_BASIC_OPTION["division"])
        
    def start(self):
        self.stateReg()
        self.updateStates()
        self.eventReg()
        
        # Set default sell conditions
        observe_condition = {}
        cur_holdings = dict(self.acc.holdings)
        for stockcode in cur_holdings.keys():
            if stockcode in self.observe_condition:
                observe_condition[stockcode] = self.observe_condition[stockcode]
                continue
            
            observe_condition[stockcode] = list(self.division)
            
        self.observe_condition = observe_condition
            
        # Reg real event
        real_manager.regReal(f"{self.acc.accno}$stoploss", list(cur_holdings.keys()), self.realEventCallback)
    
    def stop(self):
        self.eventTerm()
        self.stateTerm()
        real_manager.termReal(f"{self.acc.accno}$stoploss") 
    
    def realEventCallback(self, seed, stockcode, real_type, real_data):
        if real_type == "주식체결":
            stockcode = getRegStock(stockcode)
            
            if self.acc.isHoldings(stockcode):
               
                # Decide sell or not
                conditions = self.observe_condition[stockcode]
                new_observe_condition = []
                for condition in conditions:
                    cond_income_rate = condition["income_rate"]
                    cond_sell_percent = condition["sell_percent"]
                    
                    holding_info = self.acc.holdings[stockcode]
                    cur_income_rate = holding_info.getIncomeRate()
                    
                    if cur_income_rate <= cond_income_rate:
                        # Sell in main thread
                        self.update.emit("stoploss_sell", {
                            "stockcode": stockcode,
                            "sell_percent": cond_sell_percent,
                            "cond_income_rate": cond_income_rate,
                        })
                        break
                    else:
                        new_observe_condition.append(condition)
                    
                self.observe_condition[stockcode] = new_observe_condition
                        