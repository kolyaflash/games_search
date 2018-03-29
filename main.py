import argparse
import codecs
import json
import logging
import os

from game_search.downloader import GiantbombDownloader
from game_search.indexer import Indexer

dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'game_search')
logging.basicConfig(level=logging.DEBUG)

# Settings
API_KEY = os.getenv('API_KEY', '2e53b430c5e9d5a18344a0c5ee4fb91acf9f2ee2')
TMP_RES_DIR = os.getenv('TMP_RES_DIR', os.path.join(dir_path, 'tmp'))


def download(filename):
    # Platform IDs.
    platforms = [
        '21',  # NES
        '9',  # SNES
        '43',  # N64
    ]

    filepath = os.path.join(TMP_RES_DIR, '{}.json'.format(filename))

    with codecs.open(filepath, 'w', encoding='utf8') as fp:
        # TODO: Use async/threads
        results = []
        for platform_id in platforms:
            downloader = GiantbombDownloader(API_KEY, [platform_id], limit=100)
            for chunk in downloader.download_all_generator():
                results.extend(chunk)
            # for chunk in json.JSONEncoder().iterencode(iterator):
            #     fp.write(chunk)
        fp.write(json.dumps(results))


def index(filename):
    indexer = Indexer()

    filepath = os.path.join(TMP_RES_DIR, '{}.json'.format(filename))
    with codecs.open(filepath, 'r', encoding='utf8') as fp:
        indexer.build_index(json.load(fp), lambda x: x['name'])
    return indexer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Indexer CLI')
    parser.add_argument('--download', help='download all games',
                        action='store_true')
    parser.add_argument('--filename', help='filename for games list to use',
                        default='all_games')
    args = parser.parse_args()

    if args.download:
        download(args.filename)
    else:
        indexer = index(args.filename)

        while True:
            s = input("Enter search: ")
            results = indexer.query(s)
            print("Found {} results".format(len(results)))
            for res in results:
                print('{} [{}]'.format(res[0]['name'], res[1]))
