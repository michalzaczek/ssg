import unittest

from utilities import extract_title


class TestHTMLNode(unittest.TestCase):
    def test_extract_title_simple(self):
        md = """
# title
- item1
- item2
"""
        self.assertEqual(extract_title(md), "title")

    def test_extract_title_simple_raise(self):
        md = """
## title
### title 2
text
        """
        with self.assertRaises(Exception):
            extract_title(md)
