import unittest
from src.utilities.text import get_env_key_value, get_env_vars_from_lines


class TestURLUtility(unittest.TestCase):
    def test_export_syntax(self):
        self.assertEqual(get_env_key_value("export Foo=Bar"), ("Foo", "Bar"))
        self.assertEqual(get_env_key_value("export Foo='Bar'"), ("Foo", "Bar"))
        self.assertEqual(get_env_key_value(
            "export Foo=\"Bar\""), ("Foo", "Bar"))
        self.assertEqual(get_env_key_value(
            "         export AWS_ACCESS_KEY_ID='anaccesskey'"), ("AWS_ACCESS_KEY_ID", "anaccesskey"))

    def test_key_value_syntax(self):
        self.assertEqual(get_env_key_value("Foo=Bar"), ("Foo", "Bar"))
        self.assertEqual(get_env_key_value("var1=value1"), ("var1", "value1"))
        self.assertEqual(get_env_key_value(
            "var1='value1!@#$'"), ("var1", "value1!@#$"))

    def test_fail_if_multiple_line_passed(self):
        line = """
        export var1='value1'
        export var2='value2'
"""
        with self.assertRaises(ValueError):
            get_env_key_value(line)

    def test_multiline_value(self):
        aws_config = """

        export AWS_ACCESS_KEY_ID="anaccesskey"
        export AWS_SECRET="secretkey"

"""
        vars = get_env_vars_from_lines(aws_config)
        self.assertEqual(vars["AWS_ACCESS_KEY_ID"], "anaccesskey")
        self.assertEqual(vars["AWS_SECRET"], "secretkey")
        self.assertEqual(len(vars.keys()), 2)


if __name__ == '__main__':
    unittest.main()
