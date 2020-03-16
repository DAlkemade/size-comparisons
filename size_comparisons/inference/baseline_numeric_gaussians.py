import math

from size_comparisons.scraping.analyze import fill_dataframe
from size_comparisons.parse_objects import InputsParser
import pandas as pd
import numpy as np
from scipy import stats
# scipy.stats.f_oneway
# scipy.stats.ttest_ind

class BaselineNumericGaussians(object):

    def __init__(self, data: pd.DataFrame):
        self.data = data

    def retrieve_mu_std(self, name: str) -> (float, float):
        row = self.retrieve_row(name)
        return row['mean'].values[0], row['std'].values[0]

    def retrieve_row(self, name):
        row = self.data.loc[self.data['name'] == name]
        if row.empty:
            raise RuntimeWarning(f"Unknown object {name}")
        return row

    def retrieve_sizes(self, name):
        row = self.retrieve_row(name)
        return row['sizes'].values[0]

    def larger_than_simple(self, object1: str, object2: str) -> float:
        mu1, std1 = self.retrieve_mu_std(object1)
        mu2, std2 = self.retrieve_mu_std(object2)
        if math.isnan(mu1) or math.isnan(mu2):
            raise RuntimeWarning("Nan value, unreliable results")

        mu_combine = mu1 - mu2
        std = np.sqrt(std1**2 + std2**2)
        cdf0 = stats.norm(mu_combine, std).cdf(0.)
        return 1 - cdf0

    def ttest(self, object1: str, object2: str):
        # TODO how to use the fact that we know sizes can't be negative
        sizes1 = self.retrieve_sizes(object1)
        sizes2 = self.retrieve_sizes(object2)
        tvalue, p = stats.ttest_ind(sizes1, sizes2, equal_var=False)
        # p value: assuming the null hypothesis (the population means are the same) is true, what is the probability
        # of seeing the data that we are seeing or more extreme
        mean_larger = self.larger_than_simple(object1, object2) > .5

        return p, mean_larger


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
            ttest, mean_larger = baseline.ttest(name1, name2)
        except RuntimeWarning:
            print(f"Unreliable result for {name1}, {name2}, not showing")
            continue
        print(f'Mean of {name1} is {"" if mean_larger else "not "}bigger than {name2}, null hypothesis p_value is '
              f'{ttest} and the difference is thus '
              f'{"" if ttest <= 0.05 else "not"} significant')


if __name__ == "__main__":
    main()