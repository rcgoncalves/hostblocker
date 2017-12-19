import logging
import unittest

import hostblocker.functions.filters


class TestFilters(unittest.TestCase):
    """
    Test class for filters.
    """
    def test_is_not_blank(self):
        self.assertFalse(
            hostblocker.functions.filters.is_not_blank('')
        )
        self.assertFalse(
            hostblocker.functions.filters.is_not_blank(' ')
        )
        self.assertTrue(
            hostblocker.functions.filters.is_not_blank(' example.com')
        )

    def test_is_not_2nd_level_domain(self):
        self.assertFalse(
            hostblocker.functions.filters.is_not_2nd_level_domain('example.com')
        )
        self.assertTrue(
            hostblocker.functions.filters.is_not_2nd_level_domain('sub.example.com')
        )

    def test_is_not_top_level_domain(self):
        self.assertTrue(
            hostblocker.functions.filters.is_not_top_level_domain('example.com')
        )
        self.assertFalse(
            hostblocker.functions.filters.is_not_top_level_domain('com')
        )
        self.assertFalse(
            hostblocker.functions.filters.is_not_top_level_domain('localhost')
        )

    def test_is_valid_domain(self):
        self.assertTrue(
            hostblocker.functions.filters.is_valid_domain('example.com')
        )
        self.assertFalse(
            hostblocker.functions.filters.is_valid_domain('example.com.')
        )
        self.assertFalse(
            hostblocker.functions.filters.is_valid_domain('.example.com')
        )
        self.assertFalse(
            hostblocker.functions.filters.is_valid_domain('-example.com')
        )
        self.assertFalse(
            hostblocker.functions.filters.is_valid_domain(
                '1234567890123456789012345678901234567890123456789012345678901234.com'
            )
        )
        self.assertFalse(
            hostblocker.functions.filters.is_valid_domain(
                '1234567890123456789012345678901234567890123456789012345678901234.'
                '1234567890123456789012345678901234567890123456789012345678901234.'
                '1234567890123456789012345678901234567890123456789012345678901234.'
                '1234567890123456789012345678901234567890123456789012345678901234.com'
            )
        )

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.CRITICAL)


if __name__ == '__main__':
    unittest.main()
