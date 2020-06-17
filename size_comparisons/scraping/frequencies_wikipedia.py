from __future__ import division

import logging
from typing import List

import lucene
import tqdm
# noinspection PyUnresolvedReferences
from java.nio.file import Paths
# noinspection PyUnresolvedReferences
from org.apache.lucene.analysis.standard import StandardAnalyzer
# noinspection PyUnresolvedReferences
from org.apache.lucene.index import DirectoryReader, Term
# noinspection PyUnresolvedReferences
from org.apache.lucene.queryparser.classic import QueryParser
# noinspection PyUnresolvedReferences
from org.apache.lucene.search import IndexSearcher, PhraseQuery
# noinspection PyUnresolvedReferences
from org.apache.lucene.store import FSDirectory

logger = logging.getLogger(__name__)


def find_frequencies_wikipedia(terms: List[str], index_location: str):
    """Find frequencies using a Lucene index of wikipedia."""
    # TODO doesn't find any n>1 grams due to missing location index on contents!

    logger.warning('Not working! Does not find any n>1 grams')
    # noinspection PyUnresolvedReferences
    lucene.initVM(initialheap='32m', maxheap='4G')
    file = Paths.get(index_location)
    dir = FSDirectory.open(file)
    reader = DirectoryReader.open(dir)

    freqs = {}
    for term_str in tqdm.tqdm(terms):
        term = Term("contents", term_str)
        freq = reader.totalTermFreq(term)
        freqs[term_str] = freq

    reader.close()
    return freqs
