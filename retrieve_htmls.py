# Save the results the google search api return for 'OBJECT length'
import asyncio
import os
import pickle
import ssl

import parse_objects
import google_ops


def main():
    print(ssl.OPENSSL_VERSION)
    labels = parse_objects.retrieve_labels()
    fname = 'google_results_html.p'
    file_path = os.path.join('data', fname)
    urls = pickle.load(open(os.path.join('data', 'google_urls.p'), 'rb'))
    loop = asyncio.get_event_loop()
    google_ops.create_or_update_urls_html(file_path, labels, urls, loop)


if __name__ == "__main__":
    main()
