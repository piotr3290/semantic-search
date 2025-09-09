from sentence_transformers import util


class SemanticComparator:
    def __init__(self, embeddings):
        self.embeddings = embeddings

    def calculate_similarity(self, search_sentence:str, corpus:list)->list:
        if len(corpus) == 0:
            return []
        embeddings_search_sentence = self.embeddings.encode([search_sentence], convert_to_tensor=True).to("cuda")
        embeddings_search_sentence = util.normalize_embeddings(embeddings_search_sentence)

        embeddings_corpus = self.embeddings.encode(corpus, convert_to_tensor=True).to("cuda")
        embeddings_corpus = util.normalize_embeddings(embeddings_corpus)

        similarities = util.semantic_search(embeddings_search_sentence, embeddings_corpus, score_function=util.dot_score, top_k=20)
        return similarities[0]