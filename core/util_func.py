from core.logger import logger
from core.errors import ErrorCode
from core.global_state import GlobalState

def getRegStock(stockcode):
    if not stockcode:
        raise ValueError
    
    return stockcode[1:] if stockcode[0] == 'A' else stockcode

def isStock(stockcode, market=["kospi", "kosdaq"]):
    gstate = GlobalState()
    
    try:
        stockcode = getRegStock(stockcode)
    except ValueError:
        return False
    
    for mk in market:
        if mk == "kospi" and stockcode in gstate.kospi_stocks:
            return True
        elif mk == "kosdaq" and stockcode in gstate.kosdaq_stocks:
            return True
        
    return False
