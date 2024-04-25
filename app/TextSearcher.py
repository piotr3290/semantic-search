from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QTextCursor

from app.KeywordsExtractor import KeywordsExtractor
from app.SynonymsFinder import SynonymsFinder


class TextSearcher:

    def __init__(self):
        self.words = []
        self.keywords_extractor = KeywordsExtractor()
        self.synonyms_finder = SynonymsFinder()

    def set_search_phrase(self, search_phrase):
        keywords = self.keywords_extractor.get_keywords(search_phrase)
        synonyms = self.synonyms_finder.find_synonyms(keywords)
        print(keywords)
        print(synonyms)
        self.words = keywords + synonyms

    def search(self, cursor):
        document = cursor.document()
        regex = QRegExp(r'\b\w+\b')

        search_cursor = QTextCursor(document)
        search_cursor.setPosition(cursor.position())

        while True:
            search_cursor = document.find(regex, search_cursor)
            if search_cursor.isNull():
                break
            word = search_cursor.selectedText()
            if word.lower() in self.words:
                return search_cursor.selectionStart(), search_cursor.selectionEnd()
            else:
                search_cursor.setPosition(search_cursor.selectionEnd())
        return -1, -1
