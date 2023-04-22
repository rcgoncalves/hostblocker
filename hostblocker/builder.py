import collections
import logging

import hostblocker.functions.filters
import hostblocker.functions.mappers
import hostblocker.reader.fetch

from typing import Any

def apply_blacklist(
        hosts: dict[str, int],
        blacklist: str,
        threshold: int = 1) -> dict[str, int]:
    """
    Applies the blacklist, changing the value (score) of the blacklisted hosts to 9999.

    :param hosts: the map of hosts to their score.
    :param blacklist: the path to the blacklist file (or None).
    :param threshold: the score threshold to include a domain in the output (default: 1).
    :return: the modified hosts map.
    """
    if blacklist:
        try:
            with open(blacklist) as file:
                for line in file.readlines():
                    domain = line.strip()
                    if hosts[domain] >= threshold:
                        logging.info('domain already blocked: %s (score: %d)',
                                     domain, hosts[domain])
                    else:
                        logging.debug('blocking domain %s (previous score: %d)',
                                      domain, hosts[domain])
                    hosts[domain] = 9999
        except OSError:
            logging.exception('IO error applying blacklist')
    return hosts


def apply_whitelist(
        hosts: dict[str, int],
        whitelist: str,
        threshold: int = 1) -> dict[str, int]:
    """
    Applies the whitelist, changing the value (score) of the whitelisted hosts to 0.

    :param hosts: the map of hosts to their score.
    :param whitelist: the path to the whitelist (or None)
    :param threshold: the score threshold to include a domain in the output (default: 1).
    :return: the modified hosts map.
    """
    if whitelist:
        try:
            with open(whitelist) as file:
                for line in file.readlines():
                    domain = line.strip()
                    if hosts[domain] < threshold:
                        logging.info('domain not blocked: %s (score: %d)', domain, hosts[domain])
                    else:
                        logging.debug('unblocking domain %s (previous score: %d)',
                                      domain, hosts[domain])
                    hosts[domain.rstrip()] = 0
        except OSError:
            logging.exception('IO error applying whitelist')
    return hosts


def filter_score(
        hosts: dict[str, int],
        threshold: int = 1) -> list[str]:
    """
    Filters the hosts based on a score threshold.
    The list returned is ordered by reverse domain name.

    :param hosts: the map of hosts to their score.
    :param threshold: the score threshold to include a domain in the output (default: 1).
    :return:
    """
    hosts_list = []
    for host, score in hosts.items():
        if score > threshold:
            hosts_list.append(host)
        elif score > 0.9 * threshold:
            logging.info('host %s discarded, but score is above 90%% of threshold (%d)',
                         host, score)
    logging.info('score filter: %d/%d (threshold: %d)', len(hosts_list), len(hosts), threshold)
    return sorted(hosts_list, key=reverse_domain)


def build_from_sources(
        config: dict[str, Any],
        cache: int = 0) -> dict[str, int]:
    """
    Builds the initial hosts map from the sources list, which associates a score to each host domain read.

    :param config: the sources configuration read from the YAML file.
    :param cache: number of hours to cache files.
    :return: the hosts map.
    """
    # dictionary where values have value 0 by default
    hosts: dict[str, int] = collections.defaultdict(int)
    for item in config['sources']:
        url = item['url']
        logging.info('processing list URL %s', url)
        lines = hostblocker.reader.fetch.get_lines(url, cache)
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
        lines: list[bytes],
        hosts: dict[str, int],
        mappers: list[str],
        filters: list[str],
        score: int = 1) -> dict[str, int]:
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
            getattr(hostblocker.functions.mappers, mapper)
        except AttributeError:
            logging.warning('invalid mapper: %s', mapper)
            mappers.remove(mapper)
    logging.debug('mappers: %s', str(mappers))
    for filterr in filters[:]:
        try:
            getattr(hostblocker.functions.filters, filterr)
        except AttributeError:
            logging.warning('invalid filter: %s', filterr)
            filters.remove(filterr)
    logging.debug('filters: %s', str(filters))
    count = 0
    for line in lines:
        line_str = line.decode('latin1').strip()
        line_str = map_line(line_str, mappers)
        if filter_line(line_str, filters):
            hosts[line_str] += score
            count += 1
    logging.info('added %d domains', count)
    return hosts


def map_line(
        line: str,
        mappers: list[str]) -> str:
    """
    Applies a sequence of mappers to a line, returning the modified line.
    Assumes the mappers are valid functions.

    :param line: the line.
    :param mappers: the sequence of mappers.
    :return: the modified line.
    """
    if mappers:
        for f in mappers:
            line = getattr(hostblocker.functions.mappers, f)(line)
    return line


def filter_line(
        line: str,
        filters: list[str]) -> bool:
    """
    Applies a sequence of filters to a line.
    Assumes the filters are valid functions.

    :param line: the line.
    :param filters: the sequence of filters.
    :return: True if the line met all filter conditions; False otherwise.
    """
    if filters:
        for f in filters:
            if not getattr(hostblocker.functions.filters, f)(line):
                return False
    return True


def reverse_domain(domain: str) -> str:
    """
    Reverses the segments of a domain name.

    :param domain: the domain to reverse.
    :return: the reversed domain.
    """
    return '.'.join(reversed(domain.split('.')))
