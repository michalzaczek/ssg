import unittest

from textnode import (
    TextNode,
    TextType,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
)


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
        node = TextNode("Text with <<<delimiter<<< word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "<<<", TextType.BOLD)
        compare_nodes = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("delimiter", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
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

    def test_split_non_text_node_passes_through(self):
        """Non-TEXT nodes should be added as-is without splitting"""
        bold_node = TextNode("**test**", TextType.BOLD)
        new_nodes = split_nodes_delimiter([bold_node], "**", TextType.BOLD)
        compare_nodes = [TextNode("**test**", TextType.BOLD)]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_mixed_node_types(self):
        """Only TEXT nodes should be split, others pass through"""
        text_node = TextNode("This is **bold** text", TextType.TEXT)
        bold_node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([text_node, bold_node], "**", TextType.BOLD)
        compare_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_unmatched_delimiter_raises_exception(self):
        """Unmatched delimiter should raise ValueError"""
        node = TextNode("This is **unmatched", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertIn("unmatched delimiter", str(context.exception).lower())

    def test_split_unmatched_delimiter_at_start(self):
        """Unmatched delimiter at start should raise exception"""
        node = TextNode("**unmatched text", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_unmatched_delimiter_multiple(self):
        """Multiple unmatched delimiters should raise exception"""
        node = TextNode("**first** **unmatched", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_unmatched_code_delimiter(self):
        """Unmatched code delimiter should raise exception"""
        node = TextNode("This has `unmatched code", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_unmatched_italic_delimiter(self):
        """Unmatched italic delimiter should raise exception"""
        node = TextNode("This has _unmatched italic", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "_", TextType.ITALIC)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    # Additional tests for extract_markdown_images
    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_markdown_images_empty_alt(self):
        text = "Image with ![empty alt]()"
        matches = extract_markdown_images(text)
        self.assertListEqual([("empty alt", "")], matches)

    def test_extract_markdown_images_no_images(self):
        text = "This is just plain text with no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_images_empty_text(self):
        text = ""
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_images_at_start(self):
        text = "![first](https://example.com/img1.png) and some text"
        matches = extract_markdown_images(text)
        self.assertListEqual([("first", "https://example.com/img1.png")], matches)

    def test_extract_markdown_images_at_end(self):
        text = "Some text and ![last](https://example.com/img2.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("last", "https://example.com/img2.png")], matches)

    def test_extract_markdown_images_with_spaces_in_alt(self):
        text = "![alt text with spaces](https://example.com/image.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("alt text with spaces", "https://example.com/image.png")], matches
        )

    def test_extract_markdown_images_http_url(self):
        text = "![image](http://example.com/image.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "http://example.com/image.png")], matches)

    def test_extract_markdown_images_relative_path(self):
        text = "![image](./images/photo.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "./images/photo.jpg")], matches)

    def test_extract_markdown_images_absolute_path(self):
        text = "![image](/static/img/logo.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "/static/img/logo.png")], matches)

    def test_extract_markdown_images_special_chars_in_url(self):
        text = "![image](https://example.com/path/to/image%20with%20spaces.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("image", "https://example.com/path/to/image%20with%20spaces.png")],
            matches,
        )

    def test_extract_markdown_images_mixed_with_links(self):
        text = "Check out ![this image](img.png) and [this link](https://example.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("this image", "img.png")], matches)

    def test_extract_markdown_images_multiple_same(self):
        text = "![same](img1.png) and ![same](img2.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("same", "img1.png"), ("same", "img2.png")],
            matches,
        )

    def test_extract_markdown_images_with_code_blocks(self):
        text = "Here's `code` and ![image](img.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "img.png")], matches)

    def test_extract_markdown_images_with_bold_text(self):
        text = "This is **bold** and ![image](img.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "img.png")], matches)

    # Additional tests for extract_markdown_links
    def test_extract_markdown_links_single(self):
        text = "Check out [this link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("this link", "https://example.com")], matches)

    def test_extract_markdown_links_no_links(self):
        text = "This is just plain text with no links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_empty_text(self):
        text = ""
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_at_start(self):
        text = "[first link](https://example.com) and some text"
        matches = extract_markdown_links(text)
        self.assertListEqual([("first link", "https://example.com")], matches)

    def test_extract_markdown_links_at_end(self):
        text = "Some text and [last link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("last link", "https://example.com")], matches)

    def test_extract_markdown_links_empty_anchor(self):
        text = "Link with [empty anchor]()"
        matches = extract_markdown_links(text)
        self.assertListEqual([("empty anchor", "")], matches)

    def test_extract_markdown_links_with_spaces_in_anchor(self):
        text = "[anchor text with spaces](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("anchor text with spaces", "https://example.com")], matches
        )

    def test_extract_markdown_links_http_url(self):
        text = "[link](http://example.com/page)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "http://example.com/page")], matches)

    def test_extract_markdown_links_relative_path(self):
        text = "[link](./pages/about.html)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "./pages/about.html")], matches)

    def test_extract_markdown_links_absolute_path(self):
        text = "[link](/docs/guide.md)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "/docs/guide.md")], matches)

    def test_extract_markdown_links_special_chars_in_url(self):
        text = "[link](https://example.com/path?query=value&other=123)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("link", "https://example.com/path?query=value&other=123")], matches
        )

    def test_extract_markdown_links_mixed_with_images(self):
        text = "Check out [this link](https://example.com) and ![this image](img.png)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("this link", "https://example.com")], matches)

    def test_extract_markdown_links_multiple_same(self):
        text = "[same](link1.html) and [same](link2.html)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("same", "link1.html"), ("same", "link2.html")],
            matches,
        )

    def test_extract_markdown_links_with_code_blocks(self):
        text = "Here's `code` and [link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_links_with_bold_text(self):
        text = "This is **bold** and [link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_links_anchor_with_special_chars(self):
        text = "[link with **bold** text](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("link with **bold** text", "https://example.com")], matches
        )

    def test_extract_markdown_links_url_with_hash(self):
        text = "[link](https://example.com/page#section)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com/page#section")], matches)

    def test_extract_markdown_links_url_with_port(self):
        text = "[link](http://localhost:8000/page)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "http://localhost:8000/page")], matches)

    def test_extract_markdown_links_does_not_extract_images(self):
        text = "This has ![an image](img.png) which should not be extracted"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_images_does_not_extract_links(self):
        text = "This has [a link](https://example.com) which should not be extracted"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_complex_text(self):
        text = "Visit [GitHub](https://github.com) for code, [Stack Overflow](https://stackoverflow.com) for questions, and [Reddit](https://reddit.com) for discussions."
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("GitHub", "https://github.com"),
                ("Stack Overflow", "https://stackoverflow.com"),
                ("Reddit", "https://reddit.com"),
            ],
            matches,
        )

    def test_extract_markdown_images_complex_text(self):
        text = "See ![screenshot](screenshot.png) of the app, ![logo](logo.svg) for branding, and ![diagram](diagram.png) for architecture."
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("screenshot", "screenshot.png"),
                ("logo", "logo.svg"),
                ("diagram", "diagram.png"),
            ],
            matches,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )


if __name__ == "__main__":
    unittest.main()
