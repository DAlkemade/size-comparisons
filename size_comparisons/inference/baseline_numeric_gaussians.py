import numpy as np
import pandas as pd
import tqdm
from scipy import stats
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra


class BaselineNumericGaussiansLazy(object):

    def __init__(self, data: pd.DataFrame):
        self.data = data

    def retrieve_row(self, name):
        row = self.data.loc[self.data['name'] == name]
        if row.empty:
            raise RuntimeWarning(f"Unknown object {name}")
        return row

    def retrieve_sizes(self, name):
        row = self.retrieve_row(name)
        return row['sizes'].values[0]

    def ttest_lazy(self, object1: str, object2: str) -> float:
        # TODO how to use the fact that we know sizes can't be negative
        # TODO think about using the ztest (maybe increase number of pages scraped), because having gaussian might be
        # more useful
        index1 = self.data.index[self.data['name'] == object1][0]
        index2 = self.data.index[self.data['name'] == object2][0]
        sizes1 = self.retrieve_sizes(object1)
        sizes2 = self.retrieve_sizes(object2)
        tvalue, p = stats.ttest_ind(sizes1, sizes2, equal_var=False)  # welch ttest (unequal variances)
        # https://blog.minitab.com/blog/adventures-in-statistics-2/understanding-t-tests-1-sample-2-sample-and-paired-t-tests
        # p value: assuming the null hypothesis (the population means are the same) is true, what is the probability
        # of seeing the data that we are seeing or more extreme

        return tvalue


class BaselineNumericGaussians(object):

    def __init__(self, data: pd.DataFrame, matrix=None):
        """Set up parameters.

        :param data: dataframe with index in the form of range(0, len(data.index))
        """
        try:
            data_filtered = data[['name', 'sizes']]
        except KeyError:
            raise ValueError("Missing column in dataframe")
        self.data = data_filtered
        self.matrix = matrix
        self.distance_matrix = None

    @property
    def data_size(self):
        return self.data.shape[0]

    def update_distance_matrix(self):
        if self.matrix is None:
            raise ValueError('Graph is empty')
        graph = csr_matrix(self.matrix)
        self.distance_matrix = dijkstra(csgraph=graph, directed=True, return_predecessors=False)

    def fill_adjacency_matrix(self):
        self.matrix = np.full((self.data_size, self.data_size), np.nan)
        index = self.data.index

        for i in tqdm.tqdm(index):
            for j in index[i:]:
                if i != j:
                    # TODO handle singlevalue and empty lists
                    sizes1 = self.data.iloc[i]['sizes']
                    sizes2 = self.data.iloc[j]['sizes']
                    tvalue, p = stats.ttest_ind(sizes1, sizes2, equal_var=False)
                    # Based on https://stackoverflow.com/a/46229127
                    # TODO might be an error in assumptions by dividing p by 2 to get one-sided, since we have unequal variances
                    one_sided_p = p / 2
                    if tvalue > 0:
                        p1 = one_sided_p
                        p2 = 1 - one_sided_p
                    else:
                        p1 = 1- one_sided_p
                        p2= one_sided_p
                    self.matrix[i, j] = p1
                    self.matrix[j, i] = p2
                    print()
                else:
                    self.matrix[i,j] = 1.

    def _shortest_path(self, index1: int, index2: int):
        if self.distance_matrix is None:
            raise ValueError('Distance matrix is empty, please run update_distance_matrix')
        return self.distance_matrix[index1, index2]

    def shortest_path(self, object1: str, object2: str):
        # We know only one value will be returned
        index1 = self.data.index[self.data['name'] == object1][0]
        index2 = self.data.index[self.data['name'] == object2][0]
        return self._shortest_path(index1, index2)


def find_confidences_for_pairs_lazy(data: pd.DataFrame, test_pairs_tuples: list):
    baseline = BaselineNumericGaussiansLazy(data)
    for pair in test_pairs_tuples:
        try:
            name1 = pair.object1
            name2 = pair.object2
        except RuntimeWarning:
            print("Couldn't find one of the objects, skipping this pair")
            continue
        try:
            t_statistic = baseline.ttest_lazy(name1, name2)
        except RuntimeWarning:
            print(f"Unreliable result for {name1}, {name2}, not showing")
            continue
        print(
            f'Mean of {name1} is {"" if t_statistic > 0 else "not "}bigger than {name2}, null hypothesis tstatistic is '
            f'{t_statistic}')
