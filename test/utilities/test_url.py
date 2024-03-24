import unittest
from src.utilities.url import is_valid_url


class TestURLUtility(unittest.TestCase):
    def test_valid_urls(self):
        self.assertTrue(is_valid_url("https://google.com"))
        self.assertTrue(is_valid_url("https://google.com/"))
        self.assertTrue(is_valid_url("https://google.com/maps"))
        self.assertTrue(is_valid_url("https://tahsin.us"))
        self.assertTrue(is_valid_url("https://www.tahsin.us"))
        self.assertTrue(is_valid_url("https://something.tahsin.us"))

    def test_invalid_urls(self):
        self.assertFalse(is_valid_url("google.com"))
        self.assertFalse(is_valid_url("google"))
        self.assertFalse(is_valid_url("google."))
        self.assertFalse(is_valid_url("tahsin.us"))


if __name__ == '__main__':
    unittest.main()
