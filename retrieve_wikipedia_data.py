import pickle
import os

import parse_objects
from wikipedia import retrieve_wikipedia_pages


def main():
    names = parse_objects.retrieve_names()
    labels = parse_objects.retrieve_labels()
    wiki_lookups = retrieve_wikipedia_pages(names, labels)
    pickle.dump(wiki_lookups, open(os.path.join('data', 'wikipedia_lookups.p'), 'wb'))


if __name__ == "__main__":
    main()
