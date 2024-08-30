from core.global_state import UseGlobal

class API(UseGlobal):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(API, cls).__new__(cls)
            
        return cls.instance
    
    def __init__(self, kiwoom=None):
        if hasattr(self, "initialized"):
            return
        
        super().__init__()
        self.kiwoom = kiwoom
        self.ocx = self.kiwoom.ocx
        
        self.initialized = True
        
    def login(self):
        self.kiwoom.commConnect()
        login_success = self.gstate.lock()
    
        return login_success
    
    def getLoginInfo(self):
        stock_name = self.kiwoom.getMasterCodeName("005930")
        conn = self.kiwoom.getConnectState()
        acc_count = self.kiwoom.getLoginInfo("ACCOUNT_CNT")
        acc_total = self.kiwoom.getLoginInfo("ACCNO")
        acc_list = acc_total.split(";")[:-1]
        
        user_id = self.kiwoom.getLoginInfo("USER_ID")
        user_name = self.kiwoom.getLoginInfo("USER_NAME")
        
        return [acc_list, user_id, user_name]
    