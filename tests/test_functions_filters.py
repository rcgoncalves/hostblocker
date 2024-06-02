import pytest

import hostblocker.functions.filters


@pytest.mark.parametrize('line', [
    '',
    ' ',
    '  \t     ',
])
def test_is_not_blank_false(line: str) -> None:
    assert not hostblocker.functions.filters.is_not_blank(line)


@pytest.mark.parametrize('line', [
    'example.com',
    'sub.example.com',
])
def test_is_not_blank_true(line: str) -> None:
    assert hostblocker.functions.filters.is_not_blank(line)


@pytest.mark.parametrize('line', [
    'example.com',
    'x.zip',
    'a.dev',
])
def test_is_not_2nd_level_domain_false(line: str) -> None:
    assert not hostblocker.functions.filters.is_not_2nd_level_domain(line)


@pytest.mark.parametrize('line', [
    'sub.example.com',
    'sub1.sub2.x.zip',
    'a.b.c.d.e.f.dev',
])
def test_is_not_2nd_level_domain_true(line: str) -> None:
    assert hostblocker.functions.filters.is_not_2nd_level_domain(line)


@pytest.mark.parametrize('line', [
    'com',
    'localhost',
    'net',
    'org',
])
def test_is_not_top_level_domain_false(line: str) -> None:
    assert not hostblocker.functions.filters.is_not_top_level_domain(line)


@pytest.mark.parametrize('line', [
    'example.com',
    'sub.example.net',
    'a.b.c.d.example.org',
])
def test_is_not_top_level_domain_true(line: str) -> None:
    assert hostblocker.functions.filters.is_not_top_level_domain(line)


@pytest.mark.parametrize('line', [
    'example .com',
    'example.com.',
    '.example.com',
    '-example.com',
    '1234567890123456789012345678901234567890123456789012345678901234.com',
    '1234567890123456789012345678901234567890123456789012345678901234.'
    '1234567890123456789012345678901234567890123456789012345678901234.'
    '1234567890123456789012345678901234567890123456789012345678901234.'
    '1234567890123456789012345678901234567890123456789012345678901234.com'
])
def test_is_valid_domain_false(line: str) -> None:
    assert not hostblocker.functions.filters.is_valid_domain(line)


@pytest.mark.parametrize('line', [
    'example.com',
    'sub.example.zip',
    'a.b.c.d.example.workx',
])
def test_is_valid_domain_true(line: str) -> None:
    assert hostblocker.functions.filters.is_valid_domain(line)
