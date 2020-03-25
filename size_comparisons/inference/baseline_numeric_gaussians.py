import math

import numpy as np
import pandas as pd
import tqdm
from scipy import stats


class BaselineNumericGaussians(object):
    # TODO add ttest results cache for prepopulation

    def __init__(self, data: pd.DataFrame):
        """Set up parameters.

        :param data: dataframe with index in the form of range(0, len(data.index))
        """
        self.data = data
        data_size = self.data.shape[0]
        self.adjancency_matrix_cache = np.full((data_size, data_size), np.nan)

    def fill_adjacency_matrix(self):
        for i in tqdm.tqdm(self.data.index):
            for j in self.data.index:
                if i != j:
                    # TODO handle singlevalue and empty lists
                    sizes1 = self.data.iloc[i]['sizes']
                    sizes2 = self.data.iloc[j]['sizes']
                    tvalue, p = stats.ttest_ind(sizes1, sizes2, equal_var=False)
                    # Based on https://stackoverflow.com/a/46229127
                    # TODO might be an error in assumptions by dividing p by 2 to get one-sided, since we have unequal variances
                    one_sided_p = p/2
                    one_sided_p_other_way = 1 - one_sided_p
                    self.adjancency_matrix_cache[i, j] = one_sided_p
                    self.adjancency_matrix_cache[j, i] = one_sided_p_other_way

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

    def ttest(self, object1: str, object2: str) -> float:
        # TODO how to use the fact that we know sizes can't be negative
        # TODO think about using the ztest (maybe increase number of pages scraped), because having gaussian might be
        # more useful
        index1 = self.data.index[self.data['name'] == object1][0]
        index2 = self.data.index[self.data['name'] == object2][0]
        cached_value = self.adjancency_matrix_cache[index1, index2]
        if math.isnan(cached_value):
            sizes1 = self.retrieve_sizes(object1)
            sizes2 = self.retrieve_sizes(object2)
            tvalue, p = stats.ttest_ind(sizes1, sizes2, equal_var=False)  # welch ttest (unequal variances)
            # https://blog.minitab.com/blog/adventures-in-statistics-2/understanding-t-tests-1-sample-2-sample-and-paired-t-tests
            # p value: assuming the null hypothesis (the population means are the same) is true, what is the probability
            # of seeing the data that we are seeing or more extreme
        else:
            tvalue = cached_value

        return tvalue


def find_confidences_for_pairs_lazy(data: pd.DataFrame, test_pairs_tuples: list):
    baseline = BaselineNumericGaussians(data)
    baseline.fill_adjacency_matrix()
    for pair in test_pairs_tuples:
        try:
            name1 = pair.object1
            name2 = pair.object2
        except RuntimeWarning:
            print("Couldn't find one of the objects, skipping this pair")
            continue
        try:
            t_statistic = baseline.ttest(name1, name2)
        except RuntimeWarning:
            print(f"Unreliable result for {name1}, {name2}, not showing")
            continue
        print(
            f'Mean of {name1} is {"" if t_statistic > 0 else "not "}bigger than {name2}, null hypothesis tstatistic is '
            f'{t_statistic}')
