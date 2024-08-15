from app.TextSearcher import TextSearcher

if __name__ == '__main__':
    print('Console App')
    text_searcher = TextSearcher()
    search_phrase = 'That is a happy person'
    text_searcher.set_search_phrase(search_phrase)
#     sentences = text_searcher.tokenize_into_sentences("""We read the file in chunks of a specified buffer size (buffer_size), reducing memory usage compared to reading the entire file at once. We perform the search within each chunk individually rather than loading the entire file into memory, which is more efficient for large files.
# We stop searching after finding the first occurrence of the keyword to optimize performance.
# Adjust the buffer_size according to the size of your files and available memory. Larger buffer sizes can improve performance but may consume more memory.
# Experiment with different values to find the optimal balance for your specific use case.""")
#     sentences = text_searcher.tokenize_into_sentences("That is a happy dog. That is a very happy person. Today is a sunny day.")
    filtered_sentences = text_searcher.filter_sentences(["That is a happy dog", "That is a very happy person", "Today is a sunny day"])
    filtered_sentences2 = [filtered_sentence for filtered_sentence in filtered_sentences if filtered_sentence[1]]
    print('filtered_sentences')
    print(filtered_sentences)
    sim = text_searcher.calculate_similarity(search_phrase,
                                             [filtered_sentence[2] for filtered_sentence in filtered_sentences])
    a = [((tup.item(), ) + elem) for tup, elem in zip(sim, filtered_sentences2)]
    print(a)
