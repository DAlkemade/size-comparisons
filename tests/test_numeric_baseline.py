from collections import namedtuple

from scipy.stats import norm

from size_comparisons.inference.baseline_numeric_gaussians import BaselineNumericGaussians
import pandas as pd


def test_non_lazy_baseline_integration():
    Entry = namedtuple('Entry', ['name', 'sizes'])
    data_list = list()
    data_list.append(Entry('tiger', norm.rvs(10.0, 2.5, size=500)))
    data_list.append(Entry('insect', norm.rvs(.05, .01, size=100)))
    data = pd.DataFrame(data_list)
    baseline = BaselineNumericGaussians(data)
    baseline.fill_adjacency_matrix()
    baseline.update_distance_matrix()
    tiger_to_insect = baseline.shortest_path('tiger', 'insect')
    insect_to_tiger = baseline.shortest_path('insect', 'tiger')
    assert tiger_to_insect < insect_to_tiger
