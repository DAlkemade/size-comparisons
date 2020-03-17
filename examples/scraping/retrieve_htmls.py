# Save the results the google search api return for 'OBJECT length'
import asyncio
import os
import pickle
from argparse import ArgumentParser
from pathlib import Path
import time

from size_comparisons.scraping import html_scraper
from size_comparisons.parse_objects import InputsParser


def main():
    parser = ArgumentParser()
    parser.add_argument('--datadir', default=None, type=str)
    args = parser.parse_args()
    data_path = None
    if args.datadir is not None:
        data_path = Path(args.datadir)
    inputparser = InputsParser(data_dir=data_path)
    labels = inputparser.retrieve_labels()[:10]
    fname = 'google_results_html.p'
    file_path = inputparser.data_dir / fname
    urls = inputparser.retrieve_google_urls()
    loop = asyncio.get_event_loop()
    htmls_lookup = html_scraper.create_or_update_urls_html(labels, urls, loop)
    while True:
        try:
            with open(file_path, 'wb') as f:
                pickle.dump(htmls_lookup, f, pickle.HIGHEST_PROTOCOL)
        except PermissionError:
            time.sleep(300.)
            continue
        break




if __name__ == "__main__":
    main()
