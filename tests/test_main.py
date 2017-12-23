import logging
import os
import sys
import unittest

import hostblocker.main

DEBUG_LOG = 'debug.log'


class TestMain(unittest.TestCase):
    """
    Test class for main.
    """
    def test_init_args_defaults(self):
        sys.argv = ['hostblocker']
        args = hostblocker.main.init_args()
        self.assertEqual(args.config, 'config/sources.yml')
        self.assertEqual(args.out, 'hosts')
        self.assertEqual(args.format, 'hosts')
        self.assertEqual(args.header, '')
        self.assertEqual(args.whitelist, '')
        self.assertEqual(args.blacklist, '')
        self.assertEqual(args.score, 4)
        self.assertEqual(args.cache, 60)
        self.assertEqual(args.debug, '')

    def test_init_args_all_short(self):
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
        self.assertEqual(args.config, 'sources.yml')
        self.assertEqual(args.out, 'out')
        self.assertEqual(args.format, 'format')
        self.assertEqual(args.header, 'header')
        self.assertEqual(args.whitelist, 'whitelist')
        self.assertEqual(args.blacklist, 'blacklist')
        self.assertEqual(args.score, 1)
        self.assertEqual(args.cache, 1)
        self.assertEqual(args.debug, 'debug.log')

    def test_init_args_all_long(self):
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
        self.assertEqual(args.config, 'sources.yml')
        self.assertEqual(args.out, 'out')
        self.assertEqual(args.format, 'format')
        self.assertEqual(args.header, 'header')
        self.assertEqual(args.whitelist, 'whitelist')
        self.assertEqual(args.blacklist, 'blacklist')
        self.assertEqual(args.score, 1)
        self.assertEqual(args.cache, 1)
        self.assertEqual(args.debug, 'debug.log')

    def test_init_logging(self):
        root_logger = hostblocker.main.init_logging('')
        self.assertTrue(len(root_logger.handlers) > 0)
        self.assertEqual(root_logger.handlers[0].level, logging.ERROR)

    def test_init_logging_debug(self):
        root_logger = hostblocker.main.init_logging(DEBUG_LOG)
        self.assertTrue(len(root_logger.handlers) > 1)
        self.assertEqual(root_logger.handlers[0].level, logging.ERROR)
        self.assertEqual(root_logger.handlers[1].level, logging.DEBUG)

    del_debug_log = False

    def setUp(self):
        if not os.path.exists(DEBUG_LOG):
            self.del_debug_log = True

    def tearDown(self):
        if self.del_debug_log and os.path.exists(DEBUG_LOG):
            os.remove(DEBUG_LOG)


if __name__ == '__main__':
    unittest.main()
