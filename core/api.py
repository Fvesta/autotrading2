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
    