import datetime
import unittest
import pytz

from src.python.utilities.datetime import calculate_time


class TestBasic(unittest.TestCase):
    def test_should_work_for_today(self):
        result = calculate_time("10:00 pm", "Asia/Dhaka", 0, "relative")
        self.assertEqual(result, datetime.datetime.now(pytz.timezone("Asia/Dhaka")).replace(hour=22, minute=0, second=0, microsecond=0))

    def test_should_work_for_tomorrow(self):
        result = calculate_time("10:00 pm", "Asia/Dhaka", 1, "relative")
        self.assertEqual(result, datetime.datetime.now(pytz.timezone("Asia/Dhaka")).replace(hour=22, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1))

    def test_should_work_for_absolute_date(self):
        result = calculate_time("10:00 pm", "Asia/Dhaka", "23 Mar 2026", "absolute")
        self.assertEqual(result.date(), datetime.date(2026, 3, 23))
        self.assertEqual(str(result), "2026-03-23 22:00:00+06:00")

    def test_should_raise_error_for_invalid_time_format(self):
        with self.assertRaises(ValueError):
            calculate_time("invalid-date10:am", "Asia/Dhaka", 0, "relative")


if __name__ == '__main__':
    unittest.main()
