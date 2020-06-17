import logging

import numpy as np
import pandas as pd
import tqdm
from scipy import stats
from scipy.sparse.csgraph import shortest_path
from scipy.sparse.csgraph._tools import csgraph_from_dense
from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.compilation import fill_dataframe

logger = logging.getLogger(__name__)


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
        self.data.reset_index(inplace=True)
        self.matrix = matrix
        self.distance_matrix = None

    def update_ttest_value(self, name1: str, name2: str, value: float):
        """Update the edges between two objects.

        As the two directed edges sum to 1, update the pvalues both ways.
        """
        index1 = self.retrieve_index_for_name(name1)
        index2 = self.retrieve_index_for_name(name2)
        self.matrix[index1, index2] = value
        self.matrix[index2, index1] = 1 - value

    @property
    def data_size(self):
        return self.data.shape[0]

    def update_distance_matrix(self):
        """Find all shortests paths using Dijkstra.

        The shortest path between two objects represents the pvalue of the null hypothesis that object1 > object2
        """
        if self.matrix is None:
            raise ValueError('Graph is empty')
        graph = csgraph_from_dense(self.matrix, null_value=np.inf)
        # TODO zero weights break the dijkstra system, so think about that
        self.distance_matrix = shortest_path(csgraph=graph, method='D', directed=True, return_predecessors=False)

    def fill_adjacency_matrix(self):
        """Compute ttest values between all objects."""
        logger.info("Fill matrix")
        self.matrix = np.full((self.data_size, self.data_size), np.nan)
        index = self.data.index
        element_indices = list()
        for i in index:
            for j in index[i:]:
                element_indices.append((i, j))
        for i, j in tqdm.tqdm(element_indices):
            sizes1 = self.data.iloc[i]['sizes']
            sizes2 = self.data.iloc[j]['sizes']
            if min(len(sizes1), len(sizes2)) <= 1:
                # We don't trust results with only 1 data points, as it will give a deceiving std of 0
                tvalue = 0
                p = .5
            else:
                tvalue, p = stats.ttest_ind(sizes1, sizes2, equal_var=False)
            # Based on https://stackoverflow.com/a/46229127
            # TODO might be an error in assumptions by dividing p by 2 to get one-sided, since we have unequal variances
            one_sided_p = p / 2
            if tvalue > 0:
                p1 = one_sided_p
                p2 = 1 - one_sided_p
            else:
                p1 = 1 - one_sided_p
                p2 = one_sided_p
            self.matrix[i, j] = p1
            self.matrix[j, i] = p2

    def _shortest_path(self, index1: int, index2: int):
        """Find shortest path between two objects, using their indices in the matrix."""
        if self.distance_matrix is None:
            raise ValueError('Distance matrix is empty, please run update_distance_matrix')
        return self.distance_matrix[index1, index2]

    def retrieve_index_for_name(self, name: str):
        """Find index in pandas dataframe for a value of the name field."""
        return self.data.index[self.data['name'] == name][0]

    def shortest_path(self, object1: str, object2: str):
        """Find shortest path between two objects by name."""
        # We know only one value will be returned
        index1 = self.retrieve_index_for_name(object1)
        index2 = self.retrieve_index_for_name(object2)
        return self._shortest_path(index1, index2)


def load_and_update_baseline(data_dir=None) -> BaselineNumericGaussians:
    """Load numeric graph and update distance matrix."""
    input_parser = InputsParser(data_dir=data_dir)
    labels = input_parser.retrieve_labels()
    names = input_parser.retrieve_names()
    data = fill_dataframe(names, labels, datadir=data_dir)
    matrix = input_parser.load_adjacency_matrix()
    baseline = BaselineNumericGaussians(data, matrix=matrix)
    baseline.update_distance_matrix()
    return baseline
