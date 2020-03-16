from argparse import ArgumentParser

import nltk

from size_comparisons.scraping import parse_objects
from size_comparisons.scraping.analyze import analyze_results
from size_comparisons.scraping.parse_objects import InputsParser

nltk.download('wordnet')


# TODO: think about 3-grams (body of water)


def main():
    # parser = ArgumentParser()
    # parser.add_argument('--datadir', type=str, default=)
    inputparser = InputsParser()
    labels = inputparser.retrieve_labels()
    analyze_results(labels)


if __name__ == "__main__":
    main()
