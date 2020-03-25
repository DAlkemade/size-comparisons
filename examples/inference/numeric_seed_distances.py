from size_comparisons.inference.baseline_numeric_gaussians import find_confidences_for_pairs_lazy, \
    BaselineNumericGaussians
from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.analyze import fill_dataframe


def main():
    input_parser = InputsParser()
    labels = input_parser.retrieve_labels()
    data = fill_dataframe(labels)
    matrix = input_parser.load_adjacency_matrix()
    baseline = BaselineNumericGaussians(data, matrix= matrix)
    baseline.update_distance_matrix()


if __name__ == "__main__":
    main()
