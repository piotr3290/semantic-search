from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication

from app.MainWindow import MainWindow
from app.SplashScreen import SplashScreen


class AppInitializer(QObject):
    main_window_loaded = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.splash_screen = SplashScreen()
        self.splash_screen.show()

        self.main_window = MainWindow()

    def load_main_window(self):
        self.main_window.load_models()
        self.main_window_loaded.emit()

    def show_main_window(self):
        self.splash_screen.finish(self.main_window)
        self.main_window.show()
