from keybert import KeyBERT


class KeywordsExtractor:
    def __init__(self):
        self.kw_model = KeyBERT()

    def get_keywords(self, search_phrase):
        keywords = self.kw_model.extract_keywords(search_phrase)
        print(f"Selected Keywords: {keywords}")
        return [keyword for keyword, _ in keywords]
