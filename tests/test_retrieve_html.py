import os
import pickle

from google import retrieve_htmls, create_or_update_urls_html


def test_retrieve_htmls():
    results = {'test': ['html']}
    urls = {'tiger123': ['https://en.wikipedia.org/wiki/Tiger', 'https://seaworld.org/animals/all-about/tiger/characteristics/']}
    retrieve_htmls(results, ['tiger123'], urls)
    assert 'test' in results.keys()
    assert 'tiger123' in results.keys()
    assert type(results['tiger123']) is list
    assert len(results['tiger123']) > 0


def test_loading_updating_saving():
    fname = 'test_htmls.p'
    file_path = os.path.join('../tmp', fname)
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass
    label1 = 'tiger123'
    label2 = 'helicopter123'
    labels = [label1, label2]
    urls = {label1: ['https://en.wikipedia.org/wiki/Tiger',
                         'https://seaworld.org/animals/all-about/tiger/characteristics/'],
            'helicopter123': ['https://www.popularmechanics.com/flight/a2150/4224761/']}


    create_or_update_urls_html(file_path, labels, urls)

    results: dict = pickle.load(open(file_path, 'rb'))
    assert type(results) is dict
    assert len(results.keys()) == 2
    assert type(results[label1]) is list
    for label in labels:
        assert len(results[label]) == len(urls[label])
        for res in results[label]:
            assert res.status_code == 200
            assert type(res.text) is str
        # assert results[label]
    os.remove(file_path)
