from wikipediaapi import WikipediaPage
from typing import List

from retrieve_wikipedia_data import DOWNLOAD_ATTRIBUTES, retrieve_wikipedia_pages


def test_wikipedia_scraper():
    """Integration test for wikipedia scraper to test that it retrieves all data."""
    searches = ['tiger']
    lookups: List[WikipediaPage] = retrieve_wikipedia_pages(searches)
    for lookup in lookups:
        called = lookup._called
        for key, call_happened in called.items():
            if key in DOWNLOAD_ATTRIBUTES:
                assert call_happened, f"Have not called {key}"
