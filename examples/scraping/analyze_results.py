import nltk

from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.analyze import analyze_results

nltk.download('wordnet')


# TODO: think about 3-grams (body of water)


def main():
    """Compile dataframe with scraper data and plot some results."""
    inputparser = InputsParser()
    labels = inputparser.retrieve_labels()
    analyze_results(labels)


if __name__ == "__main__":
    main()
