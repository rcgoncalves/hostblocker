import io
import logging
import os
import tempfile
import unittest
from typing import List

import hostblocker.writer.hosts


class TestWriteHosts(unittest.TestCase):
    """
    Test class for writing hosts.
    """
    dir_path = os.path.dirname(os.path.abspath(__file__))
    hosts = ['example.com', 'example.net', 'example.org']
    hosts_write = ['0.0.0.0 example.com', '0.0.0.0 example.net', '0.0.0.0 example.org']
    header = ['127.0.0.1 localhost localhost.local', '1.2.3.4   example.com',
              '1.2.3.4   app.example.com']

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
            hostblocker.writer.hosts.write_hosts_list(self.hosts, file)
            file.seek(0)
            lines = self.read_entries(file)
        self.assertEqual(len(lines), 3)
        self.assertEqual(list(map(str.strip, lines)), self.hosts_write)

    def test_write_hosts_list_error(self):
        with tempfile.TemporaryFile('r') as file:
            with self.assertLogs(level=logging.ERROR):
                self.assertTrue(hostblocker.writer.hosts.write_hosts_list(self.hosts, file) > 0)

    def test_write_header(self):
        with tempfile.TemporaryFile('r+') as file:
            hostblocker.writer.hosts.write_header(self.dir_path + '/resources/header.txt', file)
            file.seek(0)
            lines = self.read_entries(file)
        self.assertEqual(len(lines), 3)
        self.assertEqual(list(map(str.strip, lines)), self.header)

    def test_write_header_error(self):
        with tempfile.TemporaryFile('w') as file:
            with self.assertLogs(level=logging.ERROR):
                self.assertTrue(
                    hostblocker.writer.hosts.write_header('none', file) > 0
                )
        with tempfile.TemporaryFile('r') as file:
            with self.assertLogs(level=logging.ERROR):
                self.assertTrue(
                    hostblocker.writer.hosts.write_header(self.dir_path + '/resources/header.txt',
                                                          file)
                    > 0
                )

    def test_write(self):
        with tempfile.NamedTemporaryFile('r+') as file:
            hostblocker.writer.hosts.write(self.hosts,
                                           self.dir_path + '/resources/header.txt',
                                           file.name)
            lines = self.read_entries(file)
        self.assertEqual(len(lines), 11)
        self.assertEqual(lines[0], hostblocker.writer.hosts.APP_HEADER)
        self.assertTrue(lines[1].startswith('### BEGIN'))
        self.assertEqual(list(map(str.strip, lines[2:5])), self.header)
        self.assertTrue(lines[5].startswith('### END'))
        self.assertTrue(lines[6].startswith('### BEGIN'))
        self.assertEqual(list(map(str.strip, lines[7:10])), self.hosts_write)
        self.assertTrue(lines[10].startswith('### END'))

    def test_write_error(self):
        with self.assertLogs(level=logging.ERROR):
            self.assertTrue(
                hostblocker.writer.hosts.write([],
                                               self.dir_path + '/resources/header.txt',
                                               '/tmp/invalid/output/path/file.txt')
                > 0
            )

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.CRITICAL)


if __name__ == '__main__':
    unittest.main()
