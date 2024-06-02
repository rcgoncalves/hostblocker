import collections
import os
from typing import Final

import hostblocker.functions.filters
import hostblocker.builder
import hostblocker.reader.fetch


DIR_PATH: Final[str] = os.path.dirname(os.path.abspath(__file__))


def test_process_lines_hosts() -> None:
    lines = hostblocker.reader.fetch.get_lines(f'file://{DIR_PATH}/resources/hosts.txt')
    hosts: dict[str, int] = collections.defaultdict(int)
    hosts = hostblocker.builder.process_lines(lines, hosts,
                                              ['remove_ip_local', 'remove_comments', 'trim'],
                                              ['is_not_blank', 'is_valid_domain'])
    assert len(hosts) == 6
    for key in hosts:
        assert key
        assert hostblocker.functions.filters.is_valid_domain(key)


def test_process_lines_list() -> None:
    lines = hostblocker.reader.fetch.get_lines(f'file://{DIR_PATH}/resources/list.txt')
    hosts: dict[str, int] = collections.defaultdict(int)
    hosts = hostblocker.builder.process_lines(lines, hosts, ['remove_comments', 'trim'], ['is_not_blank'])
    assert len(hosts) == 7
    for key in hosts:
        assert key
        assert hostblocker.functions.filters.is_valid_domain(key)


def test_process_lines_adblock() -> None:
    lines = hostblocker.reader.fetch.get_lines(f'file://{DIR_PATH}/resources/adblock.txt')
    hosts: dict[str, int] = collections.defaultdict(int)
    hosts = hostblocker.builder.process_lines(lines, hosts,
                                              ['remove_adblock_text', 'remove_adblock_comments'],
                                              ['is_not_blank'])
    assert len(hosts) == 6
    for key in hosts:
        assert key
        assert hostblocker.functions.filters.is_valid_domain(key)


def test_process_lines_list_invalid() -> None:
    lines = hostblocker.reader.fetch.get_lines(f'file://{DIR_PATH}/resources/list.txt')
    hosts: dict[str, int] = collections.defaultdict(int)
    hosts = hostblocker.builder.process_lines(lines, hosts,
                                              ['remove_comments', '_invalid_', 'trim'],
                                              ['is_not_blank', '_invalid_'])
    assert len(hosts) == 7
    for key in hosts:
        assert key
        assert hostblocker.functions.filters.is_valid_domain(key)


def test_apply_whitelist() -> None:
    lines = hostblocker.reader.fetch.get_lines(f'file://{DIR_PATH}/resources/list.txt')
    hosts: dict[str, int] = collections.defaultdict(int)
    hosts = hostblocker.builder.process_lines(lines, hosts, ['remove_comments'], ['is_not_blank'])
    hosts = hostblocker.builder.apply_whitelist(hosts, f'{DIR_PATH}/resources/apply.txt')
    for key in hosts:
        if key in {'example.com', 'app.example.com'}:
            assert hosts[key] == 0
        else:
            assert hosts[key] == 1


def test_apply_whitelist_error() -> None:
    hosts: dict[str, int] = collections.defaultdict(int)
    hosts = hostblocker.builder.apply_whitelist(hosts, f'{DIR_PATH}/resources/none')
    assert len(hosts) == 0


def test_apply_blacklist() -> None:
    lines = hostblocker.reader.fetch.get_lines(f'file://{DIR_PATH}/resources/list.txt')
    hosts: dict[str, int] = collections.defaultdict(int)
    hosts = hostblocker.builder.process_lines(lines, hosts, ['remove_comments'], ['is_not_blank'])
    hosts = hostblocker.builder.apply_blacklist(hosts, f'{DIR_PATH}/resources/apply.txt')
    for key in hosts:
        if key in {'example.com', 'app.example.com'}:
            assert hosts[key] == 9999
        else:
            assert hosts[key] == 1


def test_apply_blacklist_error() -> None:
    hosts: dict[str, int] = collections.defaultdict(int)
    hosts = hostblocker.builder.apply_blacklist(hosts, f'{DIR_PATH}/resources/none')
    assert len(hosts) == 0


def test_filter_score() -> None:
    lines = hostblocker.reader.fetch.get_lines(f'file://{DIR_PATH}/resources/list.txt')
    hosts: dict[str, int] = collections.defaultdict(int)
    hosts = hostblocker.builder.process_lines(lines, hosts, ['remove_comments'], ['is_not_blank'])
    hosts_list = hostblocker.builder.filter_score(hosts, 0)
    assert len(hosts_list) == len(hosts)


def test_filter_score_empty() -> None:
    lines = hostblocker.reader.fetch.get_lines(f'file://{DIR_PATH}/resources/list.txt')
    hosts: dict[str, int] = collections.defaultdict(int)
    hosts = hostblocker.builder.process_lines(lines, hosts, ['remove_comments'], ['is_not_blank'])
    hosts_list = hostblocker.builder.filter_score(hosts, 1)
    assert len(hosts_list) == 0


def test_build_from_sources() -> None:
    config = {
        'mappers': ['trim'],
        'filters': ['is_not_blank'],
        'sources': [
            {
                'url': 'http://example.com/file.txt',
                'score': 1,
            },
            {
                'url': f'file://{DIR_PATH}/resources/list.txt',
                'score': 1,
                'mappers': ['remove_comments'],
                'filters': ['is_valid_domain'],
                'header': 1
            }
        ]
    }
    hosts = hostblocker.builder.build_from_sources(config)
    assert len(hosts) == 7
