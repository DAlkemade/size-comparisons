import asyncio
import pickle
import pprint
from _ssl import SSLCertVerificationError
from collections import namedtuple

import aiohttp
import tqdm
from googlesearch import search

pp = pprint.PrettyPrinter()

NUM_RESULTS = 10

ObjectURL = namedtuple('ObjectURL', ['url', 'index', 'label', 'position_in_order'])


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


def create_or_update_urls_html(file_path: str, keys: list, urls: dict, asyncio_loop):
    """Update (or create) file with html from urls."""
    try:
        file = open(file_path, 'rb')
        results = pickle.load(file)
    except (EOFError, FileNotFoundError):
        print("No previous results, creating new object")
        results = dict()

    # try:
    gather_htmls(results, keys, urls, asyncio_loop)
    # except Exception as e:  # TODO specify error (403 http)
    #     print(e)
    #     print("Something went wrong, saving intermediate result")

    pickle.dump(results, open(file_path, 'wb'))


async def request(url_obj: ObjectURL, sem):
    async with sem, aiohttp.ClientSession() as session:
        print(f'Request {url_obj.position_in_order}')
        try:
            async with session.get(url_obj.url) as resp:
                # TODO only reads html, not pdfs
                print('Worked')
                return await resp.text(), url_obj, resp.status
        except UnicodeDecodeError as e:
            print(f"{url_obj.url} is not HTML and thus we do not support it.")
            return None, url_obj, -1
        except (AssertionError, SSLCertVerificationError) as e:
            print(f"{url_obj.url} Something we expect to happen sometimes went wrong, skipping this one: {e}")
            return None, url_obj, -1
        except Exception as e:
            print(f"{url_obj.url} Something unknown went wrong, skipping this one, please check exception: {e}")
            return None, url_obj, -1
        except:
            print(f"Don't know what went wrong")


async def main(results: dict, labels: list, urls_lookup: dict):
    urls_list = []
    for label_position, label in enumerate(labels):
        if label not in results.keys():
            urls_for_object = urls_lookup[label]
            for i, url in enumerate(urls_for_object):
                url_obj = ObjectURL(url, i, label, label_position)
                urls_list.append(url_obj)

    sem = asyncio.Semaphore(1000)
    tasks = [request(url_obj, sem) for url_obj in urls_list]

    results_list = [await f for f in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks))]
    # results_list = await asyncio.gather(*tasks)

    for html, url_obj, status in results_list:
        if url_obj.label not in results.keys():
            results[url_obj.label] = []
        if status == 200:
            results[url_obj.label].append(html)
        # TODO could also create the list like [None] * NUM_RESULTS and enter at correct index here to preserve order


def gather_htmls(results: dict, keys: list, urls_lookup: dict, asyncio_loop):
    try:
        asyncio_loop.run_until_complete(main(results, keys, urls_lookup))
        asyncio_loop.run_until_complete(asyncio_loop.shutdown_asyncgens())
    finally:
        asyncio_loop.close()
