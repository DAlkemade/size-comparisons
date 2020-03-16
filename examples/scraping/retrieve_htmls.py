# Save the results the google search api return for 'OBJECT length'
import asyncio
import os
import pickle

from size_comparisons.scraping import html_scraper
from size_comparisons.parse_objects import InputsParser


def main():
    inputparser = InputsParser()
    labels = inputparser.retrieve_labels()
    fname = 'google_results_html.p'
    file_path = os.path.join('data', fname)
    urls = pickle.load(open(os.path.join('data', 'google_urls.p'), 'rb'))
    loop = asyncio.get_event_loop()
    htmls_lookup = html_scraper.create_or_update_urls_html(labels, urls, loop)
    with open(file_path, 'wb') as f:
        pickle.dump(htmls_lookup, f, pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    main()
