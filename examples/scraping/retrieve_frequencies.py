from size_comparisons.scraping import parse_objects
from size_comparisons.scraping.frequencies import retrieve_frequencies


def main():
    names = parse_objects.retrieve_names()
    retrieve_frequencies(names)


if __name__ == '__main__':
    main()
