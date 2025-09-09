import json


from app.TextSearcher import TextSearcher

with open('scifact_20.json', 'r', encoding='utf-8') as file:
    queries = json.load(file)
text_searcher = TextSearcher(keywords_top_n=5, keywords_min_threshold=0.1, synonyms_top_n=5, synonyms_min_threshold=0.6)

def check(min_threshold):
    counter = 0
    true_positive = 0
    false_positive = 0
    false_negative = 0
    true_negative = 0

    for query in queries:
        search_phrase = query['query']
        candidates = query['candidates']
        candidates_sentences = []
        sentences = []
        for candidate in candidates:
            candidate_sentences = text_searcher.tokenize_into_sentences(candidate)
            candidates_sentences.append(candidate_sentences)
            sentences += candidate_sentences

        ratings = query['ratings']

        hits = text_searcher.calculate_similarity(search_phrase, sentences)

        best_hits = [hit for hit in hits if hit['score'] >= min_threshold]
        best_hits_sentences = set()
        for best_hit in best_hits:
            best_hits_sentences.add(sentences[best_hit['corpus_id']])

        for i in range(len(candidates_sentences)):
            is_hit = not best_hits_sentences.isdisjoint(candidates_sentences[i])
            counter += 1
            if is_hit and ratings[i] == 1:
                true_positive += 1
            elif is_hit and ratings[i] == 0:
                false_positive += 1
            elif not is_hit and ratings[i] == 1:
                false_negative += 1
            elif not is_hit and ratings[i] == 0:
                true_negative += 1

    return {
        "min_threshold": min_threshold,
        "true_positive": true_positive,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "true_negative": true_negative,
        "total": counter
    }


if __name__ == '__main__':
    min_thresholds = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]
    results = []
    for j in range(len(min_thresholds)):
        print('start', j)
        results.append(check(min_thresholds[j]))
    with open('exp2_sbert_res.json', 'w', encoding='utf-8') as file:
        json.dump(results, file, indent=4)