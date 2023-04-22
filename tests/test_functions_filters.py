import logging
import unittest

import hostblocker.functions.filters

from typing import Self


class TestFilters(unittest.TestCase):
    """
    Test class for filters.
    """
    def test_is_not_blank(self: Self) -> None:
        self.assertFalse(hostblocker.functions.filters.is_not_blank(''))
        self.assertFalse(hostblocker.functions.filters.is_not_blank(' '))
        self.assertTrue(hostblocker.functions.filters.is_not_blank(' example.com'))

    def test_is_not_2nd_level_domain(self: Self) -> None:
        self.assertFalse(hostblocker.functions.filters.is_not_2nd_level_domain('example.com'))
        self.assertTrue(hostblocker.functions.filters.is_not_2nd_level_domain('sub.example.com'))

    def test_is_not_top_level_domain(self: Self) -> None:
        self.assertTrue(hostblocker.functions.filters.is_not_top_level_domain('example.com'))
        self.assertFalse(hostblocker.functions.filters.is_not_top_level_domain('com'))
        self.assertFalse(hostblocker.functions.filters.is_not_top_level_domain('localhost'))

    def test_is_valid_domain(self: Self) -> None:
        self.assertTrue(hostblocker.functions.filters.is_valid_domain('example.com'))
        self.assertFalse(hostblocker.functions.filters.is_valid_domain('example.com.'))
        self.assertFalse(hostblocker.functions.filters.is_valid_domain('.example.com'))
        self.assertFalse(hostblocker.functions.filters.is_valid_domain('-example.com'))
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
    def set_up_class(cls: type[Self]) -> None:
        logging.basicConfig(level=logging.CRITICAL)


if __name__ == '__main__':
    unittest.main()
