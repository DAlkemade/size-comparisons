import logging

from size_comparisons.parse_objects import InputsParser
logname = 'log.log'
logging.basicConfig(filename=logname,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

logging.info("Running Urban Planning")

logger = logging.getLogger('urbanGUI')
import pprint

from size_comparisons.scraping.analyze import retrieve_synset

pp = pprint.PrettyPrinter()
PRINT_HTML = False


analyzed_terms = ['n03326948', 'n04311174', 'n04060904', 'n03216402', 'n01579410', 'n04326084']

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
            logger.info(htmls[term])
        logger.info(regex_sizes[term])
        logger.info(regex_contexts[term])


if __name__ == "__main__":
    main()