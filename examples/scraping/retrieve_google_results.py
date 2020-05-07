# Save the results the google search api return for 'OBJECT length'

from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.google_ops import create_or_update_results
import logging
from datetime import datetime
from logging_setup_dla.logging import set_up_root_logger
import os

set_up_root_logger(f'COMPARE_{datetime.now().strftime("%d%m%Y%H%M%S")}', os.getcwd())

logger = logging.getLogger(__name__)


def main():
    """Retrieve google search results for all object lengths."""
    inputparser = InputsParser()
    names = inputparser.retrieve_names()
    queries = [[f'{name} length'] for name in names]

    labels = inputparser.retrieve_labels()
    fname = 'google_urls.p'
    file_path = inputparser.data_dir / fname
    create_or_update_results(file_path, queries, labels)


if __name__ == "__main__":
    main()
