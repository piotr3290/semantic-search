import json
from itertools import product
from concurrent.futures import ProcessPoolExecutor

from app.TextSearcher import TextSearcher

queries_file = 'scifact_20.json'
output_file = 'exp1_res.json'

with open(queries_file, 'r', encoding='utf-8') as file:
    queries = json.load(file)

TEXT_SEARCHER = None

def initialize_text_searcher():
    global TEXT_SEARCHER
    if TEXT_SEARCHER is None:
        TEXT_SEARCHER = TextSearcher()

def check(params):
    global TEXT_SEARCHER
    if TEXT_SEARCHER is None:
        initialize_text_searcher()

    keywords_top_n, keywords_min_threshold, synonyms_top_n, synonyms_min_threshold = params

    TEXT_SEARCHER.reset_words()
    TEXT_SEARCHER.set_filtering_parameters(keywords_top_n, keywords_min_threshold, synonyms_top_n, synonyms_min_threshold)

    counter = 0
    true_positive = 0
    false_positive = 0
    false_negative = 0
    true_negative = 0

    print('q1')
    for query in queries:
        search_phrase = query['query']
        sentences = query['candidates']
        ratings = query['ratings']

        TEXT_SEARCHER.set_search_phrase(search_phrase)
        filtered_sentences = TEXT_SEARCHER.filter_sentences(sentences)

        for i in range(len(filtered_sentences)):
            counter += 1
            if filtered_sentences[i][1] and ratings[i] == 1:
                true_positive += 1
            elif filtered_sentences[i][1] and ratings[i] == 0:
                false_positive += 1
            elif not filtered_sentences[i][1] and ratings[i] == 1:
                false_negative += 1
            elif not filtered_sentences[i][1] and ratings[i] == 0:
                true_negative += 1
    print('q2')

    return {
        "keywords_top_n": keywords_top_n,
        "keywords_min_threshold": keywords_min_threshold,
        "synonyms_top_n": synonyms_top_n,
        "synonyms_min_threshold": synonyms_min_threshold,
        "true_positive": true_positive,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "true_negative": true_negative,
        "total": counter
    }


if __name__ == '__main__':
    with open(queries_file, 'r', encoding='utf-8') as file:
        queries = json.load(file)

    key_words_top_n_list = [1, 3, 5, 8, 10]
    key_words_min_threshold_list = [0.7, 0.5, 0.3, 0.1]
    synonyms_top_n_list = [1, 3, 5, 8, 10]
    synonyms_min_threshold_list = [0.8, 0.7, 0.6, 0.5]

    param_combinations = list(product(key_words_top_n_list, key_words_min_threshold_list, synonyms_top_n_list, synonyms_min_threshold_list))
    total_cases = len(param_combinations)

    result = []

    with ProcessPoolExecutor(initializer=initialize_text_searcher) as executor:
        for case_counter, output in enumerate(executor.map(check, param_combinations), 1):
            result.append(output)

            if case_counter % 10 == 0 or case_counter == total_cases:
                with open(output_file, 'w', encoding='utf-8') as file:
                    json.dump(result, file, indent=4)

            print(f"Completed {case_counter}/{total_cases}", flush=True)
