import os
import pickle
import pprint

import tqdm

import parse_objects
from lengths_regex import LengthsFinderRegex
from wikipedia import is_disambiguation, WikiLookupWrapper

pp = pprint.PrettyPrinter()


# TODO: think about whether I should filter double wikipedia entries. Maybe ignore wikipedia altogether


def regex_wiki(label: str, lookups_wrapper: WikiLookupWrapper):
    """Retrieve sizes from a wiki page."""
    lookup = lookups_wrapper.lookup(label)
    matches = None  # TODO maybe make empty list
    if lookup.exists() and not is_disambiguation(lookup):
        matcher = LengthsFinderRegex(lookup.text)
        matches = matcher.find_all_matches()

    return matches


def regex_google_results(label: str, htmls_lookup: dict):
    """Retrieve sizes from a list of html pages."""
    htmls = htmls_lookup[label]
    sizes = []
    for html in htmls:
        matcher = LengthsFinderRegex(html)
        sizes += matcher.find_all_matches()
    return sizes


def main():
    print('Google search results are not yet included')
    names = parse_objects.retrieve_names()
    labels = parse_objects.retrieve_labels()
    wiki_lookups = parse_objects.retrieve_wikipedia_lookups()
    lookups_wrapper = WikiLookupWrapper(wiki_lookups)

    htmls_lookup = parse_objects.retrieve_google_results_html()

    results = {}

    for i in tqdm.trange(len(names)):
        label = labels[i]
        sizes = []
        sizes += regex_wiki(label, lookups_wrapper)
        sizes += regex_google_results(label, htmls_lookup)
        sizes.sort()
        results[label] = sizes

    pickle.dump(results, open(os.path.join('data', 'regex_sizes.p'), 'wb'))
    pp.pprint(results)


if __name__ == "__main__":
    main()
