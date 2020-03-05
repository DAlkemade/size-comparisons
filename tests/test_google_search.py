import os
import pickle

from google import retrieve_google_results, create_or_update_results


def test_google_retrieval():
    results = {'test': ['url']}
    retrieve_google_results(results, ['tiger size'], ['tiger'])
    assert 'test' in results.keys()
    assert 'tiger' in results.keys()
    assert type(results['tiger']) is list
    assert len(results['tiger']) > 0


def test_loading_updating_saving():
    names = ['tiger size', 'helicopter size']
    labels = ['tiger', 'helicopter']
    fname = 'test_google_urls.p'
    file_path = os.path.join('../tmp', fname)
    create_or_update_results(file_path, names, labels)
    results: dict = pickle.load(open(file_path, 'rb'))
    assert type(results) is dict
    assert len(results.keys()) == 2
    assert type(results['tiger']) is list
    assert len(results['tiger']) > 0
    os.remove(file_path)
