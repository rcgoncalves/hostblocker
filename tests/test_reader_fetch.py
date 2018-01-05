import logging
import sys
import unittest

import hostblocker.reader.fetch


URL = 'http://example.com/file.txt'


class TestFetch(unittest.TestCase):
    """
    Test class for fetch functions.
    """
    def test_get_lines_error(self):
        with self.assertLogs(level=logging.ERROR):
            lines = hostblocker.reader.fetch.get_lines(URL + 'x', sys.maxsize)
            self.assertEqual(lines, [])

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.CRITICAL)


if __name__ == '__main__':
    unittest.main()
