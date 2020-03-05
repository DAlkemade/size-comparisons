import os
import pickle

import tqdm
from wikipediaapi import WikipediaPage

import parse_objects
from lengths_regex import LengthsFinderRegex
from wikipedia import is_disambiguation, WikiLookupWrapper
import pprint

pp = pprint.PrettyPrinter()

def regex_wiki(label: str, lookups_wrapper: WikiLookupWrapper):
    lookup = lookups_wrapper.lookup(label)
    matches = None  # TODO maybe make empty list
    if lookup.exists() and not is_disambiguation(lookup):
        matcher = LengthsFinderRegex(lookup.text)
        matches = matcher.find_all_matches()
        matches.sort()

    return matches


def regex_google_results(results: list):
    raise NotImplementedError()


def main():
    print('Google search results are not yet included')
    names = parse_objects.retrieve_names()
    labels = parse_objects.retrieve_labels()
    wiki_lookups = parse_objects.retrieve_wikipedia_lookups()
    lookups_wrapper = WikiLookupWrapper(wiki_lookups)

    results = {}

    for i in tqdm.trange(len(names)):
        name = names[i]
        label = labels[i]
        sizes = []
        sizes += regex_wiki(label, lookups_wrapper)
        results[label] = sizes

    pickle.dump(results, open(os.path.join('data', 'regex_sizes.p'), 'wb'))
    pp.pprint(results)


if __name__ == "__main__":
    main()
