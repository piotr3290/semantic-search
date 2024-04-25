import regex
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from app.InfoDialog import InfoDialog
from app.TextSearcher import TextSearcher
from app.ui.mainWindow_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.textSearcher = None
        self.chunk_size = 100
        self.file_position = 0
        self.isSearchInputSet = False
        self.selected_file_path = ''

        self.setupUi(self)
        self.retranslateUi(self)

        self.openFileButton.clicked.connect(self.open_file)
        self.searchNextButton.clicked.connect(self.search)
        self.searchStartButton.clicked.connect(self.search_start)
        self.loadMoreButton.clicked.connect(self.append_chunk)
        self.searchInput.textChanged.connect(self.search_input_changed)

    def load_models(self):
        self.textSearcher = TextSearcher()

    def search_input_changed(self):
        self.isSearchInputSet = False

    def open_file(self):
        self.textBrowser.clear()
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '')

        if file_path != '':
            self.selected_file_path = file_path
            self.file_position = 0
            self.load_next_chunk()

    def get_next_chunk(self):
        with open(self.selected_file_path, 'rb') as file:
            file.seek(self.file_position)
            chunk = file.read(self.chunk_size)

        return self.slice_string_at_last_whitespace(chunk.decode('utf-8'))

    def append_chunk(self):
        chunk = self.get_next_chunk()
        self.textBrowser.moveCursor(QTextCursor.End)
        self.textBrowser.insertPlainText(chunk)
        self.textBrowser.moveCursor(QTextCursor.Start)
        self.file_position += len(chunk)

    def load_next_chunk(self):
        chunk = self.get_next_chunk()
        self.textBrowser.setText(chunk)
        self.clear_highlights()
        self.textBrowser.moveCursor(QTextCursor.Start)
        self.file_position += len(chunk)

    def search_start(self):
        self.file_position = 0
        self.load_next_chunk()
        self.search()

    def search(self):
        input_text = self.searchInput.text()
        self.clear_highlights()

        if not self.isSearchInputSet:
            self.textSearcher.set_search_phrase(input_text)
            self.isSearchInputSet = True

        while True:
            cursor = self.textBrowser.textCursor()
            start, end = self.textSearcher.search(cursor)

            if start == -1:
                chunk = self.get_next_chunk()
                if not chunk:
                    info_dialog = InfoDialog()
                    info_dialog.exec_()
                    break
                else:
                    self.textBrowser.setText(chunk)
                    self.clear_highlights()
                    self.textBrowser.moveCursor(QTextCursor.Start)
                    self.file_position += len(chunk)
            else:
                cursor.beginEditBlock()
                color_format = QTextCharFormat(cursor.charFormat())
                color_format.setBackground(Qt.yellow)

                cursor.setPosition(start)
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, end - start)
                cursor.mergeCharFormat(color_format)
                cursor.setPosition(end)
                cursor.endEditBlock()
                self.textBrowser.setTextCursor(cursor)
                break

    def slice_string_at_last_whitespace(self, text):
        match = regex.search(r'(?r)[\s\.\,]', text)
        return text if match is None else text[:match.end()]

    def clear_highlights(self):
        cursor = self.textBrowser.textCursor()
        initial_position = cursor.position()
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat())
        cursor.setPosition(initial_position)
        self.textBrowser.setTextCursor(cursor)
