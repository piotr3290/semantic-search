import sys
from threading import Thread

from PyQt5.QtWidgets import QApplication

from app.AppInitializer import AppInitializer

if __name__ == '__main__':
    app = QApplication(sys.argv)

    app_initializer = AppInitializer()
    app_initializer.main_window_loaded.connect(app_initializer.show_main_window)

    load_window_thread = Thread(target=app_initializer.load_main_window)
    load_window_thread.start()

    app.exec_()
