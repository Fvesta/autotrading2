
# For typehint
from __future__ import annotations

import os
from qt_material import QtStyleTools
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QObject, QEvent, QTimer, QObject
from PySide2.QtWidgets import QMainWindow

from core.logger import logger
from core.global_state import UseGlobal
from style.colors import colors
from style.utils import setTableSizeSameHor, setTableSizeSameVer

class UIEventFilter(UseGlobal, QObject):
    def __init__(self, ui: QMainWindow):
        QObject.__init__(self)
        UseGlobal.__init__(self)
        
    def eventFilter(self, ui: QMainWindow, event):
        account_dict = self.gstate.getState("account_dict")
        
        # Window name format is "_{accno}_{win_name}" or "{win_name}"
        full_name = ui.objectName()
        name_arr = full_name.split("_")
        try:
            # If name is started with "_"
            if len(name_arr[0]) == 0:
                win_name = "_".join(name_arr[2:])
            else:
                win_name = full_name
        except ValueError:
            logger.warning("Wrong window name")
            return super(UIEventFilter, self).eventFilter(ui, event)
        
        if event.type() == QEvent.Resize:
            if win_name == "main_win":
                accounts = account_dict.keys()
                for accno in accounts:
                    balance_table = getattr(ui, f"_{accno}_balance_table")
                    setTableSizeSameHor(balance_table)
            
            if win_name == "trade_setting":
                pass
            
            if win_name == "balance_win":
                setTableSizeSameHor(ui.holding_table)
                
            if win_name == "trade_log_win":
                setTableSizeSameHor(ui.balance_log_table)
                setTableSizeSameHor(ui.exec_log_table)
        
        if event.type() == QEvent.Close:
            if full_name in self.gstate.activated_windows:
                winobj = self.gstate.activated_windows[full_name]
                winobj.eventTerm()
                winobj.stateTerm()
                del self.gstate.activated_windows[full_name]
        
        return super(UIEventFilter, self).eventFilter(ui, event)

def showModal(func, single=True):
    def wrapper(self: "WindowAbs", *args, **kwargs):
        func(self, *args, **kwargs)
        
        if single:
            if self.name in self.gstate.activated_windows:
                return
        
        self.gstate.activated_windows[self.name] = self
        
        self.ui.show()
        
        # If ui is loaded, calculate table once after loading
        QTimer.singleShot(0, self.afterSetting)
    
    return wrapper
    
class WindowAbs(QtStyleTools, UseGlobal, QObject):
    def __init__(self, name, ui_path, css_path):
        QObject.__init__(self)
        UseGlobal.__init__(self)

        self.name = name
        self.ui = QUiLoader().load(ui_path, None)
        self.ui.setObjectName(name)
        self.css_path = css_path
        
        self.apply_stylesheet(self.ui, theme="style/dark_cyan.xml")
        
        # Event setting
        self.event_filter = UIEventFilter(self.ui)
        self.ui.installEventFilter(self.event_filter)
    
    def updateStyle(self):
        # Apply custom stylesheet
        stylesheet = self.ui.styleSheet()
        with open(self.css_path) as file:
            newStylesheet = stylesheet + file.read().format(**os.environ, **colors)
            self.ui.setStyleSheet('')
            self.ui.setStyleSheet(newStylesheet)
    
    def initSetting(self):
        pass
    
    # Call after show function (after layout calculation is done)
    def afterSetting(self):
        
        # Apply custom style
        self.updateStyle()
        
    @showModal
    def show(self):
        self.ui.show()
        QTimer.singleShot(0, self.afterSetting)
    
    def close(self):
        pass
