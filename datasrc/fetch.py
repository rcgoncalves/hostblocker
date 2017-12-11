import hashlib
import logging
import os
import time
import urllib
from typing import List, Union


CACHE_VAR = 'HOSTBLOCKER_CACHE_PATH'
CACHE_DIR = os.getenv(CACHE_VAR, 'cache')


def get_lines(
        url: str,
        cache: int=0) -> List[bytearray]:
    """
    Retrieves the lines from a URL.
    Lines may be cache, and lines may be read from cache, if cache is greater than 0, and URL is not
    of type 'file://'.

    :param url: the URL.
    :param cache: number of hours to cache files.
    :return: the list of lines.
    """
    if cache <= 0 or url.startswith('file://'):
        lines = get_lines_no_cache(url)
        if lines is None:
            lines = []
    else:
        cache_file = CACHE_DIR + '/' + hashlib.sha256(url.encode('utf-8')).hexdigest()
        if not os.path.exists(cache_file):
            expired = True
        else:
            age = (time.time() - os.stat(cache_file).st_mtime) / 3600
            expired = age > cache
            logging.debug('cache expired? %s (age: %d)', expired, age)
        if expired:
            logging.debug('no cache for URL %s', url)
            lines = get_lines_no_cache(url)
            if lines is None:
                lines = []
            else:
                write_to_cache(lines, cache_file)
        else:
            logging.debug('reading URL %s from cache (%s)', url, cache_file)
            lines = read_from_cache(cache_file)
            if lines is None:
                lines = get_lines_no_cache(url)
    return lines


def get_lines_no_cache(url: str) -> Union[List[bytearray], None]:
    """
    Retrieves the lines of a URL.

    :param url: the URL.
    :return: the list of lines, or None if an error occurs.
    """
    req = urllib.request.Request(url,
                                 data=None,
                                 headers={
                                     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13)'
                                                   ' AppleWebKit/604.4.7 (KHTML, like Gecko)'
                                                   ' Version/11.0.2 Safari/604.4.7'
                                 })
    try:
        data = urllib.request.urlopen(req)
        lines = data.readlines()
    except (urllib.request.HTTPError, urllib.request.URLError, IOError):
        logging.exception('error fetching data from URL %s', url)
        lines = None
    return lines


def write_to_cache(
        lines: List[bytearray],
        cache_file: str) -> None:
    """
    Writes lines to a cache file.

    :param lines: the lines to write.
    :param cache_file: the path to the cache file.
    """
    try:
        if not os.path.isdir(CACHE_DIR):
            os.makedirs(CACHE_DIR, 0o755)
        with open(cache_file, 'wb') as file:
            for line in lines:
                file.write(line)
    except IOError:
        logging.exception('IO error writing cache')


def read_from_cache(cache_file: str) -> Union[List[bytearray], None]:
    """
    Reads lines from a cache file.

    :param cache_file: the path to the cache file.
    :return: the list of lines, or None if an error occurs.
    """
    try:
        with open(cache_file, 'rb') as file:
            lines = file.readlines()
    except IOError:
        logging.exception('IO error reading cache')
        lines = None
    return lines
