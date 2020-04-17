import random
import time

import pandas as pd
import tqdm
from bs4 import BeautifulSoup
from requests import get
from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.analyze import retrieve_synset
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt


class Record:
    def __init__(self, name, label):
        self.label = label
        self.name = name
        self.length = None
        self.height = None
        self.size = None
        self.top_level_synset = None
        self.count = None


def check_contains_height_length(url):
    time.sleep(2)
    raw = get(url).text
    soup = BeautifulSoup(raw, 'html.parser')
    spans = soup.find_all('span')
    span_contents = [span.get_text() for span in spans]
    return int('Length' in span_contents or 'Height' in span_contents)


def generate_query(query_raw: str):
    return f'https://google.com/search?q={query_raw.replace(" ", "+")}'


# data = pd.read_csv('D:\GitHubD\size-comparisons\data\manually_selected.csv')
# objects = data['object']
inputparser = InputsParser()
names = inputparser.retrieve_names()
labels = inputparser.retrieve_labels()
records = [Record(name, labels[i]) for i, name in enumerate(names)]
random.seed(42)
records = random.sample(records, 30)
del names
del labels


def search_infoboxes(record: Record) -> None:
    record.size = check_contains_height_length(generate_query(f'{record.name} size'))
    record.height = check_contains_height_length(generate_query(f'{record.name} height'))
    record.length = check_contains_height_length(generate_query(f'{record.name} length'))


for record in tqdm.tqdm(records):
    search_infoboxes(record)

for record in records:
    synset = retrieve_synset(record.label)
    record.category = synset.lexname()

ngram_count_lookup = inputparser.retrieve_frequencies()
for record in records:
    count = int(ngram_count_lookup[record.name])
    record.count = count


data_dict = dict()
data_dict['names'] = [record.name for record in records]
data_dict['height'] = [record.height for record in records]
data_dict['size'] = [record.size for record in records]
data_dict['length'] = [record.length for record in records]
data_dict['category'] = [record.category for record in records]
data_dict['count'] = [record.count for record in records]

df = pd.DataFrame(data=data_dict)
df['any'] = (df['height']) | (df['size']) | (df['length'])
groups = df.groupby(['category']).agg(['mean', 'size'])
print(groups)
groups.to_csv(inputparser.data_dir / 'infoboxes.csv')

print(df.groupby(['category']).size())

print(f'total means: {df.mean()}')

x = df['count'].values
anys = df['any'].values
print(x)
print(anys)


bin_means, bin_edges, binnumber = stats.binned_statistic(x, anys, 'sum', bins=10)
plt.figure()
plt.plot(x, anys, 'b.', label='raw data')
plt.hlines(bin_means, bin_edges[:-1], bin_edges[1:], colors='g', lw=5,
           label='binned statistic of data')
plt.legend()
plt.show()
