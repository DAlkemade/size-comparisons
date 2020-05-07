import pickle

from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.wikipedia import retrieve_wikipedia_pages
import logging
from datetime import datetime
from logging_setup_dla.logging import set_up_root_logger
import os

set_up_root_logger(f'WIKI_{datetime.now().strftime("%d%m%Y%H%M%S")}', os.getcwd())

logger = logging.getLogger(__name__)


def main():
    """"""
    inputparser = InputsParser()
    names = inputparser.retrieve_names()
    labels = inputparser.retrieve_labels()
    wiki_lookups = retrieve_wikipedia_pages(names, labels)
    pickle.dump(wiki_lookups, open(inputparser.data_dir / 'wikipedia_lookups.p', 'wb'))


if __name__ == "__main__":
    main()
