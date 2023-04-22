import logging
import sys
import unittest

import hostblocker.reader.fetch

from typing import Self, Final


URL: Final[str] = 'http://example.com/file.txt'


class TestFetch(unittest.TestCase):
    """
    Test class for fetch functions.
    """
    def test_get_lines_error(self: Self) -> None:
        with self.assertLogs(level=logging.ERROR):
            lines = hostblocker.reader.fetch.get_lines(URL + 'x', sys.maxsize)
            assert lines == []

    @classmethod
    def set_up_class(cls: type[Self]) -> None:
        logging.basicConfig(level=logging.CRITICAL)


if __name__ == '__main__':
    unittest.main()
