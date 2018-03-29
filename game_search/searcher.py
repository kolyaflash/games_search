from collections import defaultdict

from .utils import tokenize_string


class SimpleSearcher(object):
    '''
    Simple searcher that parse input string into tokens and applies
    pre-set predicate's logic to find documents in index.

    Some extra features, like symbols or words in input to make search
    results more precise, can be added with another Searcher class.
    '''

    def __init__(self, operator='AND'):
        self._operator = operator

    def _filter_documents(self, index):
        docs_ids_sets = [set([i[0] for i in idx]) for idx in index.values()]

        if self._operator == 'AND':
            found_docs = set.intersection(*docs_ids_sets)
        elif self._operator == 'OR':
            found_docs = set.union(*docs_ids_sets)
        else:
            raise ValueError("Operator {} is not supported".format(self._operator))

        return found_docs

    def search(self, index, input_string):
        '''
        Returns dict where keys are found documents ids and values
        is list of position indexes for substrings found in input_string.

        {
            doc_id<int>: [ searched_term1_pos<int>, searched_term2_pos<int>, ... ],
            ...
        }
        '''
        tokens = tokenize_string(input_string)

        index_slice = {t: index.get(t, []) for t in tokens}
        result_docs_ids = self._filter_documents(index_slice)

        result = defaultdict(list)
        for token_indexes in index_slice.values():
            for idx in token_indexes:
                if idx[0] in result_docs_ids:
                    result[idx[0]].append(idx[1])

        return result
