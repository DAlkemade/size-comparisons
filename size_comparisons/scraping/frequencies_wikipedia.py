from __future__ import division

from typing import List

import lucene
# noinspection PyUnresolvedReferences
import tqdm
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


def find_frequencies_wikipedia(terms: List[str], index_location: str):
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
