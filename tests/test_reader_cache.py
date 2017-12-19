import hashlib
import logging
import os
import sys
import unittest

import hostblocker.reader.cache
import hostblocker.reader.fetch


URL = 'https://example.com/file.txt'
CACHE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/resources'
CACHE_NAME = hashlib.sha256(URL.encode('utf-8')).hexdigest()


class TestFetch(unittest.TestCase):
    """
    Test class for fetch functions.
    """
    def test_get_lines_cache(self):
        hostblocker.reader.cache.CACHE_DIR = CACHE_DIR
        lines = hostblocker.reader.fetch.get_lines(URL, sys.maxsize)
        lines_file = hostblocker.reader.fetch.get_lines_no_cache('file://' + CACHE_DIR
                                                                 + '/' + CACHE_NAME)
        self.assertEqual(lines, lines_file)

    def test_write_read_cache(self):
        hostblocker.reader.fetch.CACHE_DIR = '/tmp'
        lines = hostblocker.reader.fetch.get_lines_no_cache('file://' + CACHE_DIR + '/'
                                                            + CACHE_NAME)
        hostblocker.reader.cache.write(URL, lines)
        lines_cache = hostblocker.reader.cache.read(URL)
        self.assertEqual(lines, lines_cache)

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.CRITICAL)


if __name__ == '__main__':
    unittest.main()
