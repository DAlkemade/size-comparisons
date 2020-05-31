import logging
import time

from bs4 import BeautifulSoup
from requests import get

logger = logging.getLogger(__name__)

HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0'
    }
class Record:
    def __init__(self, name, label):
        self.label = label
        self.name = name
        self.length = None
        self.height = None
        self.size = None
        self.top_level_synset = None
        self.count = None


def check_contains_height_length(url):
    time.sleep(2)
    raw = get(url, allow_redirects=True, headers=HEADERS).text
    soup = BeautifulSoup(raw, 'html.parser')
    spans = soup.find_all('span')
    span_contents = [span.get_text() for span in spans]
    return int('Length' in span_contents or 'Height' in span_contents)


def generate_query(query_raw: str):
    return f'https://google.com/search?q={query_raw.replace(" ", "+")}&hl=en'


def search_infoboxes(record: Record) -> None:
    record.size = check_contains_height_length(generate_query(f'{record.name} size'))
    record.height = check_contains_height_length(generate_query(f'{record.name} height'))
    record.length = check_contains_height_length(generate_query(f'{record.name} length'))
