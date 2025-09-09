import json
import time

from app.TextSearcher import TextSearcher

with open('scifact_20.json', 'r', encoding='utf-8') as file:
    queries_20 = json.load(file)

with open('scifact_100.json', 'r', encoding='utf-8') as file:
    queries_100 = json.load(file)

text_searcher = TextSearcher(keywords_top_n=5, keywords_min_threshold=0.1, synonyms_top_n=5, synonyms_min_threshold=0.6)

def check(queries, label):
    processing_start_time = time.time()

    for query in queries:
        search_phrase = query['query']
        candidates = query['candidates']
        candidates_sentences = []
        sentences = []
        for candidate in candidates:
            candidate_sentences = text_searcher.tokenize_into_sentences(candidate)
            candidates_sentences.append(candidate_sentences)
            sentences += candidate_sentences

        text_searcher.set_search_phrase(search_phrase)
        filtered_sentences = text_searcher.filter_sentences(sentences)
        filtered_sentences2 = [filtered_sentence for filtered_sentence in filtered_sentences if filtered_sentence[1]]
        hits = text_searcher.calculate_similarity(search_phrase,
                                                  [filtered_sentence[2] for filtered_sentence in filtered_sentences2])

        best_hits = [hit for hit in hits if hit['score'] >= 0.5]
        best_hits_sentences = set()
        for best_hit in best_hits:
            best_hits_sentences.add(filtered_sentences2[best_hit['corpus_id']][2])


    processing_end_time = time.time()

    return {
        "label": label,
        "processing_time": processing_end_time - processing_start_time,
        "query_processing_time": (processing_end_time - processing_start_time) / len(queries),
        "queries_count": len(queries)
    }


if __name__ == '__main__':
    results = []
    results.append(check(queries_20, 20))
    results.append(check(queries_100, 100))
    with open('exp3_res.json', 'w', encoding='utf-8') as file:
        json.dump(results, file, indent=4)