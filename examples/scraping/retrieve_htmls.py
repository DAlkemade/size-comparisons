# Save the results the google search api return for 'OBJECT length'
import asyncio
import os
import pickle
from argparse import ArgumentParser

from size_comparisons.scraping import html_scraper
from size_comparisons.parse_objects import InputsParser


def main():
    parser = ArgumentParser()
    parser.add_argument('--datadir', default=None, type=str)
    args = parser.parse_args()
    inputparser = InputsParser(data_dir=args.datadir)
    labels = inputparser.retrieve_labels()
    fname = 'google_results_html.p'
    file_path = os.path.join('data', fname)
    urls = inputparser.retrieve_google_urls()
    loop = asyncio.get_event_loop()
    htmls_lookup = html_scraper.create_or_update_urls_html(labels, urls, loop)
    with open(file_path, 'wb') as f:
        pickle.dump(htmls_lookup, f, pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    main()
