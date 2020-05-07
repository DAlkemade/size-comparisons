import pickle

from size_comparisons.inference.baseline_numeric_gaussians import BaselineNumericGaussians
from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.compilation import fill_dataframe
import logging
from datetime import datetime
from logging_setup_dla.logging import set_up_root_logger
import os

set_up_root_logger(f'NUMERIC_SEED_{datetime.now().strftime("%d%m%Y%H%M%S")}', os.getcwd())

logger = logging.getLogger(__name__)

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
    try:
        main()
    except Exception:
        logger.exception("Unhandled exception")
        raise

