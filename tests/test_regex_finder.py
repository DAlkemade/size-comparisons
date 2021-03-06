import pytest
import wikipediaapi
from matplotlib import pyplot as plt

from size_comparisons.scraping.lengths_regex import LengthsFinderRegex


@pytest.fixture
def wikipedia():
    return wikipediaapi.Wikipedia('en')


def test_lookup(wikipedia):
    """
    Check if there is no connection or something.
    :param wikipedia: wikipedia api fixture.
    """
    wikipedia.page("Tiger")


def test_meters_pattern():
    """
    Test whether we find the meters pattern.
    """
    finder = LengthsFinderRegex('the tiger is 4 meters long, wait no, 3.5 meters, no actually 5.5m.')
    matches, _ = finder.find_all_matches()
    strings, matches = zip(*matches)
    assert len(matches) == 3
    assert matches[0] == 4.
    assert matches[1] == 3.5
    assert matches[2] == 5.5


def test_centimeters_pattern():
    """
    Test whether we find the cm pattern.
    """
    finder = LengthsFinderRegex(
        'the tiger is 400 centimeters long, wait no, 300.5 centimeter, no actually 5.50cm. the serial number is s500m.')
    matches, _ = finder.find_all_matches()
    strings, matches = zip(*matches)
    assert len(matches) == 3
    assert matches[0] == 4.
    assert matches[1] == 300.5 / 100
    assert matches[2] == 5.5 / 100


def test_kilometers_pattern():
    """
    Test whether we find the km pattern.
    """
    finder = LengthsFinderRegex('It is 400km.')
    matches, _ = finder.find_all_matches()
    strings, matches = zip(*matches)
    assert len(matches) == 1
    assert matches[0] == 400000.


def test_no_pattern():
    """
    Test whether if it skips a wrong pattern.
    """
    finder = LengthsFinderRegex('That is a lot of meters.')
    matches, _ = finder.find_all_matches()
    assert len(matches) == 0


def test_tiger_wiki(wikipedia):
    """
    Test whether the output of the tiger wiki page is sensible. Not a very strong test.
    """
    tiger_text = wikipedia.page('Tiger').text
    finder = LengthsFinderRegex(tiger_text, debug=False)
    matches, _ = finder.find_all_matches()
    strings, matches = zip(*matches)
    print(matches)
    plt.hist(matches)
    plt.show()
    assert len(matches) > 0

def test_typical_wikipedia_notation():
    finder = LengthsFinderRegex('will be 2 feet (0.61 m) long')
    matches, _ = finder.find_all_matches()
    strings, matches = zip(*matches)
    assert len(matches) == 2
    assert matches[0] == .6096
    assert matches[1] == .61

def test_inches_notation():
    """We are not parsing " on purpose, since it will give a lot of noise"""
    finder = LengthsFinderRegex('will be 2" long')
    matches, _ = finder.find_all_matches()
    assert len(matches) == 0

def test_id_code():

    finder = LengthsFinderRegex("https://photos.inautia.com/logosEmpresas/1/2/7/0/logo-boats-mediterrani-36113110191253696857526849654557m.jpg")
    matches, _ = finder.find_all_matches()
    assert len(matches) == 0

def test_newline():

    finder = LengthsFinderRegex("test 3.5m.\ntest 4.5m.")
    matches, _ = finder.find_all_matches()
    strings, matches = zip(*matches)
    assert len(matches) == 2

def test_newlines():

    finder = LengthsFinderRegex("\n4.5m.\n")
    matches, _ = finder.find_all_matches()
    strings, matches = zip(*matches)
    assert len(matches) == 1

def test_no_break_space():
    finder = LengthsFinderRegex("4.5&#160;meter")
    matches, _ = finder.find_all_matches()
    strings, matches = zip(*matches)
    assert len(matches) == 1
