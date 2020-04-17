import random
import time

import pandas as pd
import tqdm
from bs4 import BeautifulSoup
from requests import get
from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.analyze import retrieve_synset


class Record:
    def __init__(self, name, label):
        self.label = label
        self.name = name
        self.length = None
        self.height = None
        self.size = None
        self.top_level_synset = None


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
records = random.sample(records, 5)
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

data_dict = dict()
data_dict['names'] = [record.name for record in records]
data_dict['height'] = [record.height for record in records]
data_dict['size'] = [record.size for record in records]
data_dict['length'] = [record.length for record in records]
data_dict['category'] = [record.category for record in records]

df = pd.DataFrame(data=data_dict)
groups = df.groupby(['category']).mean()
print(groups)
groups.to_csv(inputparser.data_dir / 'infoboxes.csv')

print(f'total means: {df.mean()}')
