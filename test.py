from os.path import exists
from keybert import KeyBERT
from gensim.models import KeyedVectors
# from gensim.scripts.glove2word2vec import glove2word2vec
import nltk


# from TextSearcher import TextSearcher
import nltk
from nltk.tokenize import word_tokenize


# def load_glove_word2vec():
#     glove2word2vec('glove.6B.100d.txt', 'glove.6B.100d.word2vec.txt')

def find_first_occurrence(text, words):
    tokens = word_tokenize(text)
    print(tokens)
    for i, token in enumerate(tokens):
        if token in words:
            return i, i + 1  # Return start and end index of the word
    return -1, -1  # If none of the words are found

if __name__ == '__main__':
    nltk.download('wordnet')
    # words = ['as', 'sad', 'sdlglkdsjlgljsdgljd']
    # asd = 'asfas,; asfas. as421 a?s s    safsa\nsdg\tsad ashashfas ash asasassa s asasj hasb jhv hg vg vhjoiunk inkjkjnkjuuiiuiuuiiuhiu huukjnsdfknsdf dsfksdknvjkbsdv dsjfbskdbfksd  vskdnfiosoi sdvldsiflenkjfnsdkj dsvkjlsdlfnkdsfndsnv sdjlksdflnsdkjnksdnjgnsd v sdlfsdlgndsngjdsngljkds gds l lsdklfmk;sdlkgnsdlknkg;ksdmglksdlkng sdlkdfklgklnflnkgldkfglk fdl dkdfg;dflkngjlfnlgsdnklklsd sdkflksdnlgkndflgndslkfljdsnlgjlebsdjl dsjklfdsljfsdjlj sdjklsdfnlsdbgljsdjljbsd sd lkfsdljfljdsljnsjldg dslkljksdngfsjdgjbldslkng dsf;kdslkfsdglnsdlkn sdlkfsdljfjkbldsgjlbsd;ng;sklndg sd sdlkgjlsbjldglsjdg sdljsljd lkllksdfjlsdljgsljdbgjds sd sdlkfldsfljsdng sd sd fdslfsdljfsdjgds flkdsljfjldsjblfjdsgsd gljdsfljsljdgkjsdlkgdf g fdglkdsklfgnsdlg sd glsdkgkldsnlglknds gds ljgdslkglknsdglds gldskg k;sdlkgndsjgsd glksdglksdl jgds lkgldsl gsd jg lds gldskgljdsljg sd gds lglkdslj gldsljgds llfksdklgnksd;kg;nks;fgsd lg sdlglkdsjlgljsdgljd fgfdg   '
    # print(find_first_occurrence(asd, words))
    lemmatizer = nltk.wordnet.WordNetLemmatizer()
    print(lemmatizer.lemmatize('tests'))

    # if not (exists('glove.6B.100d.word2vec.txt')):
    #     load_glove_word2vec()
    #
    # model = KeyedVectors.load_word2vec_format('glove.6B.100d.word2vec.txt')
    #
    # search_phrase = 'Semantic search algorithm in text documents'
    #
    # kw_model = KeyBERT()
    #
    # keywords = kw_model.extract_keywords(search_phrase)
    # print(f"Selected Keywords: {keywords}")
    #
    # synonyms = {}
    #
    # for keyword, _ in keywords:
    #     try:
    #         similar_words = model.most_similar(keyword, topn=5)
    #         synonyms[keyword] = [word for word, _ in similar_words]
    #     except KeyError:
    #         synonyms[keyword] = []
    #
    # for keyword, synonym_list in synonyms.items():
    #     print(f"Synonyms for {keyword}: {', '.join(synonym_list)}")
    # searcher = TextSearcher()
    # searcher.search(search_phrase)
