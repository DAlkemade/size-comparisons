import argparse
import json
from collections import namedtuple

import nltk
import numpy as np
import pandas as pd
import tqdm
from matplotlib import pyplot as plt
import matplotlib.mlab as mlab
from nltk.corpus import wordnet as wn
from scipy.stats import norm

import parse_objects
from lengths_regex import LengthsFinderRegex
from wikipedia import is_disambiguation, WikiLookupWrapper

nltk.download('wordnet')

Entry = namedtuple('Entry', ['wiki_exists', 'disambiguation', 'count', 'synset', 'n', 'sizes'])


# TODO: think about 3-grams (body of water)

def mean_and_std(sizes: list):
    mu, std = norm.fit(sizes)
    return mu, std


def plot_sizes_with_gaussian(sizes: list):
    """Plot sizes and show gaussian.
    From https://stackoverflow.com/a/20012350"""
    data = sizes
    mu, std = mean_and_std(sizes)
    plt.hist(data, bins=25, density=True, alpha=0.6, color='g')

    # Plot the PDF.
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
    plt.title(title)

    plt.show()


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

    sizes_lookup = parse_objects.retrieve_regex_scraper_sizes()
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

        sizes = sizes_lookup[label]

        # Add ngram count
        count = None
        if name in ngram_count_lookup.keys():
            count = ngram_count_lookup[name]

        n = check_n(name)
        entry = Entry(exists, disambiguation, count, synset, n, sizes)
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
