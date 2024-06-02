import os
import tempfile
from typing import Final

import hostblocker.writer.bind


DIR_PATH: Final[str] = os.path.dirname(os.path.abspath(__file__))
HOSTS: Final[list[str]] = ['example.com', 'x.example.com', 'y.example.com', 'example.net',
                           'x.example.net', 'y.example.net', 'z.example.net', 'example.org']
HOSTS_WRITE: Final[list[str]] = ['example.com CNAME .', 'x.example.com CNAME .',
                                 'y.example.com CNAME .', 'example.net CNAME .',
                                 '*.example.net CNAME .', 'example.org CNAME .']
HEADER: Final[list[str]] = ['127.0.0.1 localhost localhost.local', '1.2.3.4   example.com',
                            '1.2.3.4   app.example.com']


def test_write_hosts_list() -> None:
    with tempfile.TemporaryFile('r+', encoding='utf-8') as file:
        hostblocker.writer.bind.write_hosts_list(HOSTS, file)
        file.seek(0)
        lines = file.readlines()
    assert len(lines) == 6
    assert list(map(str.strip, lines)) == HOSTS_WRITE


def test_write_hosts_list_error() -> None:
    with tempfile.TemporaryFile('r', encoding='utf-8') as file:
        assert hostblocker.writer.bind.write_hosts_list(HOSTS, file) > 0


def test_write_header() -> None:
    with tempfile.TemporaryFile('r+', encoding='utf-8') as file:
        hostblocker.writer.bind.write_header(DIR_PATH + '/resources/header.txt', file)
        file.seek(0)
        lines = file.readlines()
    assert len(lines) == 3
    assert list(map(str.strip, lines)) == HEADER


def test_write_header_error() -> None:
    with tempfile.TemporaryFile('w', encoding='utf-8') as file:
        assert hostblocker.writer.bind.write_header('none', file) > 0
    with tempfile.TemporaryFile('r', encoding='utf-8') as file:
        assert hostblocker.writer.bind.write_header(DIR_PATH + '/resources/header.txt', file) > 0


def test_write() -> None:
    with tempfile.NamedTemporaryFile('r+', encoding='utf-8') as file:
        hostblocker.writer.bind.write(HOSTS, DIR_PATH + '/resources/header.txt', file.name)
        lines = file.readlines()
    assert len(lines) == 14
    assert lines[0] == '; ' + hostblocker.writer.APP_HEADER
    assert lines[1].startswith('; ### BEGIN')
    assert list(map(str.strip, lines[2:5])) == HEADER
    assert lines[5].startswith('; ### END')
    assert lines[6].startswith('; ### BEGIN')
    assert list(map(str.strip, lines[7:13])) == HOSTS_WRITE
    assert lines[13].startswith('; ### END')


def test_write_error() -> None:
    assert hostblocker.writer.bind.write([],
                                         DIR_PATH + '/resources/header.txt',
                                         '/tmp/invalid/output/path/file.txt'  # noqa: S108
                                         ) > 0
