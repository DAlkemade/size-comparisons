import os
import pickle

from thesis_scraper.wikipedia import WikiLookupWrapper


def parse_entry(line):
    return line.decode("utf-8").strip('\n')


def parse_yolo_file(fname):
    res = []
    with open(fname, 'rb') as input_file:
        for line in input_file:
            res.append(parse_entry(line))
    return res


def retrieve_names():
    return parse_yolo_file('data/9k.names')


def retrieve_labels():
    return parse_yolo_file('data/9k.labels')


def retrieve_wikipedia_lookups() -> WikiLookupWrapper:
    lookups =  pickle.load(open(os.path.join('data', 'wikipedia_lookups.p'), 'rb'))
    return WikiLookupWrapper(lookups)

def retrieve_google_results_html() -> dict:
    return pickle.load(open(os.path.join('data', 'google_results_html.p'), 'rb'))


def retrieve_regex_scraper_sizes() -> dict:
    return pickle.load(open(os.path.join('data', 'regex_sizes.p'), 'rb'))

