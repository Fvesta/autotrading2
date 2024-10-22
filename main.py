import sys
import os
import traceback

# Change resource path
try:
    os.chdir(sys._MEIPASS)
    print(sys._MEIPASS)
except:
    os.chdir(os.getcwd())

from PySide2.QtWidgets import *
from PySide2.QtAxContainer import QAxWidget

app = QApplication(sys.argv)

from core.logger import logger
from core.api import API
from core.callback_handler import CallbackHandler
from core.real_processing import real_manager
from core.order_processing import order_manager
from core.condition import cond_manager
from core.kiwoom import Kiwoom
from windows.main_win.main_win import MainWin

def exception_hook(exctype, value, tb):
    error_message = ''.join(traceback.format_exception(exctype, value, tb))
    logger.error(error_message)
    
    # Set popup message
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("예외가 발생했습니다!")
    msg.setInformativeText(error_message)
    msg.setWindowTitle("Error")
    msg.exec_()

    # Not exit
    # sys.exit(1)  # 주석 처리: 프로그램 종료 방지

if __name__ == "__main__":
    ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
    
    sys.excepthook = exception_hook

    kiwoom = Kiwoom(ocx)
    api = API(kiwoom)
    
    # Set real processing manager
    real_manager.ready(api)
    real_manager.start()
    
    # Set condition processing manager
    cond_manager.ready(api)
    cond_manager.start()
    
    # Set order processing manager
    order_manager.ready(api)
    order_manager.start()
    
    # Set event callback handler
    callback_handler = CallbackHandler()
    callback_handler.watch()
    
    win = MainWin("main_win", "GUI/main_win.ui", "style/css/main_win.css")
    
    win.show()

    app.exec_()
    
    # Stop threads
    cond_manager.stop()
    real_manager.stop()
    order_manager.stop()
    