from core.api import API


class Account:
    accountCnt = 0
    
    def __init__(self, accNo):
        Account.accountCnt += 1
        
        self.api = API()
        self.accNo = accNo