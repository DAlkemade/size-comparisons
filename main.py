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


def print_some_info_on_synset(synset_string):
    apple = wn.synset(synset_string)
    print(apple.definition())
    print(apple.hypernyms())
    print(apple.lexname())
    apple_lookup = wiki_wiki.page('apple')
    print(apple_lookup.langlinks)


def retrieve_synset(label):
    pos = label[0]
    offset = int(label[1:])
    return wn.synset_from_pos_and_offset(pos, offset)


print_some_info_on_synset('apple.n.01')

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
counts = []
synsets_correct = []
synsets_all_for_string = []
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
    disambiguation_pages_list.append('Category:All article disambiguation pages' in lookup.categories.keys())

    # Add ngram count
    count = None
    if name in ngram_count_lookup.keys():
        count = ngram_count_lookup[name]
    counts.append(count)

data = pd.DataFrame(
    list(zip(names, labels, wikipedia_exists_list, disambiguation_pages_list, counts, synsets_correct)),
    columns=['name', 'label', 'wikipedia_entry', 'disambiguation', 'count', 'synset'])
print(f'Fraction of objects with wiki page: {data["wikipedia_entry"].mean()}')
print(f'Fraction of disambiguation pages (of total): {data["disambiguation"].mean()}')
