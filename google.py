import pickle
import pprint
from _ssl import SSLCertVerificationError
from collections import namedtuple

import requests
import tqdm
from googlesearch import search
import asyncio
import aiohttp

pp = pprint.PrettyPrinter()

NUM_RESULTS = 10

ObjectURL = namedtuple('ObjectURL', ['url', 'index', 'label'])


def retrieve_query(query: str) -> list:
    """Retrieve URLs from google with certain parameters."""
    results_generator = search(query, tld="com", num=NUM_RESULTS, stop=NUM_RESULTS, pause=2)
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

    # try:
    gather_htmls(results, keys, urls)
    # except Exception as e:  # TODO specify error (403 http)
    #     print(e)
    #     print("Something went wrong, saving intermediate result")

    pickle.dump(results, open(file_path, 'wb'))


async def request(url_obj: ObjectURL):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url_obj.url) as resp:
                return await resp.content.read(), url_obj
        except Exception as e:
            print(f"\nSomething went wrong retrieving url {url_obj.url}")
            return None, url_obj


async def main(results: dict, labels: list, urls_lookup: dict):
    urls_list = []
    labels = labels[:10]
    for label in labels:
        if label not in results.keys():
            urls_for_object = urls_lookup[label]
            for i, url in enumerate(urls_for_object):
                url_obj = ObjectURL(url, i, label)
                urls_list.append(url_obj)

    tasks = [request(url_obj) for url_obj in urls_list]

    results_list = [await f for f in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks))]
    # results_list = await asyncio.gather(
    #     *[request(url_obj) for url_obj in urls_list]
    # )

    for html, url_obj in results_list:
        if url_obj.label not in results.keys():
            results[url_obj.label] = [None] * NUM_RESULTS
        results[url_obj.label][url_obj.index] = html


    pp.pprint(results_list)
    pp.pprint(results)


def gather_htmls(results, keys, urls_lookup: dict):
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(results, keys, urls_lookup))
        loop.run_until_complete(loop.shutdown_asyncgens())
    finally:
        loop.close()
