import logging
from urllib.parse import urljoin

import requests

log = logging.getLogger(__name__)


class GiantbombDownloader(object):
    API_BASE_URL = 'https://www.giantbomb.com/api/'
    GAME_READ_FIELDS = [
        'name',
        # 'description',
        # 'image',
        # 'site_detail_url'
    ]

    def __init__(self, api_key, platforms=None, limit=100):
        assert type(platforms) is not str  # defence from very unwanted thing

        self.api_key = api_key
        self._platforms = ','.join(platforms if platforms else list())
        self._limit = limit
        self._default_headers = {
            # Unique UA required by Giantbomb
            'User-Agent': 'LK Downloader',
        }

    def download_all_generator(self):
        '''
        :return: generator
        '''
        results_left = 1

        offset = 0
        limit = self._limit
        while results_left > 0:
            chunk, results_left = self.download_chunk(offset)
            yield chunk
            offset += limit

    def download_chunk(self, offset):
        '''
        :param offset: int
        :return:
        '''
        download_options = {
            'format': 'json',
            'limit': self._limit,
            'offset': offset,
            'platforms': self._platforms,
            'api_key': self.api_key,
            'field_list': ','.join(self.GAME_READ_FIELDS),
        }
        response = requests.get(urljoin(self.API_BASE_URL, 'games/'),
                                params=download_options,
                                headers=self._default_headers)

        if response.status_code != 200:
            raise TypeError('Unexpected giantbomb response [{}]: {}'
                            .format(response.status_code, response.text))

        resp_data = response.json()
        if resp_data['error'] != 'OK':
            raise ValueError('Error fetch games from giantbomb: {}'
                             .format(resp_data['error']))

        cursor_pos = resp_data['offset'] + resp_data['number_of_page_results']
        results_left = (
                resp_data['number_of_total_results'] -
                cursor_pos
        )
        games = resp_data['results']
        log.info('{}/{} games downloaded (platforms: {})'
                 .format(cursor_pos, resp_data['number_of_total_results'],
                         self._platforms))
        return games, results_left
