import io
import logging
import os
import tempfile
import unittest
from typing import List

import builder.write_hosts


class TestWriteHosts(unittest.TestCase):
    """
    Test class for writing hosts.
    """
    dir_path = os.path.dirname(os.path.abspath(__file__))
    hosts = {'domain.com': 3, 'domain.net': 2, 'domain.org': 1}
    hosts_score = {'0.0.0.0 domain.com', '0.0.0.0 domain.net'}
    hosts_all = {'0.0.0.0 domain.com', '0.0.0.0 domain.net', '0.0.0.0 domain.org'}
    header = ['127.0.0.1 localhost localhost.local', '1.2.3.4   domain.com',
              '1.2.3.4   app.domain.com']

    @staticmethod
    def read_entries(file: io.TextIOWrapper) -> List[str]:
        """
        Returns the lines of a text file.

        :param file: the file.
        :return: the lines of the file.
        """
        return file.readlines()

    def test_write_hosts_list(self):
        with tempfile.TemporaryFile('r+') as file:
            builder.write_hosts.write_hosts_list(set(self.hosts.keys()), file)
            file.seek(0)
            lines = self.read_entries(file)
        self.assertEqual(len(lines), 3)
        self.assertEqual(set(map(str.strip, lines)), self.hosts_all)

    def test_write_hosts_list_error(self):
        with tempfile.TemporaryFile('r') as file:
            with self.assertLogs(level=logging.ERROR):
                self.assertTrue(
                    builder.write_hosts.write_hosts_list(set(self.hosts.keys()), file) > 0
                )

    def test_write_header(self):
        with tempfile.TemporaryFile('r+') as file:
            builder.write_hosts.write_header(self.dir_path + '/resources/header.txt', file)
            file.seek(0)
            lines = self.read_entries(file)
        self.assertEqual(len(lines), 3)
        self.assertEqual(list(map(str.strip, lines)), self.header)

    def test_write_header_error(self):
        with tempfile.TemporaryFile('w') as file:
            with self.assertLogs(level=logging.ERROR):
                self.assertTrue(
                    builder.write_hosts.write_header('none', file) > 0
                )
        with tempfile.TemporaryFile('r') as file:
            with self.assertLogs(level=logging.ERROR):
                self.assertTrue(
                    builder.write_hosts.write_header(self.dir_path + '/resources/header.txt', file)
                    > 0
                )

    def test_write_hosts(self):
        with tempfile.NamedTemporaryFile('r+') as file:
            builder.write_hosts.write_hosts(self.hosts,
                                            self.dir_path + '/resources/header.txt',
                                            file.name,
                                            2)
            lines = self.read_entries(file)
        self.assertEqual(len(lines), 10)
        self.assertEqual(lines[0], builder.write_hosts.APP_HEADER)
        self.assertTrue(lines[1].startswith('### BEGIN'))
        self.assertEqual(list(map(str.strip, lines[2:5])), self.header)
        self.assertTrue(lines[5].startswith('### END'))
        self.assertTrue(lines[6].startswith('### BEGIN'))
        self.assertEqual(set(map(str.strip, lines[7:9])), self.hosts_score)
        self.assertTrue(lines[9].startswith('### END'))

    def test_write_hosts_error(self):
        with self.assertLogs(level=logging.ERROR):
            self.assertTrue(
                builder.write_hosts.write_hosts(dict({}),
                                                self.dir_path + '/resources/header.txt',
                                                '/tmp/invalid/output/path/file.txt',
                                                1)
                > 0
            )

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.CRITICAL)


if __name__ == '__main__':
    unittest.main()
