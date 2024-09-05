import sys
from PySide2.QtWidgets import *
from PySide2.QtAxContainer import QAxWidget

from core.api import API
from core.callback_handler import CallbackHandler
from core.global_state import GlobalState
from core.kiwoom import Kiwoom
from windows.main_win.main_win import MainWin
from qt_material import apply_stylesheet

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

    kiwoom = Kiwoom(ocx)
    api = API(kiwoom)
    
    callback_handler = CallbackHandler()
    callback_handler.watch()
    
    win = MainWin("main_win", "GUI/main_win.ui", "style/main_win.css")
    
    gstate = GlobalState()
    gstate.activateWin(win)

    sys.exit(app.exec_())
