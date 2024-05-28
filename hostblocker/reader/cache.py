import hashlib
import logging
import os
import time

from typing import Final


CACHE_VAR: Final[str] = 'HOSTBLOCKER_CACHE_PATH'
# This is mostly a constant, except for tests.
CACHE_DIR: str = os.getenv(CACHE_VAR, 'cache')


def write(
        resource: str,
        lines: list[bytes]) -> bool:
    """
    Writes lines to a cache file.

    :param resource: the identifier (URL) of the resource to write.
    :param lines: the lines to write.
    """
    try:
        if not os.path.isdir(CACHE_DIR):
            os.makedirs(CACHE_DIR, 0o755)
        cache_file = CACHE_DIR + '/' + get_resource_id(resource)
        with open(cache_file, 'wb') as file:
            for line in lines:
                file.write(line)
    except OSError:
        logging.exception('IO error writing cache')
        return False
    else:
        return True


def read(
        resource: str,
        cache: int=1) -> list[bytes] | None:
    """
    Reads lines from a cache file.

    :param resource: the identifier (URL) of the resource to lookup.
    :param cache: the number of hours to cache resources (default: 1).
    :return: the list of lines obtained from the cached result, or None if there is no valid cache
     for the resource or an error occurs.
    """
    cache_file = CACHE_DIR + '/' + get_resource_id(resource)
    try:
        if not os.path.exists(cache_file):
            expired = True
        else:
            age = (time.time() - os.stat(cache_file).st_mtime) / 3600
            expired = age > cache
            logging.debug('cache expired? %s (age: %d)', expired, age)
        if expired:
            lines = None
        else:
            with open(cache_file, 'rb') as file:
                lines = file.readlines()
    except OSError:
        logging.exception('IO error reading cache')
        lines = None
    return lines


def get_resource_id(resource: str) -> str:
    return hashlib.sha256(resource.encode('utf-8')).hexdigest()
