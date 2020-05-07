import json
from argparse import ArgumentParser

from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.frequencies_wikipedia import find_frequencies_wikipedia
import logging
from datetime import datetime
from logging_setup_dla.logging import set_up_root_logger
import os

set_up_root_logger(f'FREQSWIKI_{datetime.now().strftime("%d%m%Y%H%M%S")}', os.getcwd())

logger = logging.getLogger(__name__)


def main():
    """Retrieve frequencies from a wikipedia Lucene index."""
    parser = ArgumentParser()
    parser.add_argument('--index', type=str, required=True)
    args = parser.parse_args()
    index_dir = args.index
    inputparser = InputsParser()
    names = inputparser.retrieve_names()
    fname = inputparser.data_dir / 'frequencies_wikipedia.json'
    freqs = find_frequencies_wikipedia(names, index_dir)

    with open(fname, 'w') as wf:
        json.dump(freqs, wf)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception("Unhandled exception")
        raise

