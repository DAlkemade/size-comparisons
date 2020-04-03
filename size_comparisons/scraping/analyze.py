import math
import os
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
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import LocalOutlierFactor

Entry = namedtuple('Entry',
                   ['label', 'name', 'wiki_exists', 'disambiguation', 'count', 'count_wiki', 'n', 'sizes',
                    'mean', 'std',
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


def print_statistics(data: pd.DataFrame):
    total_data_points = np.sum(data['sizes'].str.len())
    print(f'Total number of found data points: {total_data_points}')
    print(f'Number of objects: {len(data.index)}')
    stds_for_at_least_one_datapoint = data[data['n_data_points'] > 0]['std']
    create_hist(stds_for_at_least_one_datapoint, 'std for n_data_points > 0', max_value=100)

    create_hist(data['n_data_points'], 'n_data_points', max_value=30)

    data_with_suff_high_n = data[data['n_data_points'] > 5]

    nlargest = data_with_suff_high_n.nlargest(10, ['mean'])
    print_relevant_columns(nlargest, 'largest')

    nsmallest = data_with_suff_high_n.nsmallest(10, ['mean'])
    print_relevant_columns(nsmallest, 'smallest')

    print(f'std | mean: {data["std"].mean()} | median: {data["std"].median()}')
    print(f'Mean | mean: {data["mean"].mean()} | median: {data["mean"].median()}')
    print(f'Count | mean: {data["count"].mean()} | median: {data["count"].median()}')


def analyze_results(labels: list, names: list):
    """Compiles scraped data and print and plot some key result."""
    data = fill_dataframe(names, labels, remove_outliers=True, remove_zeroes=True)
    data.sort_values('mean', inplace=True)
    print(f'Fraction of objects with wiki page: {data["wiki_exists"].mean()}')
    print(f'Fraction of disambiguation pages (of total): {data["disambiguation"].mean()}')
    create_hist(data['n'], 'n')

    create_hist(data['count_wiki'], 'wikipedia counts', max_value=30000, nr_bins=200)
    create_hist(data['count_wiki'], 'wikipedia counts', max_value=1000, nr_bins=200)
    counts_zero = len(data[data['count_wiki'] == 0].values)
    print(f'#objects with 0 hits on wikipedia: {counts_zero}')

    print("Statistics all data:")
    print_statistics(data)
    data.to_csv('data_full.csv')

    data['std_relative'] = data['std'] / data['mean']
    data.sort_values('mean', inplace=True)
    data_selected = data[data['std_relative'] < .5]
    n_unique_sizes = [len(set(row['sizes'])) for index, row in data_selected.iterrows()]
    data_selected['n_sizes_unique'] = n_unique_sizes
    data_selected = data_selected[data_selected['n_sizes_unique'] > 5]
    data_selected.to_csv('data_selected.csv')

    print("Statistics selected data")
    print_statistics(data_selected)


def print_relevant_columns(df: pd.DataFrame, label: str):
    print(f'{label}: \n{df[["name", "mean", "std", "n_data_points", "label"]]}')


def fill_dataframe(names: list, labels: list, remove_outliers=True, remove_zeroes=True, debug=False,
                   datadir: str = None):
    """Compile a dataframe of scraped data for further analysis."""
    # IMPORT DATA
    input_parser = InputsParser(data_dir=datadir)
    potential_fname = input_parser.data_dir / "parsed_data.pkl"
    if os.path.exists(potential_fname):
        print('LOADING CACHED DATAFRAME')
        return pd.read_pickle(potential_fname)
    ngram_count_lookup = input_parser.retrieve_frequencies()
    counts_wikipedia = input_parser.retrieve_frequencies(wikipedia=True)
    wiki_lookup_wrapper = input_parser.retrieve_wikipedia_lookups()
    sizes_lookup = input_parser.retrieve_regex_scraper_sizes()
    results = []
    envelope_errors = 0

    for i in tqdm.trange(len(labels)):
        # Get name and label
        name = names[i]
        label = labels[i]

        # Retrieve synset
        # synset = retrieve_synset(label)

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
            with np.errstate(all='raise'):
                try:
                    # Fit detector
                    outlier_detector.fit(sizes_array)
                    preds = outlier_detector.predict(sizes_array)

                    # Predict outliers


                except (ValueError, RuntimeWarning, FloatingPointError):
                    # Backoff: use LocalOutlierFActor outlier removal
                    clf = LocalOutlierFactor(n_neighbors=min(5, len(sizes_array) - 1), contamination=0.1)
                    preds = clf.fit_predict(sizes_array)
                    envelope_errors += 1

            valid = np.extract(preds == 1, sizes_array)
            sizes = list(valid)

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
            count = int(ngram_count_lookup[name])

        count_wiki = None
        if name in counts_wikipedia.keys():
            count_wiki = int(counts_wikipedia[name])

        n = check_n(name)
        entry = Entry(label, name, exists, disambiguation, count, count_wiki, n, sizes, mean, std,
                      n_data_points)
        results.append(entry)

    if envelope_errors > 0:
        print(f"WARNING: {envelope_errors} value errors while removing outliers")
    data = pd.DataFrame(results)
    data.to_pickle(potential_fname)
    return data

def create_hist(values: list, title: str, max_value=None, debug=False, nr_bins=None) -> None:
    """Plot histogram for a column of a dataframe.

    If a max_value is given, all values larger than that value are binned together in the last bin.
    """
    if max_value is None:
        max_value = ceil(np.amax(values))
    if nr_bins is None:
        nr_bins = max_value
    bins = np.linspace(0, max_value, nr_bins)
    if debug:
        print(f'create hist for {title}')
    plt.hist(np.clip(values, bins[0], bins[-1]), bins=bins)
    plt.title(title)
    plt.show()
