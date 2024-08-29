class Kiwoom:
    def __init__(self, ocx):
        self.ocx = ocx
    
    # Login
    def commConnect(self):
        self.ocx.dynamicCall("CommConnect()")