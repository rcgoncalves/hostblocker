import sys
from typing import Final

import hostblocker.reader.fetch


URL: Final[str] = 'https://example.com/file.txt'


def test_get_lines_error() -> None:
    lines = hostblocker.reader.fetch.get_lines(URL + 'x', sys.maxsize)
    assert lines == []
