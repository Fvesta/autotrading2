from enum import Enum

class ErrorCode(Enum):
    OP_ERROR = -100            # Basic error
    OP_KIWOOM_ERROR = -101     # Kiwoom error
    OP_INPUT_ERROR = -102      # Function parameter error

class LoginFailedException(Exception):
    def __init__(self, msg=None):
        if msg == None:
            super().__init__("Login failed")
        else:
            super().__init__(f"Login failed: {msg}")
        
class KiwoomException(Exception):
    def __init__(self, errcode, msg=None):
        if msg == None:
            super().__init__(f"Kiwoom error [{errcode}]")
        else:
            super().__init__(f"kiwoom error [{errcode}]: {msg}")
        