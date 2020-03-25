import pprint
from collections import namedtuple

import pandas as pd
from scipy.stats import norm

from size_comparisons.inference.baseline_numeric_gaussians import BaselineNumericGaussians

pp = pprint.PrettyPrinter()


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


def test_relation_update():
    min_p = 0.0000000000000001
    Entry = namedtuple('Entry', ['name', 'sizes'])
    data_list = list()
    data_list.append(Entry('tiger', norm.rvs(1.2, .1, size=30)))
    data_list.append(Entry('dog', norm.rvs(1., .1, size=30)))
    data_list.append(Entry('cat', norm.rvs(.9, 1., size=20)))
    data = pd.DataFrame(data_list)
    baseline = BaselineNumericGaussians(data)
    baseline.fill_adjacency_matrix()
    baseline.update_distance_matrix()
    tiger_cat_before = baseline.shortest_path('tiger', 'cat')
    print_info(baseline)
    print('\n')

    baseline.update_ttest_value('dog', 'cat', min_p)
    baseline.update_distance_matrix()
    print_info(baseline)
    tiger_cat_after = baseline.shortest_path('tiger', 'cat')
    assert tiger_cat_after < tiger_cat_before


def print_info(baseline):
    print('tiger to cat', baseline.matrix[0, 2])
    print('tiger to dog', baseline.matrix[0, 1])
    print('dog to cat', baseline.matrix[1, 2])
    print('shortest dog to cat', baseline.shortest_path('dog', 'cat'))
    print('shortest tiger to cat', baseline.shortest_path('tiger', 'cat'))
    pp.pprint(baseline.distance_matrix)
