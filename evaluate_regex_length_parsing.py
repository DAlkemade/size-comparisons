import pprint

import wikipediaapi

from thesis_scraper.lengths_regex import LengthsFinderRegex
from analyze_results import plot_sizes_with_gaussian
from thesis_scraper.wikipedia import is_disambiguation

pp = pprint.PrettyPrinter()

interesting_objects = ['tiger', 'cave', 'glacier', 'amphitheater', 'sun deck', 'tambour', 'supermarket', 'baseball bat',
                       'baseball glove', 'crowbar', 'tennis racket', 'cooling tower', 'fishnet', 'telephone pole',
                       'treadmill']
wiki = wikipediaapi.Wikipedia('en')
res = {}

for obj in interesting_objects:
    lookup = wiki.page(obj)
    if lookup.exists() and not is_disambiguation(lookup):
        matcher = LengthsFinderRegex(lookup.text)
        matches = matcher.find_all_matches()
        matches.sort()
        res[obj] = matches
        if len(matches) > 0:
            plot_sizes_with_gaussian(matches)

pp.pprint(res)
