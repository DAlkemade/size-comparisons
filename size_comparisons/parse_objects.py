import json
import os
import pickle

from size_comparisons.scraping.wikipedia import WikiLookupWrapper
from pathlib import Path
import pandas as pd

def parse_entry(line):
    return line.decode("utf-8").strip('\n').strip('\r')


def parse_yolo_file(fname):
    res = []
    with open(fname, 'rb') as input_file:
        for line in input_file:
            res.append(parse_entry(line))
    return res


class InputsParser(object):

    def __init__(self, data_dir: Path = None):
        if data_dir is None:
            path = Path(os.getcwd())
            top_dir = path.parent.parent
            data_dir = top_dir / 'data'
        self.data_dir = data_dir

    def retrieve_names(self):
        return parse_yolo_file(self.data_dir / '9k.names')

    def retrieve_labels(self):
        return parse_yolo_file(self.data_dir / '9k.labels')

    def retrieve_wikipedia_lookups(self) -> WikiLookupWrapper:
        lookups = pickle.load(open(self.data_dir / 'wikipedia_lookups.p', 'rb'))
        return WikiLookupWrapper(lookups)

    def retrieve_google_urls(self) -> dict:
        return pickle.load(open(self.data_dir /  'google_urls.p', 'rb'))

    def retrieve_google_results_html(self) -> dict:
        return pickle.load(open(self.data_dir /  'google_results_html.p', 'rb'))

    def retrieve_regex_scraper_sizes(self) -> dict:
        return pickle.load(open(self.data_dir /  'regex_sizes.p', 'rb'))

    def retrieve_frequencies(self):
        with open(self.data_dir / 'frequencies.json', 'r') as in_file:
            ngram_count_lookup = json.load(in_file)
        return ngram_count_lookup

    def retrieve_test_pairs(self) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / 'test_pairs.txt')


