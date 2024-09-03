import os
from qt_material import QtStyleTools
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QObject, QEvent, QTimer
from PySide2.QtWidgets import QMainWindow

from core.global_state import GlobalState
from style.colors import colors
from style.utils import setTableSizeSameHor

class ResizeEventFilter(QObject):
    def eventFilter(self, ui: QMainWindow, event):
        gstate = GlobalState()
        account_dict = gstate.getState("account_dict")
        name = ui.objectName()
        
        if event.type() == QEvent.Resize:
            if name == "main_win":
                accounts = account_dict.keys()
                for accno in accounts:
                    balanceTable = getattr(ui, f"_{accno}_balanceTable")
                    setTableSizeSameHor(balanceTable)
                
        
        return super(ResizeEventFilter, self).eventFilter(ui, event)
    
class WindowAbs(QtStyleTools):
    def __init__(self, name, ui_path, css_path):
        self.ui = QUiLoader().load(ui_path, None)
        self.ui.setObjectName(name)
        self.css_path = css_path
        
        self.apply_stylesheet(self.ui, "dark_cyan.xml")
        
        # Event setting
        self.event_filter = ResizeEventFilter(self.ui)
        self.ui.installEventFilter(self.event_filter)
    
    def updateStyle(self):
        # Apply custom stylesheet
        stylesheet = self.ui.styleSheet()
        with open(self.css_path) as file:
            newStylesheet = stylesheet + file.read().format(**os.environ, **colors)
            self.ui.setStyleSheet('')
            self.ui.setStyleSheet(newStylesheet)
    
    def initSetting(self):
        
        # Update object classes, set size ...
        
        # Apply custom style
        self.updateStyle()
    
    # Call after show function (after layout calculation is done)
    def afterSetting(self):
        pass
    
    def show(self):
        self.ui.show()
        QTimer.singleShot(0, self.afterSetting)
    
    def close(self):
        pass