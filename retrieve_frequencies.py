import io
import json
import os

import tqdm

import parse_objects


class FrequencyRetriever:
    """
    Loop over unigram and bigram frequency files and return frequencies for a set of ngrams.
    """

    def __init__(self, targets: set, work_dir='data/frequencies/'):
        # TODO: maybe change dicts to lists and use np.searchsorted
        self.work_dir = work_dir
        self.ngrams = {}
        self.targets = targets

    def run(self):
        """
        Do a single scan over all files
        :return: dict with key=ngram and value=frequency
        """
        self._scan_file_for_ngrams('1gms/vocab')
        self._scan_bigrams()
        return self.ngrams

    def _find_bigram_files(self):
        files = []
        with io.open(os.path.join(self.work_dir, '2gms/2gm.idx'), 'r', encoding='utf8') as f:
            text = f.read()
            lines = text.split('\n')
            for line in lines:
                if len(line) > 0:
                    files.append(line[:8])
        return files

    def _scan_file_for_ngrams(self, fname):
        with io.open(os.path.join(self.work_dir, fname), 'r', encoding='utf8') as f:
            text = f.read()
            self._find_freqs(text)

    def _find_freqs(self, text):
        lines = text.split('\n')
        del text
        for line in lines:
            if len(line) > 0:
                word, freq = line.split('\t')
                if word in self.targets:  # should be O(1) with hashset
                    # print(f'Found word {word} with freq {freq}')
                    self.ngrams[word] = freq

    def _scan_bigrams(self):
        bigram_files = self._find_bigram_files()
        print("Scanning bigrams")
        for i in tqdm.trange(len(bigram_files)):
            file = bigram_files[i]
            self._scan_file_for_ngrams(os.path.join('2gms', file))


if __name__ == '__main__':
    names = parse_objects.retrieve_names()
    retriever = FrequencyRetriever(set(names))
    freqs = retriever.run()
    count = 0
    for name in names:
        if name in freqs.keys():
            count += 1
    frac_found = count / len(names)
    print(f'Found the frequency for fraction {frac_found}')

    # Save json
    with open('frequencies.json', 'w') as wf:
        json.dump(freqs, wf)
