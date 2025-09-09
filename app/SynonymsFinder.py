import os.path
from os.path import exists

from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec


class SynonymsFinder:

    def __init__(self, top_n:int, min_threshold:float):
        project_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
        glove_w2v_file = os.path.join(project_dir, 'glove.6B.100d.word2vec.txt')
        glove_file = os.path.join(project_dir, 'glove.6B.100d.txt')

        if not (exists(glove_w2v_file)):
            glove2word2vec(glove_file, glove_w2v_file)
        self.w2v_model:KeyedVectors = KeyedVectors.load_word2vec_format(glove_w2v_file)

        self.top_n:int = top_n
        self.min_threshold:float = min_threshold

    def find_synonyms_for_word(self, keyword:str)->list:
        try:
            synonyms = self.w2v_model.most_similar(keyword, topn=self.top_n)
            return [synonym for synonym, rate in synonyms if rate >= self.min_threshold]
        except KeyError:
            return []

    def find_synonyms(self, keywords:list)->list:
        synonyms = []

        for keyword in keywords:
            synonyms += self.find_synonyms_for_word(keyword=keyword)

        return synonyms
