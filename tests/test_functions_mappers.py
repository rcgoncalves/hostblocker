import unittest

import hostblocker.functions.mappers

from typing import Self


class TestMappers(unittest.TestCase):
    """
    Test class for mappers.
    """
    def test_remove_comments(self: Self) -> None:
        self.assertEqual(
            hostblocker.functions.mappers.remove_comments(
                '#               MalwareDomainList.com Hosts List           #'
            ),
            ''
        )
        self.assertEqual(hostblocker.functions.mappers.remove_comments('#'), '')
        self.assertEqual(hostblocker.functions.mappers.remove_comments('12345 67890 # List'), '12345 67890 ')
        self.assertEqual(hostblocker.functions.mappers.remove_comments('1qaz2wsx '), '1qaz2wsx ')

    def test_remove_comments_ab(self: Self) -> None:
        self.assertEqual(
            hostblocker.functions.mappers.remove_adblock_comments('! uBlock Origin -- Resource-abuse filters'),
            ''
        )
        self.assertEqual(hostblocker.functions.mappers.remove_adblock_comments('!'), '')
        self.assertEqual(hostblocker.functions.mappers.remove_adblock_comments('1qaz2wsx'), '1qaz2wsx')

    def test_remove_ip_local(self: Self) -> None:
        self.assertEqual(hostblocker.functions.mappers.remove_ip_local('127.0.0.1  localhost'), '  localhost')
        self.assertEqual(hostblocker.functions.mappers.remove_ip_local('127.0.0.1 example.com'), ' example.com')
        self.assertEqual(hostblocker.functions.mappers.remove_ip_local('127.0.0.1example.com'), 'example.com')
        self.assertEqual(
            hostblocker.functions.mappers.remove_ip_local('127.0.0.0 example.com'),
            '127.0.0.0 example.com'
        )

    def test_remove_ip_zero(self: Self) -> None:
        self.assertEqual(hostblocker.functions.mappers.remove_ip_zero('0.0.0.0  localhost'), '  localhost')
        self.assertEqual(hostblocker.functions.mappers.remove_ip_zero('0.0.0.0 example.com'), ' example.com')
        self.assertEqual(hostblocker.functions.mappers.remove_ip_zero('0.0.0.0example.com'), 'example.com')
        self.assertEqual(hostblocker.functions.mappers.remove_ip_zero('0.0.0.1 example.com'), '0.0.0.1 example.com')

    def test_remove_dot(self: Self) -> None:
        self.assertEqual(hostblocker.functions.mappers.remove_dot('.example.com'), 'example.com')
        self.assertEqual(hostblocker.functions.mappers.remove_dot('example.com'), 'example.com')

    def test_remove_adblock_text(self: Self) -> None:
        self.assertEqual(hostblocker.functions.mappers.remove_adblock_text('||example.com^$scripts'), '')
        self.assertEqual(hostblocker.functions.mappers.remove_adblock_text('||example.com^$third-party'), 'example.com')
        self.assertEqual(hostblocker.functions.mappers.remove_adblock_text('||example.com^$popup'), 'example.com')
        self.assertEqual(hostblocker.functions.mappers.remove_adblock_text('||example.com^$document'), 'example.com')
        self.assertEqual(
            hostblocker.functions.mappers.remove_adblock_text('||example.com^$popup,third-party'),
            'example.com'
        )
        self.assertEqual(
            hostblocker.functions.mappers.remove_adblock_text('||example.com^$document,popup'),
            'example.com'
        )
        self.assertEqual(hostblocker.functions.mappers.remove_adblock_text('/coinhive.min.js'), '')
        self.assertEqual(hostblocker.functions.mappers.remove_adblock_text('||example.com^'), 'example.com')

    def test_remove_xml_tags(self: Self) -> None:
        self.assertEqual(hostblocker.functions.mappers.remove_xml_tags(' <xml>example.com</xml> '), ' example.com ')
        self.assertEqual(hostblocker.functions.mappers.remove_xml_tags(' example.com</xml> '), ' example.com ')
        self.assertEqual(hostblocker.functions.mappers.remove_xml_tags(' example.com '), ' example.com ')

    def test_trim(self: Self) -> None:
        self.assertEqual(hostblocker.functions.mappers.trim('  example.com  '), 'example.com')
        self.assertEqual(hostblocker.functions.mappers.trim('example.com\n\r'), 'example.com')
        self.assertEqual(hostblocker.functions.mappers.trim('\t  example.com  '), 'example.com')


if __name__ == '__main__':
    unittest.main()
