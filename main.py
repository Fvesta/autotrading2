import sys
from PySide2.QtWidgets import *
from PySide2.QtAxContainer import QAxWidget 

from core.api import API
from core.kiwoom import Kiwoom
from windows.main_win import MainWin
from qt_material import apply_stylesheet

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

    kiwoom = Kiwoom(ocx)
    api = API(kiwoom)
    win = MainWin("main_win", "GUI/main_win.ui", "style/main_win.css")
    
    # App style setting
    # apply_stylesheet(app, theme='dark_cyan.xml')
    
    win.show()
    sys.exit(app.exec_())
