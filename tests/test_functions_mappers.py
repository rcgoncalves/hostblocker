import pytest

import hostblocker.functions.mappers


@pytest.mark.parametrize(('line_in', 'line_out'), [
    ('#               MalwareDomainList.com Hosts List           #', ''),
    ('#', ''),
    ('12345 67890 # List', '12345 67890 '),
    ('1qaz2wsx ', '1qaz2wsx '),
])
def test_remove_comments(line_in: str, line_out: str) -> None:
    assert hostblocker.functions.mappers.remove_comments(line_in) == line_out


@pytest.mark.parametrize(('line_in', 'line_out'), [
    ('! uBlock Origin -- Resource-abuse filters', ''),
    ('!', ''),
    ('1qaz2wsx', '1qaz2wsx'),
])
def test_remove_comments_ab(line_in: str, line_out: str) -> None:
    assert hostblocker.functions.mappers.remove_adblock_comments(line_in) == line_out


@pytest.mark.parametrize(('line_in', 'line_out'), [
    ('127.0.0.1 localhost example.com', ' localhost example.com'),
    ('127.0.0.1  localhost', '  localhost'),
    ('127.0.0.1 example.com  ', ' example.com  '),
    ('127.0.0.1example.com', 'example.com'),
    ('127.0.0.0 example.com', '127.0.0.0 example.com'),
])
def test_remove_ip_local(line_in: str, line_out: str) -> None:
    assert hostblocker.functions.mappers.remove_ip_local(line_in) == line_out


@pytest.mark.parametrize(('line_in', 'line_out'), [
    ('0.0.0.0 localhost example.com', ' localhost example.com'),
    ('0.0.0.0  localhost', '  localhost'),
    ('0.0.0.0 example.com  ', ' example.com  '),
    ('0.0.0.0example.com', 'example.com'),
    ('0.0.0.1 example.com', '0.0.0.1 example.com'),
])
def test_remove_ip_zero(line_in: str, line_out: str) -> None:
    assert hostblocker.functions.mappers.remove_ip_zero(line_in) == line_out


@pytest.mark.parametrize(('line_in', 'line_out'), [
    (':: localhost example.com', ' localhost example.com'),
    ('::  localhost', '  localhost'),
    (':: example.com  ', ' example.com  '),
    ('::example.com', 'example.com'),
    (':1:1 example.com', ':1:1 example.com'),
])
def test_remove_ipv6_zero(line_in: str, line_out: str) -> None:
    assert hostblocker.functions.mappers.remove_ipv6_zero(line_in) == line_out


@pytest.mark.parametrize(('line_in', 'line_out'), [
    ('.example.com', 'example.com'),
    ('example.com', 'example.com'),
])
def test_remove_dot(line_in: str, line_out: str) -> None:
    assert hostblocker.functions.mappers.remove_dot(line_in) == line_out


@pytest.mark.parametrize(('line_in', 'line_out'), [
    ('||example.com^$scripts', ''),
    ('||example.com^$third-party', 'example.com'),
    ('||example.com^$popup', 'example.com'),
    ('||example.com^$document', 'example.com'),
    ('||example.com^$popup,third-party', 'example.com'),
    ('||example.com^$document,popup', 'example.com'),
    ('/coinhive.min.js', ''),
    ('||example.com^', 'example.com'),
])
def test_remove_adblock_text(line_in: str, line_out: str) -> None:
    assert hostblocker.functions.mappers.remove_adblock_text(line_in) == line_out


@pytest.mark.parametrize(('line_in', 'line_out'), [
    (' <xml>example.com</xml> ', ' example.com '),
    (' example.com</xml> ', ' example.com '),
    (' example.com ', ' example.com '),
])
def test_remove_xml_tags(line_in: str, line_out: str) -> None:
    assert hostblocker.functions.mappers.remove_xml_tags(line_in) == line_out


@pytest.mark.parametrize(('line_in', 'line_out'), [
    ('  example.com  ', 'example.com'),
    ('example.com\n\r', 'example.com'),
    ('\t  example.com  ', 'example.com'),
])
def test_trim(line_in: str, line_out: str) -> None:
    assert hostblocker.functions.mappers.trim(line_in) == line_out
