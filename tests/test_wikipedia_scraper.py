from thesis_scraper.scraping.wikipedia import DOWNLOAD_ATTRIBUTES, retrieve_wikipedia_pages


def test_wikipedia_scraper():
    """Integration test for wikipedia scraper to test that it retrieves all data."""
    searches = ['tiger']
    ids = ['tiger123']
    lookups: dict = retrieve_wikipedia_pages(searches, ids)
    lookup = lookups[ids[0]]
    called = lookup._called
    for key, call_happened in called.items():
        if key in DOWNLOAD_ATTRIBUTES:
            assert call_happened, f"Have not called {key}"
