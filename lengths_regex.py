import re


# TODO: think about float vs int. e.g. we should also be able to find 1.5 meters
# TODO: if the meters is at the end of the string, with no punctuation mark, it will miss it, e.g. 'he is 6 meter'

class LengthsFinderRegex:
    """
    Find all lengths in a string (e.g. article) by matching some simple regular expressions.
    """

    def __init__(self, text):
        self.number_pattern = '[0-9]*.[0-9]*'
        self.text = text
        self.matches = list()

    def find_all_matches(self):
        self._find_meters()
        return self.matches

    @staticmethod
    def _convert_list_elements_to_float(matches):
        return [float(el) for el in matches]

    def _match_synonyms(self, synonyms):
        local_matches = list()
        # [ ,.;:$]
        for syn in synonyms:
            local_matches += re.findall(rf'({self.number_pattern})[ ]?{syn}[ ,.;:]', self.text)
        return local_matches

    def _find_meters(self):
        meter_synonyms = ['meters', 'meter', 'm']
        meter_matches = self._match_synonyms(meter_synonyms)
        self.matches += self._convert_list_elements_to_float(meter_matches)
