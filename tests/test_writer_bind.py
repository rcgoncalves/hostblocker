import io
import logging
import os
import tempfile
import unittest
from typing import List

import hostblocker.writer.bind


class TestWriteBind(unittest.TestCase):
    """
    Test class for writing bind.
    """
    dir_path = os.path.dirname(os.path.abspath(__file__))
    hosts = {'example.com': 3, 'x.example.com': 2, 'y.example.com': 1, 'example.net': 3,
             'x.example.net': 2, 'y.example.net': 2, 'z.example.net': 2, 'example.org': 0}
    hosts_score = {'example.com CNAME .', 'x.example.com CNAME .',
                   'example.net CNAME .', '*.example.net CNAME .'}
    hosts_all = {'example.com CNAME .', 'x.example.com CNAME .',
                 'y.example.com CNAME .', 'example.org CNAME .',
                 'example.net CNAME .', '*.example.net CNAME .'}
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
            hostblocker.writer.bind.write_hosts_list(list(self.hosts.keys()), file)
            file.seek(0)
            lines = self.read_entries(file)
        self.assertEqual(len(lines), 6)
        self.assertEqual(set(map(str.strip, lines)), self.hosts_all)

    def test_write_hosts_list_error(self):
        with tempfile.TemporaryFile('r') as file:
            with self.assertLogs(level=logging.ERROR):
                self.assertTrue(
                    hostblocker.writer.bind.write_hosts_list(list(self.hosts.keys()), file) > 0
                )

    def test_write_header(self):
        with tempfile.TemporaryFile('r+') as file:
            hostblocker.writer.bind.write_header(self.dir_path + '/resources/header.txt', file)
            file.seek(0)
            lines = self.read_entries(file)
        self.assertEqual(len(lines), 3)
        self.assertEqual(list(map(str.strip, lines)), self.header)

    def test_write_header_error(self):
        with tempfile.TemporaryFile('w') as file:
            with self.assertLogs(level=logging.ERROR):
                self.assertTrue(
                    hostblocker.writer.bind.write_header('none', file) > 0
                )
        with tempfile.TemporaryFile('r') as file:
            with self.assertLogs(level=logging.ERROR):
                self.assertTrue(
                    hostblocker.writer.bind.write_header(self.dir_path + '/resources/header.txt',
                                                         file)
                    > 0
                )

    def test_write(self):
        with tempfile.NamedTemporaryFile('r+') as file:
            hostblocker.writer.bind.write(self.hosts,
                                          self.dir_path + '/resources/header.txt',
                                          file.name,
                                          2)
            lines = self.read_entries(file)
        self.assertEqual(len(lines), 12)
        self.assertEqual(lines[0], '; ' + hostblocker.writer.APP_HEADER)
        self.assertTrue(lines[1].startswith('; ### BEGIN'))
        self.assertEqual(list(map(str.strip, lines[2:5])), self.header)
        self.assertTrue(lines[5].startswith('; ### END'))
        self.assertTrue(lines[6].startswith('; ### BEGIN'))
        self.assertEqual(set(map(str.strip, lines[7:11])), self.hosts_score)
        self.assertTrue(lines[11].startswith('; ### END'))

    def test_write_error(self):
        with self.assertLogs(level=logging.ERROR):
            self.assertTrue(
                hostblocker.writer.bind.write(dict({}),
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
