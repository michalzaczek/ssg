import unittest

from textnode import TextNode, TextType, split_nodes_delimiter, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_false_different_text(self):
        n1 = TextNode("hello", TextType.TEXT)
        n2 = TextNode("world", TextType.TEXT)
        self.assertNotEqual(n1, n2)

    def test_eq_false_different_type(self):
        n1 = TextNode("hello", TextType.BOLD)
        n2 = TextNode("hello", TextType.TEXT)
        self.assertNotEqual(n1, n2)

    # test functions

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.props, None)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.props, None)
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_code(self):
        node = TextNode("code snippet", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "code snippet")
        self.assertEqual(html_node.props, None)
        self.assertEqual(html_node.to_html(), "<code>code snippet</code>")

    def test_link(self):
        node = TextNode("Click me", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props, {"href": "https://www.example.com"})
        self.assertEqual(
            html_node.to_html(), '<a href="https://www.example.com">Click me</a>'
        )

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "https://example.com/image.png", "alt": "Alt text"}
        )
        self.assertEqual(
            html_node.to_html(),
            '<img src="https://example.com/image.png" alt="Alt text" />',
        )

    # split_nodes_delimiter
    def test_split_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.CODE)
        compare_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        compare_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_bold_with_asterisk(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        compare_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_italic_with_underscore(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        compare_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_multiple_delimiters(self):
        node = TextNode("This has **bold** and `code` and _italic_", TextType.TEXT)
        # Test bold first
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        compare_nodes = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and `code` and _italic_", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_delimiter_at_start(self):
        node = TextNode("**bold** at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        compare_nodes = [
            TextNode("", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" at the start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_delimiter_at_end(self):
        node = TextNode("text with **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        compare_nodes = [
            TextNode("text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_only_delimiters(self):
        node = TextNode("**bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        compare_nodes = [
            TextNode("", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_no_delimiters(self):
        node = TextNode("This has no delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        compare_nodes = [
            TextNode("This has no delimiters", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        compare_nodes = [
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_multiple_occurrences(self):
        node = TextNode("**first** and **second** bold words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        compare_nodes = [
            TextNode("", TextType.TEXT),
            TextNode("first", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.BOLD),
            TextNode(" bold words", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_multiple_nodes(self):
        node1 = TextNode("First **bold** text", TextType.TEXT)
        node2 = TextNode("Second `code` text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        compare_nodes = [
            TextNode("First ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
            TextNode("Second `code` text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_code_backtick_multiple(self):
        node = TextNode("`first` code and `second` code", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        compare_nodes = [
            TextNode("", TextType.TEXT),
            TextNode("first", TextType.CODE),
            TextNode(" code and ", TextType.TEXT),
            TextNode("second", TextType.CODE),
            TextNode(" code", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_italic_multiple_underscores(self):
        node = TextNode("_first_ italic and _second_ italic", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        compare_nodes = [
            TextNode("", TextType.TEXT),
            TextNode("first", TextType.ITALIC),
            TextNode(" italic and ", TextType.TEXT),
            TextNode("second", TextType.ITALIC),
            TextNode(" italic", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_with_whitespace_around_delimiters(self):
        node = TextNode("Text with ** bold ** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        compare_nodes = [
            TextNode("Text with ", TextType.TEXT),
            TextNode(" bold ", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_single_character_delimiter(self):
        node = TextNode("Text with |delimiter| word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "|", TextType.BOLD)
        compare_nodes = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("delimiter", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_multi_character_delimiter(self):
        node = TextNode("Text with <<<delimiter>>> word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "<<<", TextType.BOLD)
        compare_nodes = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("delimiter>>> word", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_adjacent_delimiters(self):
        node = TextNode("Text **bold1****bold2** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        compare_nodes = [
            TextNode("Text ", TextType.TEXT),
            TextNode("bold1", TextType.BOLD),
            TextNode("", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_delimiter_in_middle_of_word(self):
        node = TextNode("pre**mid**post", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        compare_nodes = [
            TextNode("pre", TextType.TEXT),
            TextNode("mid", TextType.BOLD),
            TextNode("post", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, compare_nodes)


if __name__ == "__main__":
    unittest.main()
