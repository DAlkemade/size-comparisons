import nltk

from thesis_scraper import parse_objects
from thesis_scraper.analyze import analyze_results

nltk.download('wordnet')


# TODO: think about 3-grams (body of water)


def main():
    labels = parse_objects.retrieve_labels()
    analyze_results(labels)


if __name__ == "__main__":
    main()
