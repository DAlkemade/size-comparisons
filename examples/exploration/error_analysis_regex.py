from size_comparisons.parse_objects import InputsParser

from size_comparisons.scraping.analyze import retrieve_synset

import logging
from datetime import datetime
from logging_setup_dla.logging import set_up_root_logger
import os

set_up_root_logger(f'ERRORANALYSIS_{datetime.now().strftime("%d%m%Y%H%M%S")}', os.getcwd())

logger = logging.getLogger(__name__)

PRINT_HTML = False


analyzed_terms = ['n01581984']

def main():
    input_parser = InputsParser()
    if PRINT_HTML:
        htmls = input_parser.retrieve_google_results_html()
    synset_names = [retrieve_synset(label)._name for label in analyzed_terms]
    regex_sizes = input_parser.retrieve_regex_scraper_sizes()
    regex_contexts = input_parser.retrieve_regex_scraper_contexts()
    for i, term in enumerate(analyzed_terms):
        logger.info(term)
        logger.info(synset_names[i])
        if PRINT_HTML:
            with open('htmls.txt', 'w') as f:
                f.writelines(htmls[term])
        else:
            logger.info(regex_contexts[term])
        logger.info(regex_sizes[term])


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("Unhandled exception")
        raise
