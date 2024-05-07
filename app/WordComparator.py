from nltk import SnowballStemmer, wordnet


class WordComparator:
    def get_word(self, token):
        return token


class Stemmer(WordComparator):

    def __init__(self):
        self.model = SnowballStemmer('english')

    def get_word(self, token):
        return self.model.stem(token)


class Lemmatizer(WordComparator):

    def __init__(self):
        self.model = wordnet.WordNetLemmatizer()

    def get_word(self, token):
        return self.model.lemmatize(token)
