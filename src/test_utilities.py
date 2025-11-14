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

    def test_extract_title_with_whitespace(self):
        md = "#   Hello World   "
        self.assertEqual(extract_title(md), "Hello World")

    def test_extract_title_no_space_after_hash(self):
        md = "#Title"
        self.assertEqual(extract_title(md), "Title")

    def test_extract_title_multiline(self):
        md = """Some text at the top
# The Main Title
## A subheading
More content here"""
        self.assertEqual(extract_title(md), "The Main Title")

    def test_extract_title_first_h1_wins(self):
        md = """# First Title
# Second Title"""
        self.assertEqual(extract_title(md), "First Title")

    def test_extract_title_empty_markdown(self):
        md = ""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_only_h2_and_h3(self):
        md = """## Heading 2
### Heading 3
#### Heading 4"""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_with_special_chars(self):
        md = "# Hello, World! This is a *test* with **bold** text"
        self.assertEqual(
            extract_title(md), "Hello, World! This is a *test* with **bold** text"
        )

    def test_extract_title_indented_h1(self):
        md = "   # Indented Title"
        self.assertEqual(extract_title(md), "Indented Title")
