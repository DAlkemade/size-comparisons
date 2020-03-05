import os
import pickle

import tqdm
from googlesearch import search
import requests
from urllib3.exceptions import NewConnectionError


def retrieve_query(query: str) -> list:
    """Retrieve URLs from google with certain parameters."""
    results_generator = search(query, tld="com", num=10, stop=10, pause=2)
    return list(results_generator)


def retrieve_google_results(results: dict, queries: list, keys: list):
    """Retrieve URLs from google for a list of queries and update these results INPLACE in results dict."""
    for i in tqdm.trange(len(queries)):
        name = queries[i]
        label = keys[i]
        if label not in results.keys():
            results[label] = retrieve_query(name)


def create_or_update_results(file_path: str, queries: list, keys: list):
    """Update (or create) file with google search query results."""

    try:
        file = open(file_path, 'rb')
        results = pickle.load(file)
    except (EOFError, FileNotFoundError):
        print("No previous results, creating new object")
        results = dict()

    try:
        retrieve_google_results(results, queries, keys)
    except Exception as e:  # TODO specify error (403 http)
        print(e)
        print("Something went wrong, saving intermediate result")

    pickle.dump(results, open(file_path, 'wb'))


def retrieve_htmls(results, labels, urls: dict):
    for i in tqdm.trange(len(labels)):
        label = labels[i]
        if label not in results.keys():
            htmls = []
            try:
                urls_for_name = urls[label]
            except KeyError:
                print(f"URLs not available for label {label}")
                urls_for_name = None
            for url in urls_for_name:
                try:
                    r = requests.get(url)
                    print(r)
                    htmls.append(r)
                except Exception as e:
                    print(f'Couldnt find url {url}, {e}')

            results[label] = htmls


def create_or_update_urls_html(file_path: str, keys: list, urls: dict):
    """Update (or create) file with html from urls."""
    try:
        file = open(file_path, 'rb')
        results = pickle.load(file)
    except (EOFError, FileNotFoundError):
        print("No previous results, creating new object")
        results = dict()

    try:
        retrieve_htmls(results, keys, urls)
    except Exception as e:  # TODO specify error (403 http)
        print(e)
        print("Something went wrong, saving intermediate result")

    pickle.dump(results, open(file_path, 'wb'))
