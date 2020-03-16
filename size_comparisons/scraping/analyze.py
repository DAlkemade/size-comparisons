import math
from collections import namedtuple
from math import ceil

import numpy as np
import pandas as pd
import tqdm
from matplotlib import pyplot as plt
from nltk.corpus import wordnet as wn
from scipy.stats import norm

from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.wikipedia import is_disambiguation

Entry = namedtuple('Entry', ['label', 'name', 'wiki_exists', 'disambiguation', 'count', 'synset', 'n', 'sizes', 'mean', 'std', 'n_data_points'])


def mean_and_std(sizes: list) -> (float, float):
    if len(sizes) == 0:
        return math.nan, math.nan
    mu, std = norm.fit(sizes)
    return mu, std


def plot_sizes_with_gaussian(sizes: list, title: str):
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
    title = f"{title}: mu = {mu},  std = {std}"
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


def analyze_results(labels: list):
    data = fill_dataframe(labels)
    data.sort_values('count', inplace=True)
    print(f'Fraction of objects with wiki page: {data["wiki_exists"].mean()}')
    print(f'Fraction of disambiguation pages (of total): {data["disambiguation"].mean()}')
    create_hist(data['n'], 'n')

    stds_for_at_least_one_datapoint = data[data['n_data_points'] > 0]['std']
    create_hist(stds_for_at_least_one_datapoint, 'std for n_data_points > 0', max_value=100)

    create_hist(data['n_data_points'], 'n_data_points', max_value=30)


def fill_dataframe(labels):
    # IMPORT DATA
    input_parser = InputsParser()
    names = input_parser.retrieve_names()
    ngram_count_lookup = input_parser.retrieve_frequencies()
    wiki_lookup_wrapper = input_parser.retrieve_wikipedia_lookups()
    sizes_lookup = input_parser.retrieve_regex_scraper_sizes()
    results = []

    for i in tqdm.trange(len(labels)):
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
        n_data_points = len(sizes)
        mean, std = mean_and_std(sizes)
        # plot_sizes_with_gaussian(sizes, name)

        # Add ngram count
        count = None
        if name in ngram_count_lookup.keys():
            count = ngram_count_lookup[name]

        n = check_n(name)
        entry = Entry(label, name, exists, disambiguation, count, synset, n, sizes, mean, std, n_data_points)
        results.append(entry)
    data = pd.DataFrame(results)
    return data


def create_hist(values: list, title: str, max_value=None) -> None:
    """Plot histogram for a column of a dataframe.

    If a max_value is given, all values larger than that value are binned together in the last bin.
    """
    if max_value is None:
        max_value = ceil(np.amax(values))
    bins = range(0, max_value)
    plt.hist(np.clip(values, bins[0], bins[-1]), bins=bins)
    plt.title(title)
    plt.show()