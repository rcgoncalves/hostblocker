import collections
import logging
import os
import unittest

import hostblocker.functions.filters
import hostblocker.builder
import hostblocker.reader.fetch


class TestProcessHosts(unittest.TestCase):
    """
    Test class for processing hosts.
    """
    dir_path = os.path.dirname(os.path.abspath(__file__))

    def test_process_lines_hosts(self):
        lines = hostblocker.reader.fetch.get_lines('file://' + str(self.dir_path)
                                                   + '/resources/hosts.txt')
        hosts = collections.defaultdict(int)
        hosts = hostblocker.builder.process_lines(lines, hosts,
                                                  ['remove_ip_local', 'remove_comments', 'trim'],
                                                  ['is_not_blank', 'is_valid_domain'])
        self.assertEqual(len(hosts), 6)
        for key in hosts:
            self.assertTrue(key)
            self.assertTrue(hostblocker.functions.filters.is_valid_domain(key))

    def test_process_lines_list(self):
        lines = hostblocker.reader.fetch.get_lines('file://' + str(self.dir_path)
                                                   + '/resources/list.txt')
        hosts = collections.defaultdict(int)
        hosts = hostblocker.builder.process_lines(lines, hosts,
                                                  ['remove_comments', 'trim'],
                                                  ['is_not_blank'])
        self.assertEqual(len(hosts), 7)
        for key in hosts:
            self.assertTrue(key)
            self.assertTrue(hostblocker.functions.filters.is_valid_domain(key))

    def test_process_lines_adblock(self):
        lines = hostblocker.reader.fetch.get_lines('file://' + str(self.dir_path)
                                                   + '/resources/adblock.txt')
        hosts = collections.defaultdict(int)
        hosts = hostblocker.builder.process_lines(lines, hosts,
                                                  ['remove_adblock_text',
                                                   'remove_adblock_comments'],
                                                  ['is_not_blank'])
        self.assertEqual(len(hosts), 6)
        for key in hosts:
            self.assertTrue(key)
            self.assertTrue(hostblocker.functions.filters.is_valid_domain(key))

    def test_process_lines_list_invalid(self):
        lines = hostblocker.reader.fetch.get_lines('file://' + str(self.dir_path)
                                                   + '/resources/list.txt')
        hosts = collections.defaultdict(int)
        hosts = hostblocker.builder.process_lines(lines, hosts,
                                                  ['remove_comments', '_invalid_', 'trim'],
                                                  ['is_not_blank', '_invalid_'])
        self.assertEqual(len(hosts), 7)
        for key in hosts:
            self.assertTrue(key)
            self.assertTrue(hostblocker.functions.filters.is_valid_domain(key))

    def test_apply_whitelist(self):
        lines = hostblocker.reader.fetch.get_lines('file://' + str(self.dir_path)
                                                   + '/resources/list.txt')
        hosts = collections.defaultdict(int)
        hosts = hostblocker.builder.process_lines(lines, hosts,
                                                  ['remove_comments'],
                                                  ['is_not_blank'])
        hosts = hostblocker.builder.apply_whitelist(hosts,
                                                    str(self.dir_path) + '/resources/apply.txt')
        for key in hosts:
            if key in ['example.com', 'app.example.com']:
                self.assertEqual(hosts[key], 0)
            else:
                self.assertEqual(hosts[key], 1)

    def test_apply_whitelist_error(self):
        with self.assertLogs(level=logging.ERROR):
            hosts = collections.defaultdict(int)
            hosts = hostblocker.builder.apply_whitelist(hosts,
                                                        str(self.dir_path) + '/resources/none')
            self.assertEqual(len(hosts), 0)

    def test_apply_blacklist(self):
        lines = hostblocker.reader.fetch.get_lines('file://' + str(self.dir_path)
                                                   + '/resources/list.txt')
        hosts = collections.defaultdict(int)
        hosts = hostblocker.builder.process_lines(lines, hosts,
                                                  ['remove_comments'],
                                                  ['is_not_blank'])
        hosts = hostblocker.builder.apply_blacklist(hosts,
                                                    str(self.dir_path) + '/resources/apply.txt')
        for key in hosts:
            if key in ['example.com', 'app.example.com']:
                self.assertEqual(hosts[key], 9999)
            else:
                self.assertEqual(hosts[key], 1)

    def test_apply_blacklist_error(self):
        with self.assertLogs(level=logging.ERROR):
            hosts = collections.defaultdict(int)
            hosts = hostblocker.builder.apply_blacklist(hosts,
                                                        str(self.dir_path) + '/resources/none')
            self.assertEqual(len(hosts), 0)

    def test_filter_score(self):
        lines = hostblocker.reader.fetch.get_lines('file://' + str(self.dir_path)
                                                   + '/resources/list.txt')
        hosts = collections.defaultdict(int)
        hosts = hostblocker.builder.process_lines(lines, hosts,
                                                  ['remove_comments'],
                                                  ['is_not_blank'])
        hosts_list = hostblocker.builder.filter_score(hosts, 0)
        self.assertEqual(len(hosts_list), len(hosts))

    def test_filter_score_empty(self):
        lines = hostblocker.reader.fetch.get_lines('file://' + str(self.dir_path)
                                                   + '/resources/list.txt')
        hosts = collections.defaultdict(int)
        hosts = hostblocker.builder.process_lines(lines, hosts,
                                                  ['remove_comments'],
                                                  ['is_not_blank'])
        hosts_list = hostblocker.builder.filter_score(hosts, 1)
        self.assertEqual(len(hosts_list), 0)

    def test_build_from_sources(self):
        config = {
            'mappers': ['trim'],
            'filters': ['is_not_blank'],
            'sources': [
                {
                    'url': 'http://example.com/file.txt',
                    'score': 1,
                },
                {
                    'url': 'file://' + self.dir_path + '/resources/list.txt',
                    'score': 1,
                    'mappers': ['remove_comments'],
                    'filters': ['is_valid_domain'],
                    'header': 1
                }
            ]
        }
        hosts = hostblocker.builder.build_from_sources(config)
        self.assertEqual(len(hosts), 7)

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.CRITICAL)


if __name__ == '__main__':
    unittest.main()
