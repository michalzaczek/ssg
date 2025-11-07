import unittest

from htmlnode import HTMLNode, LeafNode


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

    # LeafNode tests

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")

    def test_leaf_to_html_value_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "This is a div")
        self.assertEqual(node.to_html(), "<div>This is a div</div>")


if __name__ == "__main__":
    unittest.main()
