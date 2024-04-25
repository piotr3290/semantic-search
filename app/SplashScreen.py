from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QSplashScreen, QApplication
from pyqtspinner import WaitingSpinner

from app.ui.splashScreen_ui import Ui_splashScreen


class SplashScreen(QSplashScreen, Ui_splashScreen):

    def __init__(self):
        super(QSplashScreen, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.spinner = WaitingSpinner(
            self,
            roundness=100.0,
            fade=35.0,
            radius=20,
            lines=100,
            line_length=15,
            line_width=15,
            speed=0.7,
            color=QColor(144, 8, 255)
        )
        self.spinner.start()

    def mousePressEvent(self, event):
        event.ignore()

    def showEvent(self, event):
        screen_rect = QApplication.desktop().screenGeometry()
        self.move((screen_rect.width() - self.width()) // 2, (screen_rect.height() - self.height()) // 2)
