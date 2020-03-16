# Save the results the google search api return for 'OBJECT length'
import os

from size_comparisons.scraping import parse_objects
from size_comparisons.scraping.google_ops import create_or_update_results
from size_comparisons.scraping.parse_objects import InputsParser


def main():
    inputparser = InputsParser()
    names = inputparser.retrieve_names()
    queries = [f'{name} length' for name in names]

    labels = inputparser.retrieve_labels()
    fname = 'google_urls.p'
    file_path = os.path.join('data', fname)
    create_or_update_results(file_path, queries, labels)


if __name__ == "__main__":
    main()
