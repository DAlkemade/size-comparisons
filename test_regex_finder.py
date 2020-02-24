import pytest
import wikipediaapi
import main
from lengths_regex import LengthsFinderRegex


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
    matches = finder.find_all_matches()
    assert len(matches) == 3
    assert matches[0] == 4.
    assert matches[1] == 3.5
    assert matches[2] == 5.5

def test_centimeters_pattern():
    """
    Test whether we find the meters pattern.
    """
    finder = LengthsFinderRegex('the tiger is 400 centimeters long, wait no, 300.5 centimeter, no actually 5.50cm.')
    matches = finder.find_all_matches()
    assert len(matches) == 3
    assert matches[0] == 4.
    assert matches[1] == 300.5 / 100
    assert matches[2] == 5.5 / 100

def test_kilometers_pattern():
    """
    Test whether we find the meters pattern.
    """
    finder = LengthsFinderRegex('It is 400km.')
    matches = finder.find_all_matches()
    assert len(matches) == 1
    assert matches[0] == 400000.
