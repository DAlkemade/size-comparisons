# TODO: think about whether I should filter double wikipedia entries. Maybe ignore wikipedia altogether
import json
import pickle

import yaml
from box import Box
from pandas import DataFrame

from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.compilation import clean_sizes, mean_and_std
from size_comparisons.scraping.lengths_regex import parse_documents_for_lengths
import logging
from datetime import datetime
from logging_setup_dla.logging import set_up_root_logger
import os
import pandas as pd
import numpy as np
from learning_sizes_evaluation.evaluate import precision_recall, range_distance

set_up_root_logger(f'REGEX_{datetime.now().strftime("%d%m%Y%H%M%S")}', os.getcwd())

logger = logging.getLogger(__name__)
USE_WIKI = False

def main():
    """Parse the sizes using regex from google search results."""
    with open("config_scraper.yml", "r") as ymlfile:
        cfg = Box(yaml.safe_load(ymlfile))
    inputparser = InputsParser()
    input: DataFrame = pd.read_csv(cfg.path.objects)
    input = input.astype({'object': str})
    objects = list(input['object'])
    logger.info(f'objects: {objects}')

    lookups_wrapper = None
    if USE_WIKI:
        lookups_wrapper = inputparser.retrieve_wikipedia_lookups()
    with open(cfg.path.htmls_cache, 'rb') as f:
        htmls_lookup: dict = pickle.load(f)

    fname = inputparser.data_dir / 'regex_sizes.p'
    fname_contexts = inputparser.data_dir / 'regex_contexts.p'
    sizes_lookup = parse_documents_for_lengths(objects, htmls_lookup, fname, fname_contexts, lookups_wrapper=lookups_wrapper)
    logger.info(sizes_lookup)

    point_predictions = dict()
    for o in objects:
        try:
            sizes = sizes_lookup[o]
        except KeyError:
            point_predictions[o] = None
            continue
        if len(sizes) == 0:
            point_predictions[o] = None
            continue
        if len(sizes) > 2:
            _, sizes = clean_sizes(True, True, sizes)
        mean, std = mean_and_std(sizes)
        point_predictions[o] = mean

    logger.info(point_predictions)
    with open(f'regex_predictions.pkl', 'wb') as f:
        pickle.dump(point_predictions, f)

    precision_recall(input, point_predictions)
    range_distance(input, point_predictions)



if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("Unhandled exception")
        raise

