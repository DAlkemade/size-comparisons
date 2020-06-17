import logging
import pickle

import tqdm
from googlesearch import search  # this is the package 'google'

logger = logging.getLogger(__name__)

NUM_RESULTS = 7

logger = logging.getLogger(__name__)


def retrieve_query(query: str) -> list:
    """Retrieve URLs from google with certain parameters."""
    results_generator = search(query, tld="com", num=NUM_RESULTS, stop=NUM_RESULTS, pause=2)
    return list(results_generator)


def retrieve_google_results(results: dict, queries: list, keys: list):
    """Retrieve URLs from google for a list of queries and update these results INPLACE in results dict."""
    for i in tqdm.trange(len(queries)):
        queries_list = queries[i]
        label = keys[i]
        if label not in results.keys():
            results[label] = []
            for query in queries_list:
                results[label] = results[label] + retrieve_query(query)


def create_or_update_results(file_path: str, queries: list, keys: list):
    """Update (or create) file with google search query results."""

    try:
        file = open(file_path, 'rb')
        results = pickle.load(file)
    except (EOFError, FileNotFoundError):
        logger.info("No previous results, creating new object")
        results = dict()

    try:
        retrieve_google_results(results, queries, keys)
    except Exception as e:  # TODO specify error (403 http)
        logger.exception("Something went wrong, saving intermediate result")

    pickle.dump(results, open(file_path, 'wb'))
    return results
