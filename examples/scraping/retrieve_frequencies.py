import fileinput
from argparse import ArgumentParser

from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.frequencies import retrieve_frequencies
import logging
from datetime import datetime
from logging_setup_dla.logging import set_up_root_logger
import os
import numpy as np

set_up_root_logger(f'FREQS_{datetime.now().strftime("%d%m%Y%H%M%S")}', os.getcwd())

logger = logging.getLogger(__name__)


def main():
    """Retrieve frequencies from the web5gram corpus."""
    parser = ArgumentParser()
    parser.add_argument('--objects', required=True, type=str)
    args = parser.parse_args()
    objects_fname = args.objects

    inputparser = InputsParser()
    names = [line.strip() for line in fileinput.input(objects_fname)]
    fname = inputparser.data_dir / 'frequencies.json'
    counts_dict = retrieve_frequencies(names, fname, inputparser.data_dir / 'frequencies')

    counts = list()
    for name in names:
        try:
            count = int(counts_dict[name])
        except KeyError:
            continue
        counts.append(count)

    logger.info(f'Counts: {counts}')
    logger.info(f'Median: {np.median(counts)}')
    logger.info(f'Mean: {np.mean(counts)}')


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception("Unhandled exception")
        raise

