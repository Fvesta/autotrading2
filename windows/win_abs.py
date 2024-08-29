import os
from qt_material import QtStyleTools
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QObject, QEvent

from style.colors import colors
from style.utils import setTableSizeSameHor

class ResizeEventFilter(QObject):
    def eventFilter(self, ui, event):
        name = ui.objectName()
        
        if event.type() == QEvent.Resize:
            if name == "main_win":
                setTableSizeSameHor(ui.tableWidget)
        
        return super(ResizeEventFilter, self).eventFilter(ui, event)
    
class WindowAbs(QtStyleTools):
    def __init__(self, name, ui_path, css_path):
        self.ui = QUiLoader().load(ui_path, None)
        self.ui.setObjectName(name)
        
        self.apply_stylesheet(self.ui, "dark_cyan.xml")
        
        # Apply custom stylesheet
        stylesheet = self.ui.styleSheet()
        with open(css_path) as file:
            newStylesheet = stylesheet + file.read().format(**os.environ, **colors)
            self.ui.setStyleSheet('')
            self.ui.setStyleSheet(newStylesheet)
        
        # Event setting
        self.event_filter = ResizeEventFilter(self.ui)
        self.ui.installEventFilter(self.event_filter)
            
    def initSetting(self):
        pass
    
    def show(self):
        pass
    
    def close(self):
        pass