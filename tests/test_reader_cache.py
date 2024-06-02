import hashlib
import os
import sys
from typing import Final

import hostblocker.reader.cache
import hostblocker.reader.fetch


URL: Final[str] = 'https://example.com/file.txt'
CACHE_DIR: Final[str] = os.path.dirname(os.path.abspath(__file__)) + '/resources'
CACHE_NAME: Final[str] = hashlib.sha256(URL.encode('utf-8')).hexdigest()


def test_get_lines_cache() -> None:
    hostblocker.reader.cache.CACHE_DIR = CACHE_DIR
    lines = hostblocker.reader.fetch.get_lines(URL, sys.maxsize)
    lines_file = hostblocker.reader.fetch.get_lines_no_cache(f'file://{CACHE_DIR}/{CACHE_NAME}')
    assert lines == lines_file


def test_write_read_cache() -> None:
    hostblocker.reader.cache.CACHE_DIR = '/tmp'  # noqa: S108
    lines = hostblocker.reader.fetch.get_lines_no_cache(f'file://{CACHE_DIR}/{CACHE_NAME}')
    assert lines
    assert hostblocker.reader.cache.write(URL, lines)
    lines_cache = hostblocker.reader.cache.read(URL)
    assert lines == lines_cache


def test_read_cache_fail() -> None:
    hostblocker.reader.cache.CACHE_DIR = '/tmp/x'  # noqa: S108
    assert not hostblocker.reader.cache.read(URL)


def test_write_cache_fail() -> None:
    hostblocker.reader.cache.CACHE_DIR = '/xpto/abc'
    assert not hostblocker.reader.cache.write(URL, [b'x', b'y'])
