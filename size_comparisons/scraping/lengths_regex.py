import os
import pickle
import pprint
import re
import numpy as np

# The key is the power of 10 it is compared to meters
import tqdm

from size_comparisons.scraping.wikipedia import WikiLookupWrapper, is_disambiguation

UNITS = {
    -3: ['millimeters', 'millimeter', 'mm'],
    -2: ['centimeters', 'centimeter', 'cm'],
    0: ['meters', 'meter', 'm'],
    3: ['kilometers', 'km', 'kilometer']

}


# TODO: think about float vs int. e.g. we should also be able to find 1.5 meters
# TODO: if the meters is at the end of the string, with no punctuation mark, it will miss it, e.g. 'he is 6 meter'
# TODO: the regex has to start with a space, so it will miss anything at the start of the sentence
class LengthsFinderRegex:
    """
    Find all lengths in a string (e.g. article) by matching some simple regular expressions.
    The 'matches' list is in METERS!!
    """

    def __init__(self, text: str, debug=False):
        self.number_pattern = r'[0-9]+\.?[0-9]*'
        self.text = text
        self.matches = list()
        self.debug = debug

    def find_all_matches(self):
        """
        Find all matches using all patterns in UNITS and return them.
        :return:
        """
        for power, synonym_list in UNITS.items():
            self._find_pattern(synonym_list, power)
        return self.matches

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
        # [ ,.;:$]
        for syn in synonyms:
            local_matches += re.findall(rf'\s+({self.number_pattern})[ ]?{syn}[ ,.;:]', self.text)
        return local_matches

    def _find_pattern(self, synonyms, power):
        """
        Find all matches for a certain order in the length scale and then convert to meters.
        :param synonyms:
        :param power:
        """
        matches = self._match_synonyms(synonyms)
        matches_floats = self._convert_list_elements_to_float(matches)
        matches_floats = [el * 10 ** power for el in matches_floats]
        if self.debug:
            print(f"Power {power}: {matches_floats} {matches}")

        self.matches += matches_floats


pp = pprint.PrettyPrinter()


def regex_wiki(label: str, lookups_wrapper: WikiLookupWrapper):
    """Retrieve sizes from a wiki page."""
    lookup = lookups_wrapper.lookup(label)
    matches = []  # TODO maybe make empty list
    if lookup.exists() and not is_disambiguation(lookup):
        matcher = LengthsFinderRegex(lookup.text)
        matches = matcher.find_all_matches()

    return matches


def regex_google_results(label: str, htmls_lookup: dict, max_size=None):
    """Retrieve sizes from a list of html pages."""
    htmls = htmls_lookup[label]
    sizes = []
    for html in htmls:
        print(f'Length: {len(html)}')
        if max_size is not None and len(html) > max_size:
            html = html[:max_size]
        matcher = LengthsFinderRegex(html)
        print(f'done')
        sizes += matcher.find_all_matches()
        print('added to sizes')
    return sizes


def parse_documents_for_lengths(labels, lookups_wrapper: WikiLookupWrapper, htmls_lookup: dict, save_fname: str):
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

    print(f'Mean doc length: {np.mean(lengths)}')
    print(f'Median doc length: {np.median(lengths)}')

    results = {}

    for i in tqdm.trange(len(labels)):
        label = labels[i]
        sizes = []
        wiki_lengths = regex_wiki(label, lookups_wrapper)
        sizes += wiki_lengths
        sizes += regex_google_results(label, htmls_lookup)
        results[label] = sizes

    pickle.dump(results, open(os.path.join(save_fname), 'wb'))
    pp.pprint(results)
