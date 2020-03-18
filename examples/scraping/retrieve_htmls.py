# Save the results the google search api return for 'OBJECT length'
import asyncio
import pickle
import time
from argparse import ArgumentParser
from pathlib import Path

from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping import html_scraper


def main():
    """Retrieve the html pages for the urls in the google search results."""
    parser = ArgumentParser()
    parser.add_argument('--datadir', default=None, type=str)
    args = parser.parse_args()
    data_path = None
    if args.datadir is not None:
        data_path = Path(args.datadir)
    inputparser = InputsParser(data_dir=data_path)
    labels = inputparser.retrieve_labels()
    fname = 'google_results_html.p'
    file_path = inputparser.data_dir / fname
    print(f'Will save result at {file_path}')
    urls = inputparser.retrieve_google_urls()
    loop = asyncio.get_event_loop()
    htmls_lookup = html_scraper.create_or_update_urls_html(labels, urls, loop)
    while True:
        try:
            print("Try saving the results")
            with open(file_path, 'wb') as f:
                pickle.dump(htmls_lookup, f, pickle.HIGHEST_PROTOCOL)
        except PermissionError:
            wait = 300.
            print(f"Received permissionerror, wait {wait} seconds before retry")
            time.sleep(wait)
            continue
        break


if __name__ == "__main__":
    main()
