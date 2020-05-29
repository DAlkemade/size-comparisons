import logging
import os
import pickle
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tqdm
from logging_setup_dla.logging import set_up_root_logger
from scipy import stats
from size_comparisons.exploration.explore_infoboxes import Record, search_infoboxes
from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.analyze import retrieve_synset

SAMPLE = False

set_up_root_logger('INFOBOXES', os.getcwd())
logger = logging.getLogger(__name__)

def main():
    # data = pd.read_csv('D:\GitHubD\size-comparisons\data\manually_selected.csv')
    # objects = data['object']
    inputparser = InputsParser()
    names = inputparser.retrieve_names()
    # names = [line.strip() for line in fileinput.input('D:\GitHubD\size-comparisons\examples\exploration\VisualGenome_REFORMAT.txt')]
    labels = inputparser.retrieve_labels()
    fname_records = 'records.pkl'
    if os.path.exists(fname_records):
        with open(fname_records, 'rb') as f:
            records = pickle.load(f)
    else:
        records = [Record(name, labels[i]) for i, name in enumerate(names)]
        random.seed(41)
        if SAMPLE:
            records = random.sample(records, 50)
        del names
        del labels

        for record in records:
            synset = retrieve_synset(record.label)
            record.category = synset.lexname()

        lexnames = [record.category for record in records]
        pd.Series(lexnames).value_counts().plot(kind='bar')
        plt.xticks(rotation=90)
        plt.show()

        for record in tqdm.tqdm(records):
            search_infoboxes(record)

        with open(fname_records, 'wb') as f:
            pickle.dump(records, f, pickle.HIGHEST_PROTOCOL)
    ngram_count_lookup = inputparser.retrieve_frequencies()
    for record in records:
        try:
            count = int(ngram_count_lookup[record.name])
            record.count = count
        except KeyError:
            record.count = None
            continue

    logger.info(f'Number of records: {len(records)}')
    data_dict = dict()
    data_dict['names'] = [record.name for record in records]
    data_dict['height'] = [record.height for record in records]
    data_dict['size'] = [record.size for record in records]
    data_dict['length'] = [record.length for record in records]
    data_dict['category'] = [record.category for record in records]
    data_dict['count'] = [record.count for record in records]
    df = pd.DataFrame(data=data_dict)
    df = df.dropna()
    df['any'] = (df['height']) | (df['size']) | (df['length'])
    logger.info(f'before filter: {len(df.index)}')
    df_filtered = df[df['count'] < .01 * 1000000000]
    logger.info(f'after filter: {len(df_filtered.index)}')
    plot_results(df_filtered, inputparser)
    plot_results(df, inputparser)


def plot_results(df, inputparser):
    groups = df.groupby(['category']).agg(['mean', 'size'])
    groups.to_csv(inputparser.data_dir / 'infoboxes.csv')
    logger.info(df.groupby(['category']).size())
    logger.info(f'total means: {df.mean()}')
    x = df['count'].values
    anys = df['any'].values
    bin_means, bin_edges, binnumber = stats.binned_statistic(x, anys, 'mean', bins=12)
    plt.figure()
    plt.plot(x, anys, 'b.', label='raw data')
    plt.hlines(bin_means, bin_edges[:-1], bin_edges[1:], colors='g', lw=5,
               label='binned statistic of data')
    plt.legend()
    plt.xlabel('count in Web 1T 5-gram corpus')
    plt.ylabel('fraction of objects with a Google infobox')
    plt.savefig('infoboxes.png')
    plt.show()
    logger.info(f'percentage of objects with infobox for any query: {np.mean(anys)}')


if __name__ == '__main__':
    main()
