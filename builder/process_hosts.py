import collections
import logging
from typing import DefaultDict, Union, List

import builder.fetch
import datasrc.filters
import datasrc.mappers


def apply_blacklist(
        hosts: DefaultDict[str, int],
        blacklist: str,
        threshold: int=1) -> DefaultDict[str, int]:
    """
    Applies the blacklist, changing the value (score) of the blacklisted hosts to 9999.

    :param hosts: the map of hosts to their score.
    :param blacklist: the path to the blacklist file (or None).
    :param threshold: the score threshold to include a domain in the output (default: 1).
    :return: the modified hosts map.
    """
    if blacklist:
        try:
            with open(blacklist, 'r') as file:
                for line in file.readlines():
                    domain = line.strip()
                    if hosts[domain] >= threshold:
                        logging.info('domain already blocked: %s (score: %d)',
                                     domain, hosts[domain])
                    else:
                        logging.debug('blocking domain %s (previous score: %d)',
                                      domain, hosts[domain])
                    hosts[domain] = 9999
        except IOError:
            logging.exception('IO error applying blacklist')
    return hosts


def apply_whitelist(
        hosts: DefaultDict[str, int],
        whitelist: str,
        threshold: int=1) -> DefaultDict[str, int]:
    """
    Applies the whitelist, changing the value (score) of the whitelisted hosts to 0.

    :param hosts: the map of hosts to their score.
    :param whitelist: the path to the whitelist (or None)
    :param threshold: the score threshold to include a domain in the output (default: 1).
    :return: the modified hosts map.
    """
    if whitelist:
        try:
            with open(whitelist, 'r') as file:
                for line in file.readlines():
                    domain = line.strip()
                    if hosts[domain] < threshold:
                        logging.info('domain no blocked: %s (score: %d)', domain, hosts[domain])
                    else:
                        logging.debug('unblocking domain %s (previous score: %d)',
                                      domain, hosts[domain])
                    hosts[domain.rstrip()] = 0
        except IOError:
            logging.exception('IO error applying whitelist')
    return hosts


def build_from_sources(
        config: Union[dict, list, None],
        cache: int=0) -> DefaultDict[str, int]:
    """
    Builds the initial hosts map from the sources list, that associates a score to each host domain
    read.

    :param config: the sources configuration read from the YAML file.
    :param cache: number of hours to cache files.
    :return: the hosts map.
    """
    # dictionary where values have value 0 by default
    hosts = collections.defaultdict(int)
    for item in config['sources']:
        url = item['url']
        logging.info('processing list URL %s', url)
        lines = builder.fetch.get_lines(url, cache)
        if 'header' in item:
            logging.debug('discarding %d header lines', item['header'])
            del lines[:item['header']]
        mappers = config['mappers']
        if 'mappers' in item:
            mappers = item['mappers'] + mappers
        filters = config['filters']
        if 'filters' in item:
            filters = item['filters'] + filters
        hosts = process_lines(lines, hosts, mappers, filters, item['score'])
    return hosts


def process_lines(
        lines: List[bytearray],
        hosts: DefaultDict[str, int],
        mappers: List[str],
        filters: List[str],
        score: int=1) -> DefaultDict[str, int]:
    """
    Processes the lines of a file to build the hosts map.

    :param lines: the list of lines of the file.
    :param hosts: the previous hosts map.
    :param mappers: the sequence of mappers to apply to the lines.
    :param filters: the sequence of filters to apply to the lines.
    :param score: the score to assign to each domain added (default: 1).
    :return: the modified hosts map.
    """
    for mapper in mappers[:]:
        try:
            getattr(datasrc.mappers, mapper)
        except AttributeError:
            logging.warning('invalid mapper: %s', mapper)
            mappers.remove(mapper)
    logging.debug('mappers: %s', str(mappers))
    for filterr in filters[:]:
        try:
            getattr(datasrc.filters, filterr)
        except AttributeError:
            logging.warning('invalid filter: %s', filterr)
            filters.remove(filterr)
    logging.debug('filters: %s', str(filters))
    count = 0
    for line in lines:
        line = line.decode('latin1').strip()
        line = map_line(line, mappers)
        if filter_line(line, filters):
            hosts[line] += score
            count += 1
    logging.info('added %d domains', count)
    return hosts


def map_line(
        line: str,
        mappers: List[str]) -> str:
    """
    Applies a sequence of mappers to a line, returning the modified line.
    Assumes the mappers are valid functions.

    :param line: the line.
    :param mappers: the sequence of mappers.
    :return: the modified line.
    """
    if mappers:
        for f in mappers:
            line = getattr(datasrc.mappers, f)(line)
    return line


def filter_line(
        line: str,
        filters: List[str]) -> bool:
    """
    Applies a sequence of filters to a line.
    Assumes the filters are valid functions.

    :param line: the line.
    :param filters: the sequence of filters.
    :return: True if the line met all filter conditions; False otherwise.
    """
    if filters:
        for f in filters:
            if not getattr(datasrc.filters, f)(line):
                return False
    return True
