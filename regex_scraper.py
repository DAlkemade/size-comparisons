from thesis_scraper import parse_objects
from thesis_scraper.lengths_regex import parse_documents_for_lengths


# TODO: think about whether I should filter double wikipedia entries. Maybe ignore wikipedia altogether


def main():
    labels = parse_objects.retrieve_labels()
    lookups_wrapper = parse_objects.retrieve_wikipedia_lookups()

    htmls_lookup = parse_objects.retrieve_google_results_html()
    parse_documents_for_lengths(labels, lookups_wrapper, htmls_lookup)


if __name__ == "__main__":
    main()
