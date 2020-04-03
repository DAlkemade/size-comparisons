from size_comparisons.inference.baseline_numeric_gaussians import find_confidences_for_pairs_lazy, \
    BaselineNumericGaussians
from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.compilation import fill_dataframe


def main():
    input_parser = InputsParser()
    labels = input_parser.retrieve_labels()
    names = input_parser.retrieve_names()
    data = fill_dataframe(names, labels)
    test_pairs = input_parser.retrieve_test_pairs()
    test_pairs_tuples = list(test_pairs.itertuples(name='TestPair', index=False))
    find_confidences_for_pairs_lazy(data, test_pairs_tuples)


if __name__ == "__main__":
    main()
