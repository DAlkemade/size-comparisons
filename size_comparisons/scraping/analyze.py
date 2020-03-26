import math
from collections import namedtuple
from math import ceil

import numpy as np
import pandas as pd
import tqdm
from matplotlib import pyplot as plt
from nltk.corpus import wordnet as wn
from scipy.stats import norm
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import LocalOutlierFactor

from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.wikipedia import is_disambiguation

Entry = namedtuple('Entry',
                   ['label', 'name', 'wiki_exists', 'disambiguation', 'count', 'synset', 'n', 'sizes', 'mean', 'std',
                    'n_data_points'])


def mean_and_std(sizes: list) -> (float, float):
    """Finds the mean and standard deviation of a normal distribution fit on a list of observations."""
    if len(sizes) == 0:
        return math.nan, math.nan
    mu, std = norm.fit(sizes)
    return mu, std


def plot_sizes_with_gaussian(sizes: list, title: str):
    """Plots sizes and shows gaussian.
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
    """Checks n (as in n-gram) of a token.

    :param token: token to be checked
    :return: int n
    """
    return len(token.split(' '))


def print_some_info_on_synset(wiki, synset_string: str) -> None:
    """Displays some possiblities of the wordnet library.

    :param synset_string: Exact synset string
    """
    apple = wn.synset(synset_string)
    print(apple.definition())
    print(apple.hypernyms())
    print(apple.lexname())
    apple_lookup = wiki.page('apple')
    print(apple_lookup.langlinks)


def retrieve_synset(label: str):
    """Retrieves synset using a wordnet id.

    :param label: wordnet id
    :return: wordnet synset
    """
    pos = label[0]
    offset = int(label[1:])
    return wn.synset_from_pos_and_offset(pos, offset)


def analyze_results(labels: list):
    """Compiles scraped data and print and plot some key result."""
    data = fill_dataframe(labels, remove_outliers=True, remove_zeroes=True)
    data.sort_values('count', inplace=True)
    print(f'Fraction of objects with wiki page: {data["wiki_exists"].mean()}')
    print(f'Fraction of disambiguation pages (of total): {data["disambiguation"].mean()}')
    create_hist(data['n'], 'n')

    stds_for_at_least_one_datapoint = data[data['n_data_points'] > 0]['std']
    create_hist(stds_for_at_least_one_datapoint, 'std for n_data_points > 0', max_value=100)

    create_hist(data['n_data_points'], 'n_data_points', max_value=30)

    data_with_suff_high_n = data[data['n_data_points'] > 5]

    nlargest = data_with_suff_high_n.nlargest(10, ['mean'])
    print_relevant_columns(nlargest, 'largest')

    nsmallest = data_with_suff_high_n.nsmallest(10, ['mean'])
    print_relevant_columns(nsmallest, 'smallest')

    print(f'Mean std: {data["std"].mean()}')
    print(f'Median std: {data["std"].median()}')
    print(f'Mean mean: {data["mean"].mean()}')
    print(f'Median mean: {data["mean"].median()}')


def print_relevant_columns(df: pd.DataFrame, label: str):
    print(f'{label}: \n{df[["name", "mean", "std", "n_data_points"]]}')


def fill_dataframe(labels: list, remove_outliers=True, remove_zeroes=True, debug=False):
    """Compile a dataframe of scraped data for further analysis."""
    # IMPORT DATA
    input_parser = InputsParser()
    names = input_parser.retrieve_names()
    ngram_count_lookup = input_parser.retrieve_frequencies()
    wiki_lookup_wrapper = input_parser.retrieve_wikipedia_lookups()
    sizes_lookup = input_parser.retrieve_regex_scraper_sizes()
    results = []
    value_errors = 0

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
        if remove_zeroes:
            new_sizes = []
            for size in sizes:
                if size > 0.:
                    new_sizes.append(size)
            sizes = new_sizes
        if remove_outliers and len(sizes) > 2:
            # Create detector
            outlier_detector = EllipticEnvelope(contamination=.1)
            sizes_array = np.reshape(sizes, (-1, 1))
            try:
                # Fit detector
                outlier_detector.fit(sizes_array)
                preds = outlier_detector.predict(sizes_array)

                # Predict outliers


            except (ValueError, RuntimeWarning):
                clf = LocalOutlierFactor(n_neighbors=min(5, len(sizes_array) - 1), contamination=0.1)
                preds = clf.fit_predict(sizes_array)
                value_errors += 1

            valid = np.extract(preds == 1, sizes_array)
            sizes = list(valid)
            if name == 'cheese':
                print(sizes)
            if debug:
                valid = np.sort(valid)
                invalid = np.extract(preds == -1, sizes_array)
                invalid = np.sort(invalid)
                print(f'valid: {valid}')
                print(f'invalid: {invalid}')

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

    if value_errors > 0:
        print(f"WARNING: {value_errors} value errors while removing outliers")
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
