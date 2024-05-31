import logging
import os
import tempfile
import unittest

import hostblocker.writer.bind

from typing import Self, IO, ClassVar


class TestWriteBind(unittest.TestCase):
    """
    Test class for writing bind.
    """
    dir_path: ClassVar[str] = os.path.dirname(os.path.abspath(__file__))
    hosts: ClassVar[list[str]] = ['example.com', 'x.example.com', 'y.example.com', 'example.net',
                                  'x.example.net', 'y.example.net', 'z.example.net', 'example.org']
    hosts_write: ClassVar[list[str]] = ['example.com CNAME .', 'x.example.com CNAME .',
                                        'y.example.com CNAME .', 'example.net CNAME .',
                                        '*.example.net CNAME .', 'example.org CNAME .']
    header: ClassVar[list[str]] = ['127.0.0.1 localhost localhost.local', '1.2.3.4   example.com',
                                   '1.2.3.4   app.example.com']

    @staticmethod
    def read_entries(file: IO[str]) -> list[str]:
        """
        Returns the lines of a text file.

        :param file: the file.
        :return: the lines of the file.
        """
        return file.readlines()

    def test_write_hosts_list(self: Self) -> None:
        with tempfile.TemporaryFile('r+', encoding='utf-8') as file:
            hostblocker.writer.bind.write_hosts_list(self.hosts, file)
            file.seek(0)
            lines = self.read_entries(file)
        self.assertEqual(len(lines), 6)
        self.assertEqual(list(map(str.strip, lines)), self.hosts_write)

    def test_write_hosts_list_error(self: Self) -> None:
        with tempfile.TemporaryFile('r', encoding='utf-8') as file, self.assertLogs(level=logging.ERROR):
            self.assertTrue(hostblocker.writer.bind.write_hosts_list(self.hosts, file) > 0)

    def test_write_header(self: Self) -> None:
        with tempfile.TemporaryFile('r+', encoding='utf-8') as file:
            hostblocker.writer.bind.write_header(self.dir_path + '/resources/header.txt', file)
            file.seek(0)
            lines = self.read_entries(file)
        self.assertEqual(len(lines), 3)
        self.assertEqual(list(map(str.strip, lines)), self.header)

    def test_write_header_error(self: Self) -> None:
        with tempfile.TemporaryFile('w', encoding='utf-8') as file, self.assertLogs(level=logging.ERROR):
            self.assertTrue(hostblocker.writer.bind.write_header('none', file) > 0)
        with tempfile.TemporaryFile('r', encoding='utf-8') as file, self.assertLogs(level=logging.ERROR):
            self.assertTrue(hostblocker.writer.bind.write_header(self.dir_path + '/resources/header.txt', file) > 0)

    def test_write(self: Self) -> None:
        with tempfile.NamedTemporaryFile('r+', encoding='utf-8') as file:
            hostblocker.writer.bind.write(self.hosts, self.dir_path + '/resources/header.txt', file.name)
            lines = self.read_entries(file)
        self.assertEqual(len(lines), 14)
        self.assertEqual(lines[0], '; ' + hostblocker.writer.APP_HEADER)
        self.assertTrue(lines[1].startswith('; ### BEGIN'))
        self.assertEqual(list(map(str.strip, lines[2:5])), self.header)
        self.assertTrue(lines[5].startswith('; ### END'))
        self.assertTrue(lines[6].startswith('; ### BEGIN'))
        self.assertEqual(list(map(str.strip, lines[7:13])), self.hosts_write)
        self.assertTrue(lines[13].startswith('; ### END'))

    def test_write_error(self: Self) -> None:
        with self.assertLogs(level=logging.ERROR):
            self.assertTrue(
                hostblocker.writer.bind.write([],
                                              self.dir_path + '/resources/header.txt',
                                              '/tmp/invalid/output/path/file.txt')  # noqa: S108
                > 0
            )

    @classmethod
    def set_up_class(cls: type[Self]) -> None:
        logging.basicConfig(level=logging.CRITICAL)


if __name__ == '__main__':
    unittest.main()
