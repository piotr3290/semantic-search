from gensim.utils import tokenize
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
import torch

from app.KeywordsExtractor import KeywordsExtractor
from app.SynonymsFinder import SynonymsFinder
from app.WordComparator import Stemmer, Lemmatizer, WordComparator
from app.SemanticComparator import SemanticComparator


class TextSearcher:

    def __init__(self, keywords_top_n: int = 8, keywords_min_threshold: float = 0.1, synonyms_top_n: int = 10,
                 synonyms_min_threshold: float = 0.5,
                 embeddings_name: str = 'all-MiniLM-L6-v2', min_semantic_similarity_threshold: float = 0.5):
        self.essential_words: set = set()
        self.keywords: list = []
        self.synonyms: list = []
        self.min_semantic_similarity_threshold: float = min_semantic_similarity_threshold
        self.embeddings: SentenceTransformer = SentenceTransformer(embeddings_name, device="cuda")
        self.keywords_extractor: KeywordsExtractor = KeywordsExtractor(top_n=keywords_top_n,
                                                                       min_threshold=keywords_min_threshold,
                                                                       model=self.embeddings)
        self.synonyms_finder: SynonymsFinder = SynonymsFinder(top_n=synonyms_top_n,
                                                              min_threshold=synonyms_min_threshold)
        self.word_comparator: WordComparator = WordComparator()
        self.semantic_comparator: SemanticComparator = SemanticComparator(embeddings=self.embeddings)

    def reset_words(self)->None:
        self.essential_words = {}
        self.keywords = []
        self.synonyms = []

    def set_filtering_parameters(self, keywords_top_n: int = 5, keywords_min_threshold: float = 0.1,
                                 synonyms_top_n: int = 5,
                                 synonyms_min_threshold: float = 0.5)->None:
        self.keywords_extractor.top_n = keywords_top_n
        self.keywords_extractor.min_threshold = keywords_min_threshold
        self.synonyms_finder.top_n = synonyms_top_n
        self.synonyms_finder.min_threshold = synonyms_min_threshold

    def set_search_phrase(self, search_phrase: str)->None:
        self.keywords = self.keywords_extractor.get_keywords(search_phrase)
        self.synonyms = self.synonyms_finder.find_synonyms(self.keywords)
        self.construct_words(self.keywords + self.synonyms)

    def set_word_comparator(self, comparator: WordComparator)->None:
        if comparator == 'stemming':
            self.word_comparator = Stemmer()
        elif comparator == 'lemmatization':
            self.word_comparator = Lemmatizer()
        else:
            self.word_comparator = WordComparator()
        self.construct_words(self.keywords + self.synonyms)

    def construct_words(self, words: list)->None:
        self.essential_words = set([self.word_comparator.get_word(word) for word in words])

    def tokenize_into_sentences(self, paragraph:str)->list:
        return sent_tokenize(paragraph)

    def filter_sentences(self, sentences:list)->list:
        results = []
        for index, sentence in enumerate(sentences):
            sentence_tokens = set(tokenize(sentence, lowercase=True))
            contains_words = not sentence_tokens.isdisjoint(self.essential_words)
            results.append((index, contains_words, sentence))
        return results

    def calculate_similarity(self, search_phrase:str, corpus:list)->list:
        return self.semantic_comparator.calculate_similarity(search_phrase, corpus)

    def search(self, search_phrase:str, corpus:str)->set:
        self.reset_words()
        self.set_search_phrase(search_phrase)
        sentences = self.tokenize_into_sentences(corpus)
        filtered_sentences = [filtered_sentence for filtered_sentence in self.filter_sentences(sentences) if
                              filtered_sentence[1]]

        hits = self.calculate_similarity(search_phrase,
                                         [filtered_sentence[2] for filtered_sentence in filtered_sentences])
        best_hits = [hit for hit in hits if hit['score'] >= self.min_semantic_similarity_threshold]

        best_hits_sentences = set()
        for best_hit in best_hits:
            best_hits_sentences.add(filtered_sentences[best_hit['corpus_id']][2])

        return best_hits_sentences
