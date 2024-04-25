from PyQt5.QtWidgets import QDialog

from app.ui.infoDialog_ui import Ui_infoDialog


class InfoDialog(QDialog, Ui_infoDialog):
    def __init__(self):
        super(QDialog, self).__init__()

        self.setupUi(self)
        self.retranslateUi(self)
