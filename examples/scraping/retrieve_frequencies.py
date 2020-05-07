from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.frequencies import retrieve_frequencies
import logging
from datetime import datetime
from logging_setup_dla.logging import set_up_root_logger
import os

set_up_root_logger(f'FREQS_{datetime.now().strftime("%d%m%Y%H%M%S")}', os.getcwd())

logger = logging.getLogger(__name__)


def main():
    """Retrieve frequencies from the web5gram corpus."""
    inputparser = InputsParser()
    names = inputparser.retrieve_names()
    fname = inputparser.data_dir / 'frequencies.json'
    retrieve_frequencies(names, fname)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception("Unhandled exception")
        raise

