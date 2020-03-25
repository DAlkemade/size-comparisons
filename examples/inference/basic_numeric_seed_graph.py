from size_comparisons.inference.baseline_numeric_gaussians import find_confidences_for_pairs
from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.analyze import fill_dataframe


def main():
    input_parser = InputsParser()
    labels = input_parser.retrieve_labels()
    data = fill_dataframe(labels)
    test_pairs = input_parser.retrieve_test_pairs()
    test_pairs_tuples = list(test_pairs.itertuples(name='TestPair', index=False))
    find_confidences_for_pairs(data, test_pairs_tuples)


if __name__ == "__main__":
    main()
