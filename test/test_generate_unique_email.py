import unittest
from src.generate_unique_email import exec


class TestStringMethods(unittest.TestCase):
    def test_both_input(self):
        email = exec("tahsin", "carfax.com")

        self.assertEqual(email[-18:], "-tahsin@carfax.com")
        self.assertEqual(len(email), 28)

    def test_both_blank(self):
        email = exec("", "")

        self.assertEqual(email[-12:], "@maildrop.cc")
        self.assertEqual(len(email), 22)

    def test_just_domain(self):
        email = exec("", "carfax.com")

        self.assertEqual(email[-11:], "@carfax.com")
        self.assertEqual(len(email), 21)

    def test_just_suffix(self):
        email = exec("tahsin", "")

        self.assertEqual(email[-19:], "-tahsin@maildrop.cc")

        self.assertEqual(len(email), 29)


if __name__ == '__main__':
    unittest.main()
