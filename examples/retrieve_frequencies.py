from thesis_scraper import parse_objects
from thesis_scraper.frequencies import retrieve_frequencies


def main():
    names = parse_objects.retrieve_names()
    retrieve_frequencies(names)


if __name__ == '__main__':
    main()
