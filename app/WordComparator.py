class WordComparator:
    def get_word(self, token:str)->str:
        return token


class Stemmer(WordComparator):

    def __init__(self):
        from nltk import SnowballStemmer
        self.model:SnowballStemmer = SnowballStemmer('english')

    def get_word(self, token:str)->str:
        return self.model.stem(token)


class Lemmatizer(WordComparator):

    def __init__(self):
        from nltk import wordnet
        self.model:wordnet.WordNetLemmatizer = wordnet.WordNetLemmatizer()

    def get_word(self, token:str)->str:
        return self.model.lemmatize(token)
