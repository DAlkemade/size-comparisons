import math
import os
from collections import namedtuple

import numpy as np
import pandas as pd
import tqdm
from scipy.stats import norm
from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.wikipedia import is_disambiguation
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import LocalOutlierFactor
import logging

logger = logging.getLogger(__name__)


def fill_dataframe(names: list, labels: list, remove_outliers=True, remove_zeroes=True, debug=False,
                   datadir: str = None):
    """Compile a dataframe of scraped data for further analysis."""
    # IMPORT DATA
    input_parser = InputsParser(data_dir=datadir)
    potential_fname = input_parser.data_dir / "parsed_data.pkl"
    if os.path.exists(potential_fname):
        logger.info('LOADING CACHED DATAFRAME')
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
                logger.info(f'valid: {valid}')
                logger.info(f'invalid: {invalid}')

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
        logger.info(f"WARNING: {envelope_errors} value errors while removing outliers")
    data = pd.DataFrame(results)
    data.to_pickle(potential_fname)
    return data


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


def check_n(token: str) -> int:
    """Checks n (as in n-gram) of a token.

    :param token: token to be checked
    :return: int n
    """
    return len(token.split(' '))