import sys
import urllib.request
from mockito import when, mock, verify, unstub  # type: ignore[import-untyped]
from mockito.matchers import ANY, captor  # type: ignore[import-untyped]

import hostblocker.reader.fetch


def test_get_lines() -> None:
    url = 'https://example.com/file.txt'
    when(hostblocker.reader.cache).read(ANY, ANY).thenReturn(None)
    when(hostblocker.reader.cache).write(ANY, ANY).thenReturn(None)
    response = mock()
    when(response).readlines().thenReturn([b'abc\n', b'xyz\n'])
    when(urllib.request).urlopen(ANY, timeout=ANY).thenReturn(response)

    lines = hostblocker.reader.fetch.get_lines(url, sys.maxsize)

    assert lines == [b'abc\n', b'xyz\n']
    verify(hostblocker.reader.cache).read(url, sys.maxsize)
    verify(hostblocker.reader.cache).write(url, [b'abc\n', b'xyz\n'])
    request = captor()
    verify(urllib.request).urlopen(request, timeout=10)
    assert request.value.get_full_url() == url

    unstub(hostblocker.reader.cache)
    unstub(urllib.request)


def test_get_lines_error() -> None:
    when(hostblocker.reader.cache).read(ANY, ANY).thenReturn(None)

    lines = hostblocker.reader.fetch.get_lines('https://example.com/file.txt', sys.maxsize)

    assert lines == []

    unstub(hostblocker.reader.cache)
