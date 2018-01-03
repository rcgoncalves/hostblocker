#!/usr/local/bin/python3

import argparse
import importlib
import logging
import yaml

import hostblocker.builder


def init_logging(debug: str) -> logging.Logger:
    """
    Initializes the logging framework.
    Defines the format and levels for file and stderr outputs.

    :param debug: enable debug output.
    :return: the root logger.
    """
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')
    root = logging.getLogger()
    root.handlers[0].setLevel(logging.ERROR)
    if debug:
        ch = logging.FileHandler(debug, 'w')
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s')
        ch.setFormatter(formatter)
        root.addHandler(ch)
    return root


def init_args():
    """
    Parses the command line options.

    :return: the command line options parsed.
    """
    parser = argparse.ArgumentParser(description='Build an hosts file to block domains')
    parser.add_argument('-s', '--source',
                        help='YAML sources list',
                        required=False, default='config/sources.yml', dest='config')
    parser.add_argument('-o', '--output',
                        help='Output file',
                        required=False, default='hosts', dest='out')
    parser.add_argument('-f', '--format',
                        help='Specifies the output format (hosts, dnsmasq or bind)',
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
                        required=False, default=4, dest='score')
    parser.add_argument('-c', '--cache', type=int,
                        help='Number of hours to cache file',
                        required=False, default=60, dest='cache')
    parser.add_argument('-d', '--debug',
                        help=argparse.SUPPRESS,  # Enable debug output with the given file
                        required=False, default='', dest='debug')
    return parser.parse_args()


def main() -> int:
    """
    Main method.

    :return:
    0 in case of success.
    1 if there was an error reading the YAML config file.
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
    config = None
    with open(args.config, 'r') as stream:
        try:
            config = yaml.load(stream)
        except yaml.YAMLError:
            logging.exception('error reading sources YAML')
            exit(1)
    hosts = hostblocker.builder.build_from_sources(config, args.cache)
    hosts = hostblocker.builder.apply_blacklist(hosts, args.blacklist, args.score)
    hosts = hostblocker.builder.apply_whitelist(hosts, args.whitelist, args.score)
    try:
        mod = importlib.import_module('hostblocker.writer.' + args.format)
        mod.write(hosts, args.header, args.out, args.score)
    except ModuleNotFoundError:
        logging.error('invalid output format: %s', args.format)
        exit(2)
    return 0


if __name__ == '__main__':
    main()
