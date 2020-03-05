# Save the results the google search api return for 'OBJECT length'
import os
import pickle

import parse_objects
from google import create_or_update_urls_html


def main():
    labels = parse_objects.retrieve_labels()
    fname = 'google_results_html.p'
    file_path = os.path.join('data', fname)
    urls = pickle.load(open(os.path.join('data', 'google_urls.p')))
    create_or_update_urls_html(file_path, labels, urls)


if __name__ == "__main__":
    main()