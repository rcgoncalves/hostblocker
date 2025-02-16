#!/usr/local/bin/python3

import argparse
import importlib
import logging
import sys
import yaml
import importlib.metadata

import hostblocker.builder


def init_logging(debug: str) -> logging.Logger:
    """
    Initializes the logging framework.
    Defines the format and levels for file and stderr outputs.

    :param debug: enable debug output.
    :return: the root logger.
    """
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')
    root = logging.getLogger()
    root.handlers[0].setLevel(logging.ERROR)
    if debug:
        ch = logging.FileHandler(debug, 'w')
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s')
        ch.setFormatter(formatter)
        root.addHandler(ch)
    return root


def init_args() -> argparse.Namespace:
    """
    Parses the command line options.

    :return: the command line options parsed.
    """
    parser = argparse.ArgumentParser(description='Build an hosts file to block domains')
    parser.add_argument('-s', '--source',
                        help='YAML sources list',
                        required=True, dest='config')
    parser.add_argument('-o', '--output',
                        help='Output file',
                        required=False, default='hosts', dest='out')
    parser.add_argument('-f', '--format',
                        help='Specifies the output format (hosts, dnsmasq, bind or unbound)',
                        required=False, default='hosts', dest='format')
    parser.add_argument('-p', '--header',
                        help='Header for the output file',
                        required=False, default='', dest='header')
    parser.add_argument('-w', '--whitelist',
                        help='List of domains to not block',
                        required=False, default='', dest='whitelist')
    parser.add_argument('-b', '--blacklist',
                        help='Additional domains to block',
                        required=False, default='', dest='blacklist')
    parser.add_argument('-t', '--threshold', type=int,
                        help='Score threshold to block domains',
                        required=False, default=0, dest='score')
    parser.add_argument('-c', '--cache', type=int,
                        help='Number of hours to cache file',
                        required=False, default=60, dest='cache')
    parser.add_argument('-d', '--debug',
                        help=argparse.SUPPRESS,  # Enable debug output with the given file
                        required=False, default='', dest='debug')
    parser.add_argument('-v', '--version',
                        help='Prints version and exits',
                        action='version', version=importlib.metadata.version('hostblocker'))
    return parser.parse_args()


def main() -> int:
    """
    Main method.

    :return:
    0 in case of success.
    2 if the options specified are not valid
    3 if there was an error reading the YAML config file.
    4 if the output format is invalid
    """
    args = init_args()
    init_logging(args.debug)
    logging.debug('config file: %s', args.config)
    logging.debug('output file: %s', args.out)
    logging.debug('format: %s', args.format)
    logging.debug('header file: %s', args.header)
    logging.debug('whitelist file: %s', args.whitelist)
    logging.debug('blacklist file: %s', args.blacklist)
    logging.debug('minimum score: %d', args.score)
    logging.debug('max cache: %d', args.cache)
    try:
        with open(args.config, encoding='utf-8') as stream:
            config = yaml.safe_load(stream)
    except (FileNotFoundError, yaml.YAMLError):
        logging.exception('error reading sources YAML')
        sys.exit(3)
    hosts = hostblocker.builder.build_from_sources(config, args.cache)
    hosts = hostblocker.builder.apply_blacklist(hosts, args.blacklist, args.score)
    hosts = hostblocker.builder.apply_whitelist(hosts, args.whitelist, args.score)
    hosts_list = hostblocker.builder.filter_score(hosts, args.score)
    try:
        mod = importlib.import_module('hostblocker.writer.' + args.format)
        mod.write(hosts_list, args.header, args.out)
    except ModuleNotFoundError:
        logging.exception('invalid output format: %s', args.format)
        sys.exit(4)
    return 0


if __name__ == '__main__':
    main()
