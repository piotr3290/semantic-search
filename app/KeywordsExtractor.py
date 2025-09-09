from keybert import KeyBERT


class KeywordsExtractor:
    def __init__(self, top_n:int, min_threshold:float, model):
        self.kw_model = KeyBERT(model=model)
        self.top_n = top_n
        self.min_threshold = min_threshold

    def get_keywords(self, search_phrase:str)->list:
        keywords = self.kw_model.extract_keywords(search_phrase, top_n=self.top_n, use_mmr=True)
        return [keyword for keyword, rate in keywords if rate >= self.min_threshold]
