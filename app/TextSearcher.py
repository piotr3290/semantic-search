from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QTextCursor

from app.KeywordsExtractor import KeywordsExtractor
from app.SynonymsFinder import SynonymsFinder
from app.WordComparator import Stemmer, Lemmatizer, WordComparator


class TextSearcher:

    def __init__(self):
        self.words = {}
        self.keywords_extractor = KeywordsExtractor()
        self.synonyms_finder = SynonymsFinder()
        self.word_comparator = WordComparator()

    def set_search_phrase(self, search_phrase):
        keywords = self.keywords_extractor.get_keywords(search_phrase)
        synonyms = self.synonyms_finder.find_synonyms(keywords)
        print(keywords)
        print(synonyms)
        self.construct_words(keywords + synonyms)

    def set_word_comparator(self, comparator):
        if comparator == 'stemming':
            self.word_comparator = Stemmer()
        elif comparator == 'lemmatization':
            self.word_comparator = Lemmatizer()
        else:
            self.word_comparator = WordComparator()
        self.construct_words(self.words)

    def construct_words(self, words):
        self.words = set([self.word_comparator.get_word(word) for word in words])
        print(words)

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
            if self.word_comparator.get_word(word.lower()) in self.words:
                return search_cursor.selectionStart(), search_cursor.selectionEnd()
            else:
                search_cursor.setPosition(search_cursor.selectionEnd())
        return -1, -1
