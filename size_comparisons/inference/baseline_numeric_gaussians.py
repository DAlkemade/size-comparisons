import math

from size_comparisons.scraping.analyze import fill_dataframe
from size_comparisons.parse_objects import InputsParser
import pandas as pd
import numpy as np


class BaselineNumericGaussians(object):

    def __init__(self, data: pd.DataFrame):
        self.data = data

    def retrieve_mu_std(self, name: str) -> (float, float):
        row = self.data.loc[self.data['name'] == name]
        if row.empty:
            raise RuntimeWarning(f"Unknown object {name}")
        return row['mean'].values[0], row['std'].values[0]

    def larger_than(self, object1: str, object2: str) -> bool:
        mu1, std1 = self.retrieve_mu_std(object1)
        mu2, std2 = self.retrieve_mu_std(object2)
        if math.isnan(mu1) or math.isnan(mu2):
            raise RuntimeWarning("Nan value, unreliable results")
        return mu1 > mu2


def main():
    input_parser = InputsParser()
    labels = input_parser.retrieve_labels()
    data = fill_dataframe(labels)
    test_pairs = input_parser.retrieve_test_pairs()
    test_pairs_tuples = list(test_pairs.itertuples(name='TestPair', index=False))
    baseline = BaselineNumericGaussians(data)
    for pair in test_pairs_tuples:
        try:
            name1 = pair.object1
            name2 = pair.object2
        except RuntimeWarning:
            print("Couldn't find one of the objects, skipping this pair")
            continue
        try:
            onebiggerthan2 = baseline.larger_than(name1, name2)
        except RuntimeWarning:
            print(f"Unreliable result for {name1}, {name2}, not showing")
            continue
        print(f'{name1} is{"" if onebiggerthan2 else " not"} bigger than {name2}')


if __name__ == "__main__":
    main()