import tqdm
import wikipediaapi
import pickle
import os

import parse_objects

DOWNLOAD_ATTRIBUTES = ['extracts', 'info', 'categories']


def force_lazy_object_to_fetch_data(lookup: wikipediaapi.WikipediaPage):
    """As the WikipediaPage object loads its attributes lazily and we want to store them for future use,
    we force the object to retrieve them.
    """
    for key in DOWNLOAD_ATTRIBUTES:
        lookup._fetch(key)


def retrieve_wikipedia_pages(search_terms: list, ids: list) -> dict:
    """Retrieve the WikipediaPage objects for all YOLO objects and store them in a list, which follows the
    order of the YOLO object files (9k.names and 9k.labels).

    :param search_terms: wikipedia search terms
    :param ids: unique id for search terms
    :return: dict with ids as keys and wikipedia pages as objects
    """
    wiki_lookups = {}
    wiki = wikipediaapi.Wikipedia('en')

    for i in tqdm.trange(len(search_terms)):
        name = search_terms[i]
        id = ids[i]
        lookup = wiki.page(name)
        force_lazy_object_to_fetch_data(lookup)
        wiki_lookups[id] = lookup

    return wiki_lookups


def main():
    names = parse_objects.retrieve_names()
    labels = parse_objects.retrieve_labels()
    wiki_lookups = retrieve_wikipedia_pages(names, labels)
    pickle.dump(wiki_lookups, open(os.path.join('data', 'wikipedia_lookups.p'), 'wb'))


if __name__ == "__main__":
    main()
