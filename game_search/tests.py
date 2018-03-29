from .indexer import Indexer
from .ranking import SimpleRanking
from .searcher import SimpleSearcher


def test_build_from_dict():
    docs = [
        {'name': 'aa bb'},
        {'name': 'cc dd'},
    ]
    indexer = Indexer()
    value_getter = lambda x: x['name']
    indexer.build_index(docs, value_getter=value_getter)
    assert len(indexer.index) == 4


def test_searcher():
    indexer = Indexer()
    indexer.build_index([
        '11 aa bb',
        'aa cc;',
        'aa bb cc',
        '',
    ])
    searcher = SimpleSearcher()

    results = searcher.search(indexer.index, 'aa')
    assert results == {0: [1], 1: [0], 2: [0]}

    results = searcher.search(indexer.index, 'aa cc')
    assert results == {1: [0, 1], 2: [0, 2]}

    results = searcher.search(indexer.index, 'ccc')
    assert results == {}


def test_searcher_disjunctive():
    indexer = Indexer()
    indexer.build_index([
        'aa bb cc aa',
        'dd bb ee',
        '',
    ])
    searcher = SimpleSearcher(operator='OR')

    results = searcher.search(indexer.index, 'aa ee')
    assert results == {0: [0, 3], 1: [2]}

    results = searcher.search(indexer.index, 'ccc')
    assert results == {}


def test_ranking_singlewords():
    indexer = Indexer()
    indexer.build_index([
        '11 aa bb',
        'aa cc;',
        'aa bb cc',
        '',
    ])
    searcher = SimpleSearcher()
    ranking = SimpleRanking()
    results = searcher.search(indexer.index, 'aa')
    scores = ranking.rank_search_results(results)
    assert scores[1] < scores[0]
    assert scores[2] == scores[1]


def test_ranking_multiwords():
    indexer = Indexer()
    indexer.build_index([
        'foo bar buzz',
        'foo buzz bar',
        'spam foo bar',
        'spam never foo do the big bar',
    ])

    searcher = SimpleSearcher()
    ranking = SimpleRanking()

    results = searcher.search(indexer.index, 'foo bar')
    scores = ranking.rank_search_results(results)

    assert scores[0] < scores[1]
    assert scores[2] < scores[1]
    assert scores[3] > scores[2]
