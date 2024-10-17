from PySide2.QtWidgets import QLabel, QWidget
from PySide2.QtGui import QMovie
from PySide2.QtCore import QSize

class LoadingIndicator(QWidget):
    def __init__(self, ui, gif_path):
        super().__init__()

        self.ui = ui
        
        # Make label
        self.label = QLabel(self)
        self.movie = QMovie(gif_path)
        
        # Set gif to label
        self.label.setMovie(self.movie)
        
        self.label.hide()

    def show(self):
        self.label.show()
        self.movie.start()
        
    def hide(self):
        self.movie.stop()
        self.label.hide()
        
    def setSize(self, width, height):
        self.movie.setScaledSize(QSize(width, height))
        self.label.setFixedSize(width, height)
        
        # Set gif to label
        self.label.setMovie(self.movie)
        
    def center(self):
        size = self.label.size()
        ph = self.ui.geometry().height()
        pw = self.ui.geometry().width()
        self.label.move(int(pw/2 - size.width()/2), int(ph/2 - size.height()/2))
        