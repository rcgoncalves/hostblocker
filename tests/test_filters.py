import logging
import unittest

import datasrc.filters


class TestFilters(unittest.TestCase):
    """
    Test class for filters.
    """
    def test_is_not_blank(self):
        self.assertFalse(
            datasrc.filters.is_not_blank('')
        )
        self.assertFalse(
            datasrc.filters.is_not_blank(' ')
        )
        self.assertTrue(
            datasrc.filters.is_not_blank(' domain.com')
        )

    def test_is_not_2nd_level_domain(self):
        self.assertFalse(
            datasrc.filters.is_not_2nd_level_domain('domain.com')
        )
        self.assertTrue(
            datasrc.filters.is_not_2nd_level_domain('sub.domain.com')
        )

    def test_is_not_top_level_domain(self):
        self.assertTrue(
            datasrc.filters.is_not_top_level_domain('domain.com')
        )
        self.assertFalse(
            datasrc.filters.is_not_top_level_domain('com')
        )
        self.assertFalse(
            datasrc.filters.is_not_top_level_domain('localhost')
        )

    def test_is_valid_domain(self):
        self.assertTrue(
            datasrc.filters.is_valid_domain('domain.com')
        )
        self.assertFalse(
            datasrc.filters.is_valid_domain('domain.com.')
        )
        self.assertFalse(
            datasrc.filters.is_valid_domain('.domain.com')
        )
        self.assertFalse(
            datasrc.filters.is_valid_domain('-domain.com')
        )
        self.assertFalse(
            datasrc.filters.is_valid_domain(
                '1234567890123456789012345678901234567890123456789012345678901234.com'
            )
        )
        self.assertFalse(
            datasrc.filters.is_valid_domain(
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
