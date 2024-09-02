from PySide2.QtCore import QTimer

class WaitTimer():
    def __init__(self, name, interval=1000, callback=None):
        self.name = name
        self.wait = False
        self.interval = interval
        
        if callback == None:
            self.callback = self.fin
        else:
            self.callback = self.callbackWrapper(callback)
        
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.callback)
        
    def startWait(self):
        self.wait = True
        self.timer.start(self.interval)
        
    def cancel_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            
    def setCallback(self, callback):
        self.callback = callback
        self.timer.timeout.connect(self.callback)
        
    def fin(self):
        self.wait = False
        
    def callbackWrapper(self, callback):
        def wrapper(*args, **kwargs):
            self.wait = False
            callback(*args, **kwargs) 
        
        return wrapper
        
    def isWait(self):
        return self.wait
        
    