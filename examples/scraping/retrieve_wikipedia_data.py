import pickle

from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.wikipedia import retrieve_wikipedia_pages


def main():
    """"""
    inputparser = InputsParser()
    names = inputparser.retrieve_names()
    labels = inputparser.retrieve_labels()
    wiki_lookups = retrieve_wikipedia_pages(names, labels)
    pickle.dump(wiki_lookups, open(inputparser.data_dir / 'wikipedia_lookups.p', 'wb'))


if __name__ == "__main__":
    main()
