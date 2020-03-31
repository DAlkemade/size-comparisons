
from size_comparisons.parse_objects import InputsParser

import pprint

from size_comparisons.scraping.analyze import retrieve_synset

pp = pprint.PrettyPrinter()
PRINT_HTML = True


analyzed_terms = ['n11860555']

def main():
    input_parser = InputsParser()
    if PRINT_HTML:
        htmls = input_parser.retrieve_google_results_html()
    synset_names = [retrieve_synset(label)._name for label in analyzed_terms]
    regex_sizes = input_parser.retrieve_regex_scraper_sizes()
    # regex_contexts = input_parser.retrieve_regex_scraper_contexts()
    for i, term in enumerate(analyzed_terms):
        pp.pprint(term)
        pp.pprint(synset_names[i])
        if PRINT_HTML:
            with open('htmls.txt', 'w') as f:
                f.writelines(htmls[term])
        pp.pprint(regex_sizes[term])
        # pp.pprint(regex_contexts[term])


if __name__ == "__main__":
    main()