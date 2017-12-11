import hashlib
import logging
import os
import sys
import unittest

import datasrc.fetch

URL = 'https://domain.com/file.txt'
CACHE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/resources'
CACHE_NAME = hashlib.sha256(URL.encode('utf-8')).hexdigest()


class TestFetch(unittest.TestCase):
    """
    Test class for fetch functions.
    """
    def test_get_lines_cache(self):
        datasrc.fetch.CACHE_DIR = CACHE_DIR
        lines = datasrc.fetch.get_lines(URL, sys.maxsize)
        lines_file = datasrc.fetch.get_lines_no_cache('file://' + CACHE_DIR + '/' + CACHE_NAME)
        self.assertEqual(lines, lines_file)

    def test_get_lines_error(self):
        with self.assertLogs(level=logging.ERROR):
            datasrc.fetch.CACHE_DIR = CACHE_DIR
            lines = datasrc.fetch.get_lines(URL + 'x', sys.maxsize)
            self.assertEqual(lines, [])

    def test_write_read_cache(self):
        datasrc.fetch.CACHE_DIR = '/tmp'
        lines = datasrc.fetch.get_lines_no_cache('file://' + CACHE_DIR + '/' + CACHE_NAME)
        datasrc.fetch.write_to_cache(lines, CACHE_DIR + '/' + CACHE_NAME)
        lines_cache = datasrc.fetch.read_from_cache(CACHE_DIR + '/' + CACHE_NAME)
        self.assertEqual(lines, lines_cache)

    def test_write_to_cache_error(self):
        datasrc.fetch.CACHE_DIR = '/tmp'
        with self.assertLogs(level=logging.ERROR):
            datasrc.fetch.write_to_cache([], '/invalid/path/file.txt')

    def test_read_from_cache_error(self):
        datasrc.fetch.CACHE_DIR = '/tmp'
        with self.assertLogs(level=logging.ERROR):
            lines = datasrc.fetch.read_from_cache('/invalid/path/file.txt')
            self.assertEqual(lines, None)

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.CRITICAL)


if __name__ == '__main__':
    unittest.main()
