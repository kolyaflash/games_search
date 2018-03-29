import logging
from collections import defaultdict, OrderedDict
from .searcher import SimpleSearcher
from .ranking import SimpleRanking
from .utils import tokenize_string

log = logging.getLogger(__name__)


class Indexer(object):
    """
    Implements Full Inverted Index.
    """
    def __init__(self, searcher=None, ranking=None):
        self.index = None
        self.documents = None
        self.searcher = searcher if searcher else SimpleSearcher()
        self.ranking = ranking if ranking else SimpleRanking()

    def build_index(self, documents, value_getter=None):
        self.documents = dict()
        unsorted_index = defaultdict(list)

        if value_getter is None:
            value_getter = lambda x: x

        for doc_i, doc in enumerate(documents):
            self.documents[doc_i] = doc
            tokens = tokenize_string(value_getter(doc))
            for tok_i, token in enumerate(tokens):
                unsorted_index[token].append((doc_i, tok_i))

        # Sort by key (token) and values (doc number)
        sorted_index = OrderedDict(sorted(unsorted_index.items()))

        self.index = sorted_index
        log.info("Index built. Items: {}".format(len(sorted_index)))


    def query(self, input_string):
        results = self.searcher.search(self.index, input_string)
        scores = self.ranking.rank_search_results(results)

        ranked_results = [(self.documents[i], scores[i]) for i in results.keys()]
        ranked_results.sort(key=lambda x: x[1])
        return ranked_results
