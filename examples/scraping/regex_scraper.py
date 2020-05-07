# TODO: think about whether I should filter double wikipedia entries. Maybe ignore wikipedia altogether
from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.lengths_regex import parse_documents_for_lengths
import logging
from datetime import datetime
from logging_setup_dla.logging import set_up_root_logger
import os

set_up_root_logger(f'REGEX_{datetime.now().strftime("%d%m%Y%H%M%S")}', os.getcwd())

logger = logging.getLogger(__name__)


def main():
    """Parse the sizes using regex from wiki pages and google search results."""
    inputparser = InputsParser()
    labels = inputparser.retrieve_labels()
    lookups_wrapper = inputparser.retrieve_wikipedia_lookups()

    htmls_lookup = inputparser.retrieve_google_results_html()
    fname = inputparser.data_dir / 'regex_sizes.p'
    fname_contexts = inputparser.data_dir / 'regex_contexts.p'
    parse_documents_for_lengths(labels, lookups_wrapper, htmls_lookup, fname, fname_contexts)


if __name__ == "__main__":
    main()
