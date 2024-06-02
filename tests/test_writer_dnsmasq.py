import os
import tempfile
from typing import Final

import hostblocker.writer.dnsmasq


dir_path: Final[str] = os.path.dirname(os.path.abspath(__file__))
hosts: Final[list[str]] = ['example.com', 'example.net', 'example.org']
hosts_write: Final[list[str]] = ['server=/example.com/', 'server=/example.net/', 'server=/example.org/']
header: Final[list[str]] = ['127.0.0.1 localhost localhost.local', '1.2.3.4   example.com', '1.2.3.4   app.example.com']


def test_write_hosts_list() -> None:
    with tempfile.TemporaryFile('r+', encoding='utf-8') as file:
        hostblocker.writer.dnsmasq.write_hosts_list(hosts, file)
        file.seek(0)
        lines = file.readlines()
    assert len(lines) == 3
    assert list(map(str.strip, lines)) == hosts_write


def test_write_hosts_list_error() -> None:
    with tempfile.TemporaryFile('r', encoding='utf-8') as file:
        assert hostblocker.writer.dnsmasq.write_hosts_list(hosts, file) > 0


def test_write_header() -> None:
    with tempfile.TemporaryFile('r+', encoding='utf-8') as file:
        hostblocker.writer.dnsmasq.write_header(dir_path + '/resources/header.txt', file)
        file.seek(0)
        lines = file.readlines()
    assert len(lines) == 3
    assert list(map(str.strip, lines)) == header


def test_write_header_error() -> None:
    with tempfile.TemporaryFile('w', encoding='utf-8') as file:
        assert hostblocker.writer.dnsmasq.write_header('none', file) > 0
    with tempfile.TemporaryFile('r', encoding='utf-8') as file:
        assert hostblocker.writer.dnsmasq.write_header(dir_path + '/resources/header.txt', file) > 0


def test_write() -> None:
    with tempfile.NamedTemporaryFile('r+', encoding='utf-8') as file:
        hostblocker.writer.dnsmasq.write(hosts, dir_path + '/resources/header.txt', file.name)
        lines = file.readlines()
    assert len(lines) == 11
    assert lines[0] == hostblocker.writer.APP_HEADER
    assert lines[1].startswith('### BEGIN')
    assert list(map(str.strip, lines[2:5])) == header
    assert lines[5].startswith('### END')
    assert lines[6].startswith('### BEGIN')
    assert list(map(str.strip, lines[7:10])) == hosts_write
    assert lines[10].startswith('### END')


def test_write_error() -> None:
    assert hostblocker.writer.dnsmasq.write([],
                                            dir_path + '/resources/header.txt',
                                            '/tmp/invalid/output/path/file.txt'  # noqa: S108
                                            ) > 0
