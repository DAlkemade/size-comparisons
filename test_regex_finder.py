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
    finder = LengthsFinderRegex('the tiger is 4 meters long, wait no, 3.5 meters')
    matches = finder.find_all_matches()
    assert matches[0] == 4.
    assert matches[1] == 3.5
