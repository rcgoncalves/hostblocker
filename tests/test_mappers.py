import unittest

import datasrc.mappers


class TestMappers(unittest.TestCase):
    """
    Test class for mappers.
    """
    def test_remove_comments(self):
        self.assertEqual(
            datasrc.mappers.remove_comments(
                '#               MalwareDomainList.com Hosts List           #'
            ),
            ''
        )
        self.assertEqual(
            datasrc.mappers.remove_comments('#'),
            ''
        )
        self.assertEqual(
            datasrc.mappers.remove_comments('12345 67890 # List'),
            '12345 67890 '
        )
        self.assertEqual(
            datasrc.mappers.remove_comments('1qaz2wsx '),
            '1qaz2wsx '
        )

    def test_remove_comments_ab(self):
        self.assertEqual(
            datasrc.mappers.remove_adblock_comments('! uBlock Origin -- Resource-abuse filters'),
            ''
        )
        self.assertEqual(
            datasrc.mappers.remove_adblock_comments('!'),
            ''
        )
        self.assertEqual(
            datasrc.mappers.remove_adblock_comments('1qaz2wsx'),
            '1qaz2wsx'
        )

    def test_remove_ip_local(self):
        self.assertEqual(
            datasrc.mappers.remove_ip_local('127.0.0.1  localhost'),
            '  localhost'
        )
        self.assertEqual(
            datasrc.mappers.remove_ip_local('127.0.0.1 domain.com'),
            ' domain.com'
        )
        self.assertEqual(
            datasrc.mappers.remove_ip_local('127.0.0.1domain.com'),
            'domain.com'
        )
        self.assertEqual(
            datasrc.mappers.remove_ip_local('127.0.0.0 domain.com'),
            '127.0.0.0 domain.com'
        )

    def test_remove_ip_zero(self):
        self.assertEqual(
            datasrc.mappers.remove_ip_zero('0.0.0.0  localhost'),
            '  localhost'
        )
        self.assertEqual(
            datasrc.mappers.remove_ip_zero('0.0.0.0 domain.com'),
            ' domain.com'
        )
        self.assertEqual(
            datasrc.mappers.remove_ip_zero('0.0.0.0domain.com'),
            'domain.com'
        )
        self.assertEqual(
            datasrc.mappers.remove_ip_zero('0.0.0.1 domain.com'),
            '0.0.0.1 domain.com'
        )

    def test_remove_dot(self):
        self.assertEqual(
            datasrc.mappers.remove_dot('.domain.com'),
            'domain.com'
        )
        self.assertEqual(
            datasrc.mappers.remove_dot('domain.com'),
            'domain.com'
        )

    def test_remove_adblock_text(self):
        self.assertEqual(
            datasrc.mappers.remove_adblock_text('||domain.com^$scripts'),
            ''
        )
        self.assertEqual(
            datasrc.mappers.remove_adblock_text('||domain.com^$third-party'),
            'domain.com'
        )
        self.assertEqual(
            datasrc.mappers.remove_adblock_text('||domain.com^$popup'),
            'domain.com'
        )
        self.assertEqual(
            datasrc.mappers.remove_adblock_text('||domain.com^$document'),
            'domain.com'
        )
        self.assertEqual(
            datasrc.mappers.remove_adblock_text('||domain.com^$popup,third-party'),
            'domain.com'
        )
        self.assertEqual(
            datasrc.mappers.remove_adblock_text('||domain.com^$document,popup'),
            'domain.com'
        )
        self.assertEqual(
            datasrc.mappers.remove_adblock_text('/coinhive.min.js'),
            ''
        )
        self.assertEqual(
            datasrc.mappers.remove_adblock_text('||domain.com^'),
            'domain.com'
        )

    def test_remove_xml_tags(self):
        self.assertEqual(
            datasrc.mappers.remove_xml_tags(' <xml>domain.com</xml> '),
            ' domain.com '
        )
        self.assertEqual(
            datasrc.mappers.remove_xml_tags(' domain.com</xml> '),
            ' domain.com '
        )
        self.assertEqual(
            datasrc.mappers.remove_xml_tags(' domain.com '),
            ' domain.com '
        )

    def test_trim(self):
        self.assertEqual(
            datasrc.mappers.trim('  domain.com  '),
            'domain.com'
        )
        self.assertEqual(
            datasrc.mappers.trim('domain.com\n\r'),
            'domain.com'
        )
        self.assertEqual(
            datasrc.mappers.trim('\t  domain.com  '),
            'domain.com'
        )


if __name__ == '__main__':
    unittest.main()
