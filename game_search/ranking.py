import math


class SimpleRanking(object):

    def order_factor_score(self, positions):
        '''
        Calculate how close are words in multiple word queries.
        The less the better.
        '''
        if len(positions) == 1:
            return 0.0

        # Quick and dirty. Replace later.
        _in_between_count = len(set.difference(
            set(range(positions[0], positions[-1] + 1)),
            set(positions)))

        return _in_between_count / math.log(len(positions), 10)

    def distance_factor_score(self, positions):
        '''
        Calculate how close terms are to the beginning of the string.
        The less the better.
        '''
        # log base 2 makes this factor more weighty.
        return math.log(sum(positions) + 1, 2) / len(positions)

    def get_score(self, positions):
        '''
        Final score, the less the better.
        Basically it's a difference score, not similarity.
        '''
        return sum([
            self.order_factor_score(positions),
            self.distance_factor_score(positions),
        ])

    def rank_search_results(self, results):
        '''
        Returns dict:
        {
            doc_id<int>: score<int>
        }
        '''
        return {
            doc_id: self.get_score(sorted(positions))
            for doc_id, positions in results.items()
        }
