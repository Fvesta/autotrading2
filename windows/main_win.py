from PySide2.QtUiTools import QUiLoader

from core.api import API
from core.callback_handler import CallbackHandler
from core.errors import LoginFailedException
from core.logger import logger

class MainWin:
    def __init__(self):
        super().__init__()
        self.api = API()
        self.ui = QUiLoader().load('GUI/main.ui', None)
        
        self.callback_handler = CallbackHandler()
        
        self.initSetting()
            
    def initSetting(self):
        pass
        
    def show(self):
        self.callback_handler.watch()
        self.login()
        
        self.ui.show()
        
    def login(self):
        login_success = self.api.login()
        
        try:
            if login_success:
                logger.error("로그인에 성공했습니다")
            else:
                raise LoginFailedException
        except LoginFailedException as e:
            logger.error(e)