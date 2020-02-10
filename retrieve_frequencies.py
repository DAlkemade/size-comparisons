import io


class FrequencyRetriever:

    def __init__(self):
        self.unigrams = {}  # TODO: maybe change to list and use np.searchsorted to find unigram
        with io.open('data/frequencies/1gms/vocab', 'r', encoding='utf8') as f:
            text = f.read()
            lines = text.split('\n')
            del text
            for line in lines:
                if len(line) > 0:
                    word, freq = line.split('\t')
                    self.unigrams[word] = freq

    def retrieve_unigram_frequency(self, unigram):
        return self.unigrams[unigram]

    def retrieve_frequency(self, ngram):
        n = len(ngram.split())
        if n == 1:
            return self.retrieve_unigram_frequency(ngram)
        # TODO
        return None


if __name__ == '__main__':
    retriever = FrequencyRetriever()
    print(retriever.retrieve_frequency('apple'))
