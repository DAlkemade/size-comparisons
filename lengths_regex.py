import re


# TODO: think about float vs int. e.g. we should also be able to find 1.5 meters

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

    def _find_meters(self):
        meter_matches = re.findall(rf'({self.number_pattern}) meters', self.text)
        self.matches += self._convert_list_elements_to_float(meter_matches)
