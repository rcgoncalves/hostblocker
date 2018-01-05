import logging
import urllib.request
from typing import List, Union

import hostblocker.reader.cache


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
        lines = hostblocker.reader.cache.read(url, cache)
        if lines is None:
            logging.debug('no cache for URL %s', url)
            lines = get_lines_no_cache(url)
            if lines is None:
                lines = []
            else:
                hostblocker.reader.cache.write(url, lines)
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
                                     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:57.0) '
                                                   'Gecko/20100101 Firefox/57.0'
                                 })
    try:
        data = urllib.request.urlopen(req, timeout=10)
        lines = data.readlines()
    except (urllib.request.HTTPError, urllib.request.URLError, IOError):
        logging.exception('error fetching data from URL %s', url)
        lines = None
    return lines
