import os
import pickle
import pprint
import re
import numpy as np

# The key is the power of 10 it is compared to meters
import tqdm
import logging

logger = logging.getLogger(__name__)

from size_comparisons.scraping.wikipedia import WikiLookupWrapper, is_disambiguation

UNITS = {
    .001: ['millimeters', 'millimeter', 'mm', 'mms', 'millimetre', 'millimetres'],
    .01: ['centimeters', 'centimeter', 'cm', 'cms', 'centimetre', 'centimetres'],
    .0254: ['inches', 'inch'], #" and in left out on purpose to maintain precision
    .3048: ['feet', 'foot', 'ft'],
    1.: ['meters', 'meter', 'm', 'metre', 'metres'], # leave out ms since that is milliseconds
    1000.: ['kilometers', 'km', 'kilometer', 'kms', 'kilometres', 'kilometres'],
    1609.3: ['miles', 'mile', 'mi']
}


# TODO: think about float vs int. e.g. we should also be able to find 1.5 meters
# TODO: if the meters is at the end of the string, with no punctuation mark, it will miss it, e.g. 'he is 6 meter'
# TODO: the regex has to start with a space, so it will miss anything at the start of the sentence
class LengthsFinderRegex:
    """
    Find all lengths in a string (e.g. article) by matching some simple regular expressions.
    The 'matches' list is in METERS!!
    """

    def __init__(self, text: str, debug=False, save_context=False):
        self.save_context = save_context
        self.number_pattern = r'[0-9][0-9,]*\.?[0-9]*'
        self.text = text
        self.matches = list()
        self.contexts = list()
        self.debug = debug

    def find_all_matches(self) -> (list, list):
        """
        Find all matches using all patterns in UNITS and return them.
        :return:
        """
        for factor, synonym_list in UNITS.items():
            self._find_pattern(synonym_list, factor)
        return self.matches, self.contexts

    @staticmethod
    def _convert_list_elements_to_float(matches):
        return [float(el) for el in matches]

    def _match_synonyms(self, synonyms: list):
        """
        Find all matches in the predefined format for different unit synonyms.
        :param synonyms: list of synonyms
        :return:
        """
        local_matches = list()
        contexts = list()
        # [ ,.;:$]
        for syn in synonyms:
            # (?:$|[^a-zA-Z])
            punct = r'[.,;:)]'
            pattern = rf'(?:^|[ \(-])({self.number_pattern})(?:[ ]|&#160;)?{syn}(?:$|{punct}+ |{punct}+$| )'
            if self.save_context:
                contexts += re.findall(r"(^.*?%s.*?$)" % pattern, self.text, re.MULTILINE)
            local_matches += re.findall(pattern, self.text, re.MULTILINE)
        return local_matches, contexts

    def _find_pattern(self, synonyms, factor):
        """
        Find all matches for a certain order in the length scale and then convert to meters.
        :param synonyms:
        :param factor:
        """
        matches, contexts = self._match_synonyms(synonyms)
        matches = [match.replace(',', '') for match in matches]
        matches_floats = self._convert_list_elements_to_float(matches)
        matches_floats = [el * factor for el in matches_floats]

        self.matches += zip(matches, matches_floats)
        self.contexts += contexts




def regex_wiki(label: str, lookups_wrapper: WikiLookupWrapper) -> (list, list):
    """Retrieve sizes from a wiki page."""
    lookup = lookups_wrapper.lookup(label)
    matches = []  # TODO maybe make empty list
    contexts = []
    if lookup.exists() and not is_disambiguation(lookup):
        matcher = LengthsFinderRegex(lookup.text)
        matches, contexts = matcher.find_all_matches()
        _, matches = zip(*matches)

    return matches, contexts


def regex_google_results(label: str, htmls_lookup: dict, max_size=None) -> (list, list):
    """Retrieve sizes from a list of html pages."""
    sizes = list()
    contexts = list()
    try:
        htmls = htmls_lookup[label]
    except KeyError:
        logger.warning(f'{label} not in htmls')
        return sizes, contexts

    for html in htmls:
        if max_size is not None and len(html) > max_size:
            html = html[:max_size]
        matcher = LengthsFinderRegex(html)
        sizes_tmp, contexts_tmp = matcher.find_all_matches()
        if len(sizes_tmp) > 0:
            _, sizes_tmp = zip(*sizes_tmp)
            sizes += sizes_tmp
            contexts += contexts_tmp
    return sizes, contexts


def parse_documents_for_lengths(labels, htmls_lookup: dict, lookups_wrapper: WikiLookupWrapper = None):
    """Find all lengths for objects in labels using the htmls and wikipedia texts.

    :param labels: wordnet labels to find the lengths for
    :param lookups_wrapper: wikipedia texts lookup
    :param htmls_lookup: dict with lists of htmls for all objects in labels
    :param save_fname: path to save the result to
    """
    lengths = []
    for key, value in htmls_lookup.items():
        for doc in value:
            lengths.append(len(doc))

    logger.info(f'Mean doc length: {np.mean(lengths)}')
    logger.info(f'Median doc length: {np.median(lengths)}')

    results = {}
    results_contexts = {}

    for i in tqdm.trange(len(labels)):
        label = labels[i]
        sizes = list()
        contexts = list()
        if lookups_wrapper is not None:
            wiki_lengths, wiki_contexts = regex_wiki(label, lookups_wrapper)
            contexts += wiki_contexts
            sizes += wiki_lengths
        sizes_google, contexts_google = regex_google_results(label, htmls_lookup)
        sizes += sizes_google
        contexts += contexts_google
        results[label] = sizes
        results_contexts[label] = contexts

    return results, results_contexts

