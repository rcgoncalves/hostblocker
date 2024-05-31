import hashlib
import logging
import os
import sys
import unittest

import hostblocker.reader.cache
import hostblocker.reader.fetch

from typing import Self, Final


URL: Final[str] = 'https://example.com/file.txt'
CACHE_DIR: Final[str] = os.path.dirname(os.path.abspath(__file__)) + '/resources'
CACHE_NAME: Final[str] = hashlib.sha256(URL.encode('utf-8')).hexdigest()


class TestFetch(unittest.TestCase):
    """
    Test class for fetch functions.
    """
    def test_get_lines_cache(self: Self) -> None:
        hostblocker.reader.cache.CACHE_DIR = CACHE_DIR
        lines = hostblocker.reader.fetch.get_lines(URL, sys.maxsize)
        lines_file = hostblocker.reader.fetch.get_lines_no_cache(f'file://{CACHE_DIR}/{CACHE_NAME}')
        self.assertEqual(lines, lines_file)

    def test_write_read_cache(self: Self) -> None:
        hostblocker.reader.cache.CACHE_DIR = '/tmp'  # noqa: S108
        lines = hostblocker.reader.fetch.get_lines_no_cache(f'file://{CACHE_DIR}/{CACHE_NAME}')
        assert lines
        assert hostblocker.reader.cache.write(URL, lines)
        lines_cache = hostblocker.reader.cache.read(URL)
        self.assertEqual(lines, lines_cache)

    def test_read_cache_fail(self: Self) -> None:
        hostblocker.reader.cache.CACHE_DIR = '/tmp/x'  # noqa: S108
        self.assertFalse(hostblocker.reader.cache.read(URL))

    def test_write_cache_fail(self: Self) -> None:
        hostblocker.reader.cache.CACHE_DIR = '/xpto/abc'
        self.assertFalse(hostblocker.reader.cache.write(URL, [b'x', b'y']))

    @classmethod
    def set_up_class(cls: type[Self]) -> None:
        logging.basicConfig(level=logging.CRITICAL)


if __name__ == '__main__':
    unittest.main()
