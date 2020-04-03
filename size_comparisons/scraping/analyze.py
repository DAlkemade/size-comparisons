from math import ceil

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from nltk.corpus import wordnet as wn
from scipy.stats import norm
from size_comparisons.scraping.compilation import fill_dataframe, mean_and_std


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
    """Plot and print interesting features of the objects dataframe."""
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
    # TODO filter for wikipedia count > 100
    data_selected.to_csv('data_selected.csv')

    print("Statistics selected data")
    print_statistics(data_selected)


def print_relevant_columns(df: pd.DataFrame, label: str):
    """Print some relevant columns of the dataframe."""
    print(f'{label}: \n{df[["name", "mean", "std", "n_data_points", "label"]]}')


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
