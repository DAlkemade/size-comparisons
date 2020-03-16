from size_comparisons.scraping import parse_objects
from size_comparisons.scraping.frequencies import retrieve_frequencies
from size_comparisons.scraping.parse_objects import InputsParser


def main():
    inputparser = InputsParser()
    names = inputparser.retrieve_names()
    retrieve_frequencies(names)


if __name__ == '__main__':
    main()
