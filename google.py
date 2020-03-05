import os
import pickle

import tqdm
from googlesearch import search


def retrieve_query(query: str) -> list:
    results_generator = search(query, tld="com", num=10, stop=10, pause=2)
    return list(results_generator)


def retrieve_google_results(results: dict, queries: list, keys: list):
    for i in tqdm.trange(len(queries)):
        name = queries[i]
        label = keys[i]
        results[label] = retrieve_query(name)
    return results


def create_or_update_results(file_path: str, queries: list, keys: list):

    try:
        file = open(file_path, 'rb')
        results = pickle.load(file)
    except (EOFError, FileNotFoundError):
        print("No previous results, creating new object")
        results = dict()

    try:
        retrieve_google_results(results, queries, keys)
    except Exception as e: #TODO specify error (403 http)
        print(e)
        print("Something went wrong, saving intermediate result")

    pickle.dump(results, open(file_path, 'wb'))