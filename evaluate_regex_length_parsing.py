import wikipediaapi

from lengths_regex import LengthsFinderRegex
from main import is_disambiguation
import pprint

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

pp.pprint(res)
