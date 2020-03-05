import json

import nltk
import numpy as np
import pandas as pd
import tqdm
import wikipediaapi
from matplotlib import pyplot as plt
from nltk.corpus import wordnet as wn

import parse_objects
from lengths_regex import LengthsFinderRegex

nltk.download('wordnet')
TEST = True


# TODO: think about 3-grams (body of water)


def check_n(token: str) -> int:
    """
    Check n (as in n-gram) of a token
    :param token: token to be checked
    :return: int n
    """
    return len(token.split(' '))


def print_some_info_on_synset(wiki, synset_string: str) -> None:
    """
    Display some possiblities of the wordnet library.
    :param synset_string: Exact synset string
    """
    apple = wn.synset(synset_string)
    print(apple.definition())
    print(apple.hypernyms())
    print(apple.lexname())
    apple_lookup = wiki.page('apple')
    print(apple_lookup.langlinks)


def retrieve_synset(label: str):
    """
    Retrieve synset using a wordnet id.
    :param label: wordnet id
    :return: wordnet synset
    """
    pos = label[0]
    offset = int(label[1:])
    return wn.synset_from_pos_and_offset(pos, offset)


def is_disambiguation(wiki_lookup: wikipediaapi.WikipediaPage) -> bool:
    """Checks whether the wikipedia page is a disambiguation page."""
    return 'Category:All article disambiguation pages' in wiki_lookup.categories.keys()


def main():
    wiki_wiki = wikipediaapi.Wikipedia('en')
    print_some_info_on_synset(wiki_wiki, 'apple.n.01')
    # IMPORT DATA
    names = parse_objects.retrieve_names()
    labels = parse_objects.retrieve_labels()
    with open('data/frequencies.json', 'r') as in_file:
        ngram_count_lookup = json.load(in_file)
    # Reduce data if text
    if TEST:
        test_n = 10
        names = names[:test_n]
        labels = labels[:test_n]
    # CHECK IF WIKIPEDIA PAGE EXISTS AND RETRIEVE TEXT
    wikipedia_exists_list = []
    disambiguation_pages_list = []
    counts = []
    synsets_correct = []
    synsets_all_for_string = []
    ns = []
    for i in tqdm.trange(len(names)):
        # Get name and label
        name = names[i]
        label = labels[i]

        # Retrieve synset
        synsets_correct.append(retrieve_synset(label))
        synsets_all_for_string.append(wn.synsets(name.replace(' ', '_')))

        # Wikipedia entry
        lookup = wiki_wiki.page(name)
        exists = lookup.exists()
        wikipedia_exists_list.append(exists)
        disambiguation = is_disambiguation(lookup)
        disambiguation_pages_list.append(disambiguation)

        # Find all lengths
        if exists and not disambiguation:
            regex_matcher = LengthsFinderRegex(lookup.text)
            all_lengths_in_article = regex_matcher.find_all_matches()
            print(all_lengths_in_article)

        # Add ngram count
        count = None
        if name in ngram_count_lookup.keys():
            count = ngram_count_lookup[name]
        counts.append(count)

        ns.append(check_n(name))
    data = pd.DataFrame(
        list(zip(names, labels, wikipedia_exists_list, disambiguation_pages_list, counts, synsets_correct, ns)),
        columns=['name', 'label', 'wikipedia_entry', 'disambiguation', 'count', 'synset', 'n'])
    data.sort_values('count', inplace=True)
    print(f'Fraction of objects with wiki page: {data["wikipedia_entry"].mean()}')
    print(f'Fraction of disambiguation pages (of total): {data["disambiguation"].mean()}')
    plt.hist(ns, bins=range(0, np.amax(ns)))
    plt.show()


if __name__ == "__main__":
    main()
