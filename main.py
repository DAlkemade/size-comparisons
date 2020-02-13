import pandas as pd
import wikipediaapi
import tqdm
import nltk
from nltk.corpus import wordnet as wn
import parse_objects
import json

nltk.download('wordnet')
TEST = True

wiki_wiki = wikipediaapi.Wikipedia('en')

apple = wn.synset('apple.n.01')
print(apple.definition())
print(apple.hypernyms())
print(apple.lexname())
apple_lookup = wiki_wiki.page('apple')
print(apple_lookup.langlinks)

# get all images and info(but no description). see here for available properties: https://en.wikipedia.org/w/api.php?action=help&modules=query%2Bimageinfo
# https://en.wikipedia.org/w/api.php?action=query&generator=images&titles=apple&prop=imageinfo&iiprop=url&format=json&formatversion=2

# Alternative in two steps:
# 1. get images list: https://en.wikipedia.org/w/api.php?action=query&titles=Albert%20Einstein&format=json&prop=images
# 2. Get image info for one image:
# https://en.wikipedia.org/w/api.php?action=query&titles=File:Malus_domestica_-_Köhler–s_Medizinal-Pflanzen-108.jpg&prop=imageinfo&iilimit=50&iiprop=timestamp|user|url


# IMPORT DATA
names = parse_objects.retrieve_names()
labels = parse_objects.retrieve_labels()
with open('data/frequencies.json', 'r') as in_file:
    ngram_count_lookup = json.load(in_file)

# Reduce data if text
if TEST:
    test_n = 20
    names = names[:test_n]
    labels = labels[:test_n]

# CHECK IF WIKIPEDIA PAGE EXISTS AND RETRIEVE TEXT
wikipedia_exists_list = []
disambiguation_pages_list = []
synsets_not_empty = []
counts = []
for i in tqdm.trange(len(names)):
    name = names[i]
    synsets = wn.synsets(name.replace(' ', '_'))
    synsets_not_empty.append(len(synsets) > 0)
    lookup = wiki_wiki.page(name)
    exists = lookup.exists()
    wikipedia_exists_list.append(exists)
    disambiguation_pages_list.append('Category:All article disambiguation pages' in lookup.categories.keys())
    count = None
    if name in ngram_count_lookup.keys():
        count = ngram_count_lookup[name]
    counts.append(count)

data = pd.DataFrame(
    list(zip(names, labels, wikipedia_exists_list, disambiguation_pages_list, synsets_not_empty, counts)),
    columns=['name', 'label', 'wikipedia_entry', 'disambiguation', 'wordnet_entry', 'count'])
print(f'Fraction of objects with wiki page: {data["wikipedia_entry"].mean()}')
print(f'Fraction of disambiguation pages (of total): {data["disambiguation"].mean()}')
print(f'Fraction of objects with wordnet page: {data["wordnet_entry"].mean()}')
