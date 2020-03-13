import json

from thesis_scraper import parse_objects
from thesis_scraper.frequencies import FrequencyRetriever


def main():
    names = parse_objects.retrieve_names()
    retriever = FrequencyRetriever(set(names))
    freqs = retriever.run()
    count = 0
    for name in names:
        if name in freqs.keys():
            count += 1
    frac_found = count / len(names)
    print(f'Found the frequency for fraction {frac_found}')
    # Save json
    with open('frequencies.json', 'w') as wf:
        json.dump(freqs, wf)


if __name__ == '__main__':
    main()
