from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QTextCursor
from gensim.utils import tokenize
from nltk.tokenize import sent_tokenize, word_tokenize
from sentence_transformers import SentenceTransformer

from app.KeywordsExtractor import KeywordsExtractor
from app.SynonymsFinder import SynonymsFinder
from app.WordComparator import Stemmer, Lemmatizer, WordComparator


class TextSearcher:

    def __init__(self):
        self.words = {}
        self.keywords_extractor = KeywordsExtractor()
        self.synonyms_finder = SynonymsFinder()
        self.word_comparator = WordComparator()
        # self.similarity_model = SentenceTransformer("all-mpnet-base-v2")
        self.similarity_model = SentenceTransformer("all-MiniLM-L6-v2")

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
        print('WORDS')
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

    def search_console(self, sentences):
        for sentence in sent_tokenize(sentences):
            sentence_tokens = set(tokenize(sentence, lowercase=True))
            print(sentence_tokens)
            print(sentence_tokens.isdisjoint(self.words))

    def tokenize_into_sentences(self, paragraph):
        return sent_tokenize(paragraph)

    def filter_sentences(self, sentences):
        results = []
        for index, sentence in enumerate(sentences):
            sentence_tokens = set(tokenize(sentence, lowercase=True))
            print(sentence_tokens)
            print(self.words)
            print(sentence_tokens.isdisjoint(self.words))
            contains_words = not sentence_tokens.isdisjoint(self.words)
            results.append((index, contains_words, sentence))
        return results

    def calculate_similarity(self, search_sentence, corpus):
        embeddings_corpus = self.similarity_model.encode(corpus)
        embeddings_search_sentence = self.similarity_model.encode(search_sentence)
        similarities = self.similarity_model.similarity(embeddings_search_sentence, embeddings_corpus)
        return similarities[0]
