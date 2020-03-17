from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.frequencies import retrieve_frequencies


def main():
    """Retrieve frequencies from the web5gram corpus."""
    inputparser = InputsParser()
    names = inputparser.retrieve_names()
    fname = inputparser.data_dir / 'frequencies.json'
    retrieve_frequencies(names, fname)


if __name__ == '__main__':
    main()
