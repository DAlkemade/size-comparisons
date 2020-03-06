import asyncio
import os
import pickle

from html_scraper import create_or_update_urls_html, gather_htmls


def test_retrieve_htmls():
    """Check whether the html retrieval method works."""
    results = {'test': ['html']}
    urls = {'tiger123': ['https://en.wikipedia.org/wiki/Tiger',
                         'https://seaworld.org/animals/all-about/tiger/characteristics/']}
    labels = ['tiger123']

    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)

        gather_htmls(results, labels, urls, loop)

    finally:
        loop.close()

    print(results)
    assert 'test' in results.keys()
    for label in labels:
        assert label in results.keys()
        assert type(results[label]) is list
        assert len(results[label]) > 0
        for res in results[label]:
            assert type(res) is str


def test_loading_updating_saving():
    """Test whether the file creation, updating, saving, etc of the html retrieval works."""
    fname = 'test_htmls.p'
    file_path = os.path.join('../tmp', fname)
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass
    labels = ['tiger123', 'helicopter123']
    urls = {labels[0]: ['https://en.wikipedia.org/wiki/Tiger',
                        'https://seaworld.org/animals/all-about/tiger/characteristics/'],
            labels[1]: ['https://www.popularmechanics.com/flight/a2150/4224761/']}

    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)

        create_or_update_urls_html(file_path, labels, urls, loop)

    finally:
        loop.close()

    results: dict = pickle.load(open(file_path, 'rb'))
    assert type(results) is dict
    assert len(results.keys()) == 2
    for label in labels:
        assert type(results[label]) is list
        assert len(results[label]) == len(urls[label])
        for res in results[label]:
            assert type(res) is str
        # assert results[label]
    os.remove(file_path)
