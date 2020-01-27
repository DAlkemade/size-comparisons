import pandas as pd
import wikipediaapi
import tqdm
import nltk
from nltk.corpus import wordnet as wn

nltk.download('wordnet')

apple = wn.synset('apple.n.01')
print(apple.definition())
print(apple.hypernyms())
print(wn.synsets('edible fruit'.replace(' ', '_')))

TEST = True

wiki_wiki = wikipediaapi.Wikipedia('en')


def parse_entry(line):
    return line.decode("utf-8").strip('\n')


# IMPORT DATA
names = []
labels = []
with open('data/9k.names', 'rb') as input_file:
    for line in input_file:
        names.append(parse_entry(line))

# These are imagenet labels
with open('data/9k.labels', 'rb') as input_file:
    for line in input_file:
        labels.append(parse_entry(line))
# Reduce data if text
if TEST:
    test_n = 50
    names = names[:test_n]
    labels = labels[:test_n]

# CHECK IF WIKIPEDIA PAGE EXISTS AND RETRIEVE TEXT
wikipedia_exists_list = []
disambiguation_pages_list = []
synsets_not_empty = []
for i in tqdm.trange(len(names)):
    name = names[i]
    synsets = wn.synsets(name.replace(' ', '_'))
    synsets_not_empty.append(len(synsets) > 0)
    lookup = wiki_wiki.page(name)
    exists = lookup.exists()
    wikipedia_exists_list.append(exists)
    disambiguation_pages_list.append('Category:All article disambiguation pages' in lookup.categories.keys())

data = pd.DataFrame(list(zip(names, labels, wikipedia_exists_list, disambiguation_pages_list, synsets_not_empty)),
                    columns=['name', 'label', 'wikipedia_entry', 'disambiguation', 'wordnet_entry'])
print(f'Fraction of objects with wiki page: {data["wikipedia_entry"].mean()}')
print(f'Fraction of disambiguation pages (of total): {data["disambiguation"].mean()}')
print(f'Fraction of objects with wordnet page: {data["wordnet_entry"].mean()}')
