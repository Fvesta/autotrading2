from core.wait_timer import WaitTimer


class Condition:
    real_count = 0
    
    def __init__(self, cidx, condname):
        self.cidx = cidx
        self.condname = condname
        self.req_timer = WaitTimer(self.condname, 61000)
    
    