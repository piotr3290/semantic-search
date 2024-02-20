from os.path import exists
from keybert import KeyBERT
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec


def load_glove_word2vec():
    glove2word2vec('glove.6B.100d.txt', 'glove.6B.100d.word2vec.txt')


if __name__ == '__main__':
    if not(exists('glove.6B.100d.word2vec.txt')):
        load_glove_word2vec()

    model = KeyedVectors.load_word2vec_format('glove.6B.100d.word2vec.txt')

    search_phrase = 'Semantic search algorithm in text documents'

    kw_model = KeyBERT()

    keywords = kw_model.extract_keywords(search_phrase)
    print(f"Selected Keywords: {keywords}")

    synonyms = {}

    for keyword, _ in keywords:
        try:
            similar_words = model.most_similar(keyword, topn=5)
            synonyms[keyword] = [word for word, _ in similar_words]
        except KeyError:
            synonyms[keyword] = []

    for keyword, synonym_list in synonyms.items():
        print(f"Synonyms for {keyword}: {', '.join(synonym_list)}")
