from size_comparisons.scraping.lengths_regex import parse_documents_for_lengths


# TODO: think about whether I should filter double wikipedia entries. Maybe ignore wikipedia altogether
from size_comparisons.parse_objects import InputsParser


def main():
    inputparser = InputsParser()
    labels = inputparser.retrieve_labels()
    lookups_wrapper = inputparser.retrieve_wikipedia_lookups()

    htmls_lookup = inputparser.retrieve_google_results_html()
    parse_documents_for_lengths(labels, lookups_wrapper, htmls_lookup)


if __name__ == "__main__":
    main()
