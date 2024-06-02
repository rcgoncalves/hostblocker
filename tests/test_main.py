import logging
import os
import pytest
import sys
from typing import Final

import hostblocker.main


DEBUG_LOG: Final[str] = 'debug.log'
DIR_PATH: Final[str] = os.path.dirname(os.path.abspath(__file__))


def test_init_args_defaults() -> None:
    sys.argv = ['hostblocker', '-s', 'config/sources.yml']
    args = hostblocker.main.init_args()
    assert args.config == 'config/sources.yml'
    assert args.out == 'hosts'
    assert args.format == 'hosts'
    assert not args.header
    assert not args.whitelist
    assert not args.blacklist
    assert args.score == 0
    assert args.cache == 60
    assert not args.debug


def test_init_args_all_short() -> None:
    sys.argv = ['hostblocker',
                '-s', 'sources.yml',
                '-o', 'out',
                '-f', 'format',
                '-p', 'header',
                '-w', 'whitelist',
                '-b', 'blacklist',
                '-t', '1',
                '-c', '1',
                '-d', 'debug.log']
    args = hostblocker.main.init_args()
    assert args.config == 'sources.yml'
    assert args.out == 'out'
    assert args.format == 'format'
    assert args.header == 'header'
    assert args.whitelist == 'whitelist'
    assert args.blacklist == 'blacklist'
    assert args.score == 1
    assert args.cache == 1
    assert args.debug == 'debug.log'


def test_init_args_all_long() -> None:
    sys.argv = ['hostblocker',
                '--source', 'sources.yml',
                '--output', 'out',
                '--format', 'format',
                '--header', 'header',
                '--whitelist', 'whitelist',
                '--blacklist', 'blacklist',
                '--threshold', '1',
                '--cache', '1',
                '--debug', 'debug.log']
    args = hostblocker.main.init_args()
    assert args.config == 'sources.yml'
    assert args.out == 'out'
    assert args.format == 'format'
    assert args.header == 'header'
    assert args.whitelist == 'whitelist'
    assert args.blacklist == 'blacklist'
    assert args.score == 1
    assert args.cache == 1
    assert args.debug == 'debug.log'


def test_init_logging() -> None:
    root_logger = hostblocker.main.init_logging('')
    assert len(root_logger.handlers) > 0
    assert root_logger.handlers[0].level == logging.ERROR


def test_init_logging_debug() -> None:
    root_logger = hostblocker.main.init_logging(DEBUG_LOG)
    assert len(root_logger.handlers) > 1
    assert root_logger.handlers[0].level == logging.ERROR
    assert root_logger.handlers[-1].level == logging.DEBUG


def test_main_no_sources() -> None:
    sys.argv = ['hostblocker']
    with pytest.raises(SystemExit) as e:
        hostblocker.main.main()
    assert e.type is SystemExit
    assert e.value.code == 2


def test_main_missing_option_value() -> None:
    sys.argv = ['hostblocker', '-s', f'{DIR_PATH}/resources/sources.yml', '-b']
    with pytest.raises(SystemExit) as e:
        hostblocker.main.main()
    assert e.type is SystemExit
    assert e.value.code == 2


def test_main_invalid_yaml() -> None:
    sys.argv = ['hostblocker', '-s', '/invalid.yml']
    with pytest.raises(SystemExit) as e:
        hostblocker.main.main()
    assert e.type is SystemExit
    assert e.value.code == 3


def test_main_invalid_format() -> None:
    sys.argv = ['hostblocker', '-s', f'{DIR_PATH}/resources/sources.yml', '-f', 'invalid']
    with pytest.raises(SystemExit) as e:
        hostblocker.main.main()
    assert e.type is SystemExit
    assert e.value.code == 4


def test_main() -> None:
    sys.argv = ['hostblocker', '-s', f'{DIR_PATH}/resources/sources.yml']
    assert hostblocker.main.main() == 0
