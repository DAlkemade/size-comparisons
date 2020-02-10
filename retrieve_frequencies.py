import io

def fill_dict(text, dict):
    lines = text.split('\n')
    del text
    for line in lines:
        if len(line) > 0:
            word, freq = line.split('\t')
            dict[word] = freq

def find_containing_file(bigram: str):
    with open('data/frequencies/2gms/2gm.idx', 'rb') as in_file:
        for line in in_file:
            print(line)
    # TODO
    return 'TEMP'



class FrequencyRetriever:


    def __init__(self):
        # TODO: maybe change dicts to lists and use np.searchsorted
        self.unigrams = {}
        self.bigrams = {}
        with io.open('data/frequencies/1gms/vocab', 'r', encoding='utf8') as f:
            text = f.read()
            fill_dict(text, self.unigrams)

    def retrieve_unigram_frequency(self, unigram):
        return self.unigrams[unigram]

    def retrieve_frequency(self, ngram):
        n = len(ngram.split())
        if n == 1:
            return self.retrieve_unigram_frequency(ngram)
        if n == 1:
            return self.retrieve_bigram_frequency_lazy(ngram)
        raise ValueError(f'Tried to retrieve ngram with n = {n}')

    def retrieve_bigram_frequency_lazy(self, target_bigram):
        f = find_containing_file(target_bigram)
        with io.open(f, 'r', encoding='utf8') as f:
            text = f.read()
            lines = text.split('\n')
            for line in lines:
                bigram, freq = line.split('\t')
                if target_bigram == bigram:
                    return freq
        return None




if __name__ == '__main__':
    retriever = FrequencyRetriever()
    print(retriever.retrieve_frequency('apple'))
    # print(retriever.retrieve_frequency('apple pie'))
