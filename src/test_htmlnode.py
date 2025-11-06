import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_none(self):
        node = HTMLNode(tag="a", value="Click me", props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode(
            tag="a", value="Click me", props={"href": "https://www.google.com"}
        )
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            tag="a",
            value="Click me",
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        result = node.props_to_html()
        # Should have a leading space and both attributes
        self.assertTrue(result.startswith(" "))
        self.assertIn('href="https://www.google.com"', result)
        self.assertIn('target="_blank"', result)

    def test_props_to_html_empty_dict(self):
        node = HTMLNode(tag="p", value="Hello", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_to_html_raises_error(self):
        node = HTMLNode(tag="p", value="Hello")
        with self.assertRaises(NotImplementedError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
