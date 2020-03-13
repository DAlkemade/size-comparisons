# Save the results the google search api return for 'OBJECT length'
import asyncio
import os
import pickle
import ssl

from thesis_scraper import parse_objects, html_scraper
from thesis_scraper.lengths_regex import parse_documents_for_lengths


def main():
    labels = parse_objects.retrieve_labels()
    fname = 'google_results_html.p'
    file_path = os.path.join('data', fname)
    urls = pickle.load(open(os.path.join('data', 'google_urls.p'), 'rb'))
    loop = asyncio.get_event_loop()
    htmls_lookup = html_scraper.create_or_update_urls_html(labels, urls, loop)
    with open(file_path, 'wb') as f:
        pickle.dump(htmls_lookup, f, pickle.HIGHEST_PROTOCOL)
    names = parse_objects.retrieve_names()
    labels = parse_objects.retrieve_labels()
    lookups_wrapper = parse_objects.retrieve_wikipedia_lookups()

    parse_documents_for_lengths(names, labels, lookups_wrapper, htmls_lookup)


if __name__ == "__main__":
    main()
