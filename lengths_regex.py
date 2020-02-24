import re

# The index is the power of 10 it is compared to meters
UNITS = {
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

    def __init__(self, text):
        self.number_pattern = '[0-9]*.[0-9]*'
        self.text = text
        self.matches = list()

    def find_all_matches(self):
        for power, synonym_list in UNITS.items():
            self._find_pattern(synonym_list, power)
        return self.matches

    @staticmethod
    def _convert_list_elements_to_float(matches):
        return [float(el) for el in matches]

    def _match_synonyms(self, synonyms):
        local_matches = list()
        # [ ,.;:$]
        for syn in synonyms:
            local_matches += re.findall(rf'([ ]{self.number_pattern})[ ]?{syn}[ ,.;:]', self.text)
        return local_matches

    def _find_pattern(self, synonyms, power):
        centimeter_matches = self._match_synonyms(synonyms)
        centimeter_matches_floats = self._convert_list_elements_to_float(centimeter_matches)
        centimeter_matches_floats = [el * 10 ** power for el in centimeter_matches_floats]
        self.matches += centimeter_matches_floats
