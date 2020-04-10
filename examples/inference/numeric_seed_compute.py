import pickle

from size_comparisons.inference.baseline_numeric_gaussians import BaselineNumericGaussians
from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.compilation import fill_dataframe

selected = ['tiger', 'insect', 'ocean', 'cat', 'dog', 'crown', 'neuropteron', 'diving suit', 'light-emitting diode',
            'stone']


def main():
    input_parser = InputsParser()
    labels = input_parser.retrieve_labels()
    names = input_parser.retrieve_names()
    data = fill_dataframe(names, labels)
    # mask = data['name'].isin(selected)
    # data = data[mask]
    baseline = BaselineNumericGaussians(data)
    baseline.fill_adjacency_matrix()
    pickle.dump(baseline, open(input_parser.data_dir / 'baseline.p', 'rb'))


if __name__ == "__main__":
    main()
