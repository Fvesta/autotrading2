class ScrManager:
    def __new__(cls, *args):
        if not hasattr(cls, "instance"):
            cls.instance = super(ScrManager, cls).__new__(cls)
            
        return cls.instance
    
    def __init__(self):
        if hasattr(self, "initialized"):
            return
        
        self.used_scrno_set = set()
        self.lastno = 0
        
        self.scrno_dict = {}
        self.scr_used = {}
        
        for scrno in self.scrno_dict.values():
            self.scr_used[scrno] = False
        
        self.initialized = True
        
    def __formatScrNo(self, num):
        formatted_num = f"{num:04}"
        return formatted_num
        
    def scrAct(self, scrname):
        
        if scrname not in self.scrno_dict:
            self.lastno += 1
            scrno = self.__formatScrNo(self.lastno)
            
            self.scrno_dict[scrname] = scrno
        
        scrno = self.scrno_dict[scrname]
        
        self.scr_used[scrno] = True
        return scrno
    
    def deAct(self, scrno):
        if scrno not in self.scr_used:
            return
        
        self.scr_used[scrno] = False
        
scr_manager = ScrManager()
        