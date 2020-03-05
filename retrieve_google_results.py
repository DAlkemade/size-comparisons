# Save the results the google search api return for 'OBJECT length'
import os

import parse_objects
from google import create_or_update_results


def main():
    names = parse_objects.retrieve_names()
    labels = parse_objects.retrieve_labels()
    fname = 'google_urls.p'
    file_path = os.path.join('data', fname)
    create_or_update_results(file_path, names, labels)


if __name__ == "__main__":
    main()
