import pandas as pd
import wikipediaapi
import tqdm

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
with open('data/9k.labels', 'rb') as input_file:
    for line in input_file:
        labels.append(parse_entry(line))
# Reduce data if text
if TEST:
    test_n = 20
    names = names[:test_n]
    labels = labels[:test_n]

substance_article = wiki_wiki.page('substance')
print('Category:All article disambiguation pages' in substance_article.categories.keys())

# CHECK IF WIKIPEDIA PAGE EXISTS AND RETRIEVE TEXT
wikipedia_exists_list = []
disambiguation_pages_list = []
for i in tqdm.trange(len(names)):
    name = names[i]
    lookup = wiki_wiki.page(name)
    exists = lookup.exists()
    wikipedia_exists_list.append(exists)
    disambiguation_pages_list.append('Category:All article disambiguation pages' in lookup.categories.keys())

data = pd.DataFrame(list(zip(names, labels, wikipedia_exists_list, disambiguation_pages_list)),
                    columns=['name', 'label', 'wikipedia_entry', 'disambiguation'])
print(f'Fraction of objects with wiki page: {data["wikipedia_entry"].mean()}')
print(f'Fraction of disambiguation pages (of total): {data["disambiguation"].mean()}')
