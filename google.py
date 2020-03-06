import pickle

import requests
import tqdm
from googlesearch import search
import asyncio
import aiohttp


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


async def retrieve_htmls_for_object(label, results, urls):
    print("Start for new label")
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
                if r.status_code == 200:
                    htmls.append(r.text)
                else:
                    print(f"No statuscode 200 for url {url}")
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
        gather_htmls(results, keys, urls)
    except Exception as e:  # TODO specify error (403 http)
        print(e)
        print("Something went wrong, saving intermediate result")

    pickle.dump(results, open(file_path, 'wb'))


async def request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()


async def main(results: dict, labels: list, urls: dict):
    results = await asyncio.gather(
        *[retrieve_htmls_for_object(label, results, urls) for label in labels]
    )
    print(len(results))
    print(results)


def gather_htmls(results, keys, urls: dict):
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(results, keys, urls))
        loop.run_until_complete(loop.shutdown_asyncgens())
    finally:
        loop.close()
