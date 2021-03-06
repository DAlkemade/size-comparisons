from scipy.stats import norm

from size_comparisons.scraping.analyze import plot_sizes_with_gaussian


def test_gaussian_plot():
    data = norm.rvs(10.0, 2.5, size=500)
    plot_sizes_with_gaussian(data, 'test')
