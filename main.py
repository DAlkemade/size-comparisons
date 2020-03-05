import argparse
import json
from collections import namedtuple

import nltk
import numpy as np
import pandas as pd
import tqdm
from matplotlib import pyplot as plt
from nltk.corpus import wordnet as wn

import parse_objects
from lengths_regex import LengthsFinderRegex
from wikipedia import is_disambiguation, WikiLookupWrapper

nltk.download('wordnet')

Entry = namedtuple('Entry', ['wiki_exists', 'disambiguation', 'count', 'synset', 'n'])


# TODO: think about 3-grams (body of water)


def check_n(token: str) -> int:
    """
    Check n (as in n-gram) of a token
    :param token: token to be checked
    :return: int n
    """
    return len(token.split(' '))


def print_some_info_on_synset(wiki, synset_string: str) -> None:
    """
    Display some possiblities of the wordnet library.
    :param synset_string: Exact synset string
    """
    apple = wn.synset(synset_string)
    print(apple.definition())
    print(apple.hypernyms())
    print(apple.lexname())
    apple_lookup = wiki.page('apple')
    print(apple_lookup.langlinks)


def retrieve_synset(label: str):
    """
    Retrieve synset using a wordnet id.
    :param label: wordnet id
    :return: wordnet synset
    """
    pos = label[0]
    offset = int(label[1:])
    return wn.synset_from_pos_and_offset(pos, offset)


def main(test: bool):
    # IMPORT DATA
    names = parse_objects.retrieve_names()
    labels = parse_objects.retrieve_labels()
    with open('data/frequencies.json', 'r') as in_file:
        ngram_count_lookup = json.load(in_file)

    wiki_lookups = parse_objects.retrieve_wikipedia_lookups()
    wiki_lookup_wrapper = WikiLookupWrapper(wiki_lookups)
    # Reduce data if text
    if test:
        test_n = 10
        names = names[:test_n]
        labels = labels[:test_n]
    # CHECK IF WIKIPEDIA PAGE EXISTS AND RETRIEVE TEXT

    results = []
    for i in tqdm.trange(len(names)):
        # Get name and label
        name = names[i]
        label = labels[i]

        # Retrieve synset
        synset = retrieve_synset(label)
        # synsets_all_for_string.append(wn.synsets(name.replace(' ', '_')))

        # Wikipedia entry
        lookup = wiki_lookup_wrapper.lookup(label)
        exists = lookup.exists()

        disambiguation = is_disambiguation(lookup)

        # Find all lengths
        if exists and not disambiguation:
            regex_matcher = LengthsFinderRegex(lookup.text)
            all_lengths_in_article = regex_matcher.find_all_matches()

        # Add ngram count
        count = None
        if name in ngram_count_lookup.keys():
            count = ngram_count_lookup[name]

        n = check_n(name)
        entry = Entry(exists, disambiguation, count, synset, n)
        results.append(entry)

    data = pd.DataFrame(results)
    data.sort_values('count', inplace=True)
    print(f'Fraction of objects with wiki page: {data["wiki_exists"].mean()}')
    print(f'Fraction of disambiguation pages (of total): {data["disambiguation"].mean()}')
    plt.hist(data['n'], bins=range(0, np.amax(data['n'])))
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', type=bool, default=False)
    args = parser.parse_args()
    main(args.test)
