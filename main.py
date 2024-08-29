import sys
from PySide2.QtWidgets import *
from PySide2.QtAxContainer import QAxWidget 

from core.api import API
from core.kiwoom import Kiwoom
from windows.main_win import MainWin

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

    kiwoom = Kiwoom(ocx)
    api = API(kiwoom)
    win = MainWin()
    
    win.show()
    sys.exit(app.exec_())
