import asyncio
import logging
import os
import pickle
import ssl
import unicodedata
from collections import namedtuple
from typing import Dict

import aiohttp
import certifi
import tqdm
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

CONCURRENT_TASKS = 10
ObjectURL = namedtuple('ObjectURL', ['url', 'index', 'label', 'position_in_order'])
TIMEOUT = 20


def create_or_update_urls_html(htmls_fname: str, keys: list, urls: dict, asyncio_loop) -> Dict[str, list]:
    """Create file with html from urls."""

    if os.path.exists(htmls_fname):
        logger.info("Loading htmls from disk")
        with open(htmls_fname, "rb") as f_html:
            results = pickle.load(f_html)
        logger.info('Loaded htmls')
    else:
        logger.info('No htmls cache')
        results = dict()

    gather_htmls(results, keys, urls, asyncio_loop)

    with open(htmls_fname, 'wb') as f:
        pickle.dump(results, f, pickle.HIGHEST_PROTOCOL)

    return results


async def request(url_obj: ObjectURL, sem, ssl_context) -> (str, ObjectURL, int):
    """Request a url and return response."""
    async with sem, aiohttp.ClientSession() as session:
        try:
            async with session.get(url_obj.url, timeout=TIMEOUT, ssl=ssl_context) as resp:
                # TODO only reads html, not pdfs
                return await resp.text(), url_obj, resp.status
        except UnicodeDecodeError as e:
            # is not HTML and thus we do not support it.
            return e, url_obj, -1
        except aiohttp.ClientError as e:
            logger.warning(f'Client error: {e}')
            return e, url_obj, -1
        except asyncio.TimeoutError as e:
            logger.warning(f'Timeouterror for url: {url_obj.url}')
            return e, url_obj, -1
        except Exception as e:
            logger.exception(
                f"{url_obj.url} Something unknown went wrong, skipping this one, please check exception: {e}")
            return e, url_obj, -1


async def main(results: dict, labels: list, urls_lookup: dict):
    """Asynchronously request all urls."""
    urls_list = []
    for label_position, label in enumerate(labels):
        if label not in results.keys():
            urls_for_object = urls_lookup[label]
            for i, url in enumerate(urls_for_object):
                url_obj = ObjectURL(url, i, label, label_position)
                urls_list.append(url_obj)

    sem = asyncio.Semaphore(CONCURRENT_TASKS)
    sslcontext = ssl.create_default_context(cafile=certifi.where())
    tasks = [request(url_obj, sem, sslcontext) for url_obj in urls_list]
    logger.info(f'Retrieving {len(tasks)} htmls that are not in cache')

    results_list = [await f for f in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks))]
    # results_list = await asyncio.gather(*tasks)
    error_count = 0
    for html, url_obj, status in results_list:
        try:
            soup = BeautifulSoup(html, features="lxml")
        except TypeError:
            error_count += 1
            continue
        tags_to_remove = ['script', 'style']
        for tag in soup.find_all(tags_to_remove):
            tag.extract()
        html = soup.get_text()
        html = unicodedata.normalize("NFKD", html)
        if url_obj.label not in results.keys():
            results[url_obj.label] = []
        if status == 200:
            results[url_obj.label].append(html)
        else:
            error_count += 1

    logger.info(f'errors: {error_count}')

    # TODO could also create the list like [None] * NUM_RESULTS and enter at correct index here to preserve order


def gather_htmls(results: dict, keys: list, urls_lookup: dict, asyncio_loop):
    """Manage asyncio overhead for async url retrieval."""
    try:
        asyncio_loop.run_until_complete(main(results, keys, urls_lookup))
        asyncio_loop.run_until_complete(asyncio_loop.shutdown_asyncgens())
    finally:
        logger.info("Close loop")
        asyncio_loop.close()
