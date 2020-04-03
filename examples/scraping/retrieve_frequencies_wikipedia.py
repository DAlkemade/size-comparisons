import json
from argparse import ArgumentParser

from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.frequencies_wikipedia import find_frequencies_wikipedia


def main():
    """Retrieve frequencies from a wikipedia Lucene index."""
    parser = ArgumentParser()
    parser.add_argument('--index', type=str, required=True)
    args = parser.parse_args()
    index_dir = args.index
    inputparser = InputsParser()
    names = inputparser.retrieve_names()
    fname = inputparser.data_dir / 'frequencies_wikipedia.json'
    freqs = find_frequencies_wikipedia(names, index_dir)

    with open(fname, 'w') as wf:
        json.dump(freqs, wf)


if __name__ == '__main__':
    main()
