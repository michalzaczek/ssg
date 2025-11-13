import unittest

from textnode import (
    BlockType,
    TextNode,
    TextType,
    block_to_block_type,
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    markdown_to_html_node,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_textnodes,
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

    # Additional tests for split_nodes_image
    def test_split_nodes_image_single(self):
        node = TextNode(
            "Check out this ![image](https://example.com/img.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Check out this ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            ],
            new_nodes,
        )

    def test_split_nodes_image_at_start(self):
        node = TextNode(
            "![first](https://example.com/img1.png) and some text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("", TextType.TEXT),
                TextNode("first", TextType.IMAGE, "https://example.com/img1.png"),
                TextNode(" and some text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_at_end(self):
        node = TextNode(
            "Some text and ![last](https://example.com/img2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Some text and ", TextType.TEXT),
                TextNode("last", TextType.IMAGE, "https://example.com/img2.png"),
            ],
            new_nodes,
        )

    def test_split_nodes_image_only_image(self):
        node = TextNode("![only](img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("", TextType.TEXT),
                TextNode("only", TextType.IMAGE, "img.png"),
            ],
            new_nodes,
        )

    def test_split_nodes_image_no_images(self):
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_image_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_image_text_after_last(self):
        node = TextNode(
            "Start ![img](url.png) middle ![img2](url2.png) end text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "url.png"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "url2.png"),
                TextNode(" end text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_non_text_node_passes_through(self):
        bold_node = TextNode("![test](img.png)", TextType.BOLD)
        new_nodes = split_nodes_image([bold_node])
        self.assertListEqual([bold_node], new_nodes)

    def test_split_nodes_image_mixed_node_types(self):
        text_node = TextNode("Text with ![img](url.png)", TextType.TEXT)
        bold_node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_image([text_node, bold_node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "url.png"),
                TextNode("Already bold", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_split_nodes_image_multiple_nodes(self):
        node1 = TextNode("First ![img1](url1.png) text", TextType.TEXT)
        node2 = TextNode("Second ![img2](url2.png) text", TextType.TEXT)
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "url1.png"),
                TextNode(" text", TextType.TEXT),
                TextNode("Second ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "url2.png"),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_with_spaces_in_alt(self):
        node = TextNode(
            "Text ![alt text with spaces](https://example.com/img.png) more",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text ", TextType.TEXT),
                TextNode(
                    "alt text with spaces",
                    TextType.IMAGE,
                    "https://example.com/img.png",
                ),
                TextNode(" more", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_relative_path(self):
        node = TextNode("See ![logo](./images/logo.png) here", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("See ", TextType.TEXT),
                TextNode("logo", TextType.IMAGE, "./images/logo.png"),
                TextNode(" here", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_three_images(self):
        node = TextNode(
            "![first](1.png) and ![second](2.png) and ![third](3.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("", TextType.TEXT),
                TextNode("first", TextType.IMAGE, "1.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("second", TextType.IMAGE, "2.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("third", TextType.IMAGE, "3.png"),
            ],
            new_nodes,
        )

    def test_split_nodes_image_with_links(self):
        node = TextNode(
            "Text ![img](img.png) and [link](url) more",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "img.png"),
                TextNode(" and [link](url) more", TextType.TEXT),
            ],
            new_nodes,
        )

    # Additional tests for split_nodes_link
    def test_split_nodes_link_single(self):
        node = TextNode(
            "Check out this [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check out this ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_at_start(self):
        node = TextNode(
            "[first](https://example.com) and some text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("", TextType.TEXT),
                TextNode("first", TextType.LINK, "https://example.com"),
                TextNode(" and some text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_link_at_end(self):
        node = TextNode(
            "Some text and [last](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Some text and ", TextType.TEXT),
                TextNode("last", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_only_link(self):
        node = TextNode("[only](url)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("", TextType.TEXT),
                TextNode("only", TextType.LINK, "url"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_no_links(self):
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_link_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_link_text_after_last(self):
        node = TextNode(
            "Start [link1](url1) middle [link2](url2) end text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "url1"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "url2"),
                TextNode(" end text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_link_non_text_node_passes_through(self):
        bold_node = TextNode("[test](url)", TextType.BOLD)
        new_nodes = split_nodes_link([bold_node])
        self.assertListEqual([bold_node], new_nodes)

    def test_split_nodes_link_mixed_node_types(self):
        text_node = TextNode("Text with [link](url)", TextType.TEXT)
        bold_node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_link([text_node, bold_node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
                TextNode("Already bold", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_split_nodes_link_multiple_nodes(self):
        node1 = TextNode("First [link1](url1) text", TextType.TEXT)
        node2 = TextNode("Second [link2](url2) text", TextType.TEXT)
        new_nodes = split_nodes_link([node1, node2])
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "url1"),
                TextNode(" text", TextType.TEXT),
                TextNode("Second ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "url2"),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_link_with_spaces_in_anchor(self):
        node = TextNode(
            "Text [anchor text with spaces](https://example.com) more",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text ", TextType.TEXT),
                TextNode(
                    "anchor text with spaces", TextType.LINK, "https://example.com"
                ),
                TextNode(" more", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_link_relative_path(self):
        node = TextNode("See [page](./pages/about.html) here", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("See ", TextType.TEXT),
                TextNode("page", TextType.LINK, "./pages/about.html"),
                TextNode(" here", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_link_three_links(self):
        node = TextNode(
            "[first](1.html) and [second](2.html) and [third](3.html)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("", TextType.TEXT),
                TextNode("first", TextType.LINK, "1.html"),
                TextNode(" and ", TextType.TEXT),
                TextNode("second", TextType.LINK, "2.html"),
                TextNode(" and ", TextType.TEXT),
                TextNode("third", TextType.LINK, "3.html"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_with_images(self):
        node = TextNode(
            "Text [link](url) and ![img](img.png) more",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
                TextNode(" and ![img](img.png) more", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_link_special_chars_in_url(self):
        node = TextNode(
            "Visit [page](https://example.com/path?query=value&other=123)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode(
                    "page",
                    TextType.LINK,
                    "https://example.com/path?query=value&other=123",
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_link_url_with_hash(self):
        node = TextNode(
            "See [section](https://example.com/page#section)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("See ", TextType.TEXT),
                TextNode("section", TextType.LINK, "https://example.com/page#section"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_complex_mixed_content(self):
        node = TextNode(
            "Start [link1](url1) middle ![img](img.png) and [link2](url2) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "url1"),
                TextNode(" middle ![img](img.png) and ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "url2"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_complex_mixed_content(self):
        node = TextNode(
            "Start ![img1](img1.png) middle [link](url) and ![img2](img2.png) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "img1.png"),
                TextNode(" middle [link](url) and ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "img2.png"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_link_empty_anchor(self):
        node = TextNode("Link with [empty anchor]() text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Link with ", TextType.TEXT),
                TextNode("empty anchor", TextType.LINK, ""),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_empty_alt(self):
        node = TextNode("Image with ![empty alt]() text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Image with ", TextType.TEXT),
                TextNode("empty alt", TextType.IMAGE, ""),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )

    # Tests for text_to_textnodes
    def test_text_to_textnodes_example(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_plain_text(self):
        text = "This is just plain text"
        result = text_to_textnodes(text)
        expected = [TextNode("This is just plain text", TextType.TEXT)]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_only_bold(self):
        text = "This is **bold** text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_only_italic(self):
        text = "This is _italic_ text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_only_code(self):
        text = "This is `code` text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_only_image(self):
        text = "This is ![image](url.png) text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url.png"),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_only_link(self):
        text = "This is [link](url) text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_multiple_bold(self):
        text = "**first** and **second** bold"
        result = text_to_textnodes(text)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("first", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.BOLD),
            TextNode(" bold", TextType.TEXT),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_bold_and_italic(self):
        text = "**bold** and _italic_ text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_all_types(self):
        text = "**bold** _italic_ `code` ![img](img.png) [link](url)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "img.png"),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_empty_string(self):
        text = ""
        result = text_to_textnodes(text)
        expected = [TextNode("", TextType.TEXT)]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_nested_delimiters(self):
        # Nested delimiters don't work because once text is BOLD, it's no longer TEXT
        text = "**bold with _italic_ inside**"
        result = text_to_textnodes(text)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("bold with _italic_ inside", TextType.BOLD),
            TextNode("", TextType.TEXT),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_multiple_images(self):
        text = "![img1](url1.png) and ![img2](url2.png)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "url1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2.png"),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_multiple_links(self):
        text = "[link1](url1) and [link2](url2)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_image_and_link(self):
        text = "See ![image](img.png) and [link](url)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("See ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "img.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_complex_mixed(self):
        text = "Start **bold** _italic_ `code` ![img](img.png) [link](url) end"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "img.png"),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_code_in_bold(self):
        # Nested delimiters don't work because once text is BOLD, it's no longer TEXT
        text = "**bold with `code` inside**"
        result = text_to_textnodes(text)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("bold with `code` inside", TextType.BOLD),
            TextNode("", TextType.TEXT),
        ]
        self.assertListEqual(expected, result)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_whitespace(self):
        md = "   \n\n   \n\n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_single_block(self):
        md = "This is a single block with no double newlines"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single block with no double newlines"])

    def test_markdown_to_blocks_excessive_newlines(self):
        md = "Block 1\n\n\n\nBlock 2\n\n\n\n\nBlock 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Block 1",
                "Block 2",
                "Block 3",
            ],
        )

    def test_markdown_to_blocks_leading_trailing_whitespace(self):
        md = "   Block 1   \n\n   Block 2   \n\n   Block 3   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Block 1",
                "Block 2",
                "Block 3",
            ],
        )

    def test_markdown_to_blocks_with_headings(self):
        md = """# Heading 1

## Heading 2

### Heading 3"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading 1",
                "## Heading 2",
                "### Heading 3",
            ],
        )

    def test_markdown_to_blocks_with_code_blocks(self):
        md = """```
code block
with multiple lines
```

Regular paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "```\ncode block\nwith multiple lines\n```",
                "Regular paragraph",
            ],
        )

    def test_markdown_to_blocks_mixed_content(self):
        md = """# Title

Paragraph with **bold** and _italic_.

- List item 1
- List item 2

Another paragraph."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Title",
                "Paragraph with **bold** and _italic_.",
                "- List item 1\n- List item 2",
                "Another paragraph.",
            ],
        )

    def test_markdown_to_blocks_preserves_single_newlines(self):
        md = """Block with
multiple lines
in one block

Another block"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Block with\nmultiple lines\nin one block",
                "Another block",
            ],
        )

    def test_markdown_to_blocks_empty_blocks_removed(self):
        md = "Block 1\n\n\n\n\n\nBlock 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])

    def test_markdown_to_blocks_only_newlines(self):
        md = "\n\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    # Tests for block_to_block_type
    def test_block_to_block_type_paragraph(self):
        block = "This is a regular paragraph with some text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_with_newlines(self):
        block = "This is a paragraph\nwith multiple lines\nbut no special formatting"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading_h1(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_h2(self):
        block = "## Heading 2"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_h3(self):
        block = "### Heading 3"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_h4(self):
        block = "#### Heading 4"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_h5(self):
        block = "##### Heading 5"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_h6(self):
        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_too_many_hashes(self):
        block = "####### Too many hashes"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading_no_space(self):
        block = "#Heading without space"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading_with_content(self):
        block = "# This is a heading with **bold** and _italic_"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_code_block_single_line(self):
        block = "```code```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_code_block_multi_line(self):
        block = "```\ncode block\nwith multiple lines\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_code_block_empty(self):
        block = "``````"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_code_block_two_backticks(self):
        block = "``code``"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_code_block_four_backticks(self):
        block = "````code````"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_code_block_with_content(self):
        block = "```\ndef hello():\n    print('world')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_quote_single_line(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_quote_multi_line(self):
        block = "> First line of quote\n> Second line of quote\n> Third line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_quote_not_all_lines(self):
        block = "> First line\nSecond line without >"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote_with_content(self):
        block = "> This is a **bold** quote\n> with _italic_ text"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list_single_item(self):
        block = "- First item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_multiple_items(self):
        block = "- First item\n- Second item\n- Third item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_not_all_lines(self):
        block = "- First item\nSecond item without dash"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list_no_space(self):
        block = "-First item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list_with_content(self):
        block = "- Item with **bold**\n- Item with _italic_"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list_single_item(self):
        block = "1. First item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_multiple_items(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_sequential(self):
        block = "1. One\n2. Two\n3. Three\n4. Four\n5. Five"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_not_starting_at_one(self):
        block = "2. Starts at two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_skips_number(self):
        block = "1. First\n3. Skips two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_wrong_order(self):
        block = "1. First\n2. Second\n4. Skips three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_not_all_lines(self):
        block = "1. First item\nNot a numbered item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_no_space(self):
        block = "1.First item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_double_digit(self):
        block = "1. First\n2. Second\n3. Third\n4. Fourth\n5. Fifth\n6. Sixth\n7. Seventh\n8. Eighth\n9. Ninth\n10. Tenth\n11. Eleventh"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_with_content(self):
        block = "1. Item with **bold**\n2. Item with _italic_"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_zero(self):
        block = "0. Starts at zero"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_negative(self):
        block = "-1. Negative number"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_mixed_unordered_ordered(self):
        block = "- Unordered item\n1. Ordered item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_empty_string(self):
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_just_hashes(self):
        block = "####"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading_with_multiple_spaces(self):
        block = "#  Heading with multiple spaces"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_code_block_with_language(self):
        block = "```python\ndef hello():\n    pass\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_quote_empty_line(self):
        block = ">\n> Content here"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list_empty_item(self):
        block = "- \n- Item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list_empty_item(self):
        block = "1. \n2. Item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_markdown_to_html_node_heading_h1(self):
        md = "# This is a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>This is a heading</h1></div>")

    def test_markdown_to_html_node_heading_h2(self):
        md = "## This is an h2"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h2>This is an h2</h2></div>")

    def test_markdown_to_html_node_heading_h3(self):
        md = "### This is an h3"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h3>This is an h3</h3></div>")

    def test_markdown_to_html_node_heading_h4(self):
        md = "#### This is an h4"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h4>This is an h4</h4></div>")

    def test_markdown_to_html_node_heading_h5(self):
        md = "##### This is an h5"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h5>This is an h5</h5></div>")

    def test_markdown_to_html_node_heading_h6(self):
        md = "###### This is an h6"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h6>This is an h6</h6></div>")

    def test_markdown_to_html_node_heading_with_bold(self):
        md = "# This is a **bold** heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>This is a <b>bold</b> heading</h1></div>")

    def test_markdown_to_html_node_quote_single_line(self):
        md = ">This is a quote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a quote</blockquote></div>")

    def test_markdown_to_html_node_quote_multi_line(self):
        md = ">Line one\n>Line two\n>Line three"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Line one Line two Line three</blockquote></div>",
        )

    def test_markdown_to_html_node_quote_with_formatting(self):
        md = ">This is a **bold** quote with `code`"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a <b>bold</b> quote with <code>code</code></blockquote></div>",
        )

    def test_markdown_to_html_node_unordered_list_single_item(self):
        md = "- Item one"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>Item one</li></ul></div>")

    def test_markdown_to_html_node_unordered_list_multiple_items(self):
        md = "- Item one\n- Item two\n- Item three"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item one</li><li>Item two</li><li>Item three</li></ul></div>",
        )

    def test_markdown_to_html_node_unordered_list_with_formatting(self):
        md = "- **Bold** item\n- _Italic_ item\n- `Code` item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li><b>Bold</b> item</li><li><i>Italic</i> item</li><li><code>Code</code> item</li></ul></div>",
        )

    def test_markdown_to_html_node_ordered_list_single_item(self):
        md = "1. First item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>First item</li></ol></div>")

    def test_markdown_to_html_node_ordered_list_multiple_items(self):
        md = "1. First\n2. Second\n3. Third"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>"
        )

    def test_markdown_to_html_node_ordered_list_with_formatting(self):
        md = "1. **First** item\n2. Second item\n3. _Third_ item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li><b>First</b> item</li><li>Second item</li><li><i>Third</i> item</li></ol></div>",
        )

    def test_markdown_to_html_node_mixed_blocks(self):
        md = """# Heading

This is a paragraph.

- List item 1
- List item 2

>A quote"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading</h1><p>This is a paragraph.</p><ul><li>List item 1</li><li>List item 2</li></ul><blockquote>A quote</blockquote></div>",
        )

    def test_markdown_to_html_node_all_block_types(self):
        md = """# Main Heading

## Subheading

This is a **paragraph** with _formatting_.

```
code block here
```

>This is a quote

- Unordered item 1
- Unordered item 2

1. Ordered item 1
2. Ordered item 2"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<h1>Main Heading</h1>", html)
        self.assertIn("<h2>Subheading</h2>", html)
        self.assertIn("<p>This is a <b>paragraph</b> with <i>formatting</i>.</p>", html)
        self.assertIn("<pre><code>code block here", html)
        self.assertIn("<blockquote>This is a quote</blockquote>", html)
        self.assertIn(
            "<ul><li>Unordered item 1</li><li>Unordered item 2</li></ul>", html
        )
        self.assertIn("<ol><li>Ordered item 1</li><li>Ordered item 2</li></ol>", html)

    def test_markdown_to_html_node_empty_markdown(self):
        md = ""
        node = markdown_to_html_node(md)
        # Empty markdown creates a div with no children, which raises an error
        with self.assertRaises(ValueError):
            html = node.to_html()

    def test_markdown_to_html_node_only_whitespace(self):
        md = "   \n\n  \n   "
        node = markdown_to_html_node(md)
        # Whitespace-only markdown creates a div with no children, which raises an error
        with self.assertRaises(ValueError):
            html = node.to_html()

    def test_markdown_to_html_node_paragraph_with_link(self):
        md = "This is a paragraph with a [link](https://example.com) in it."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is a paragraph with a <a href="https://example.com">link</a> in it.</p></div>',
        )

    def test_markdown_to_html_node_paragraph_with_image(self):
        md = "This is a paragraph with an ![image](https://example.com/img.png) in it."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is a paragraph with an <img src="https://example.com/img.png" alt="image" /> in it.</p></div>',
        )

    def test_markdown_to_html_node_code_block_empty(self):
        md = "```\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><pre><code></code></pre></div>")

    def test_markdown_to_html_node_code_block_single_line(self):
        md = "```\nprint('hello')\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        # Code blocks preserve trailing newline
        self.assertEqual(html, "<div><pre><code>print('hello')\n</code></pre></div>")

    def test_markdown_to_html_node_code_block_preserves_indentation(self):
        md = """```
def hello():
    print('world')
    return True
```"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<pre><code>def hello():", html)
        self.assertIn("print('world')", html)
        self.assertIn("return True", html)

    def test_markdown_to_html_node_multiple_paragraphs(self):
        md = """First paragraph.

Second paragraph.

Third paragraph."""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>First paragraph.</p><p>Second paragraph.</p><p>Third paragraph.</p></div>",
        )

    def test_markdown_to_html_node_paragraph_multiline_text(self):
        md = """This is a paragraph
that spans multiple
lines but should be
collapsed into one."""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a paragraph that spans multiple lines but should be collapsed into one.</p></div>",
        )

    def test_markdown_to_html_node_heading_with_multiple_formatting(self):
        md = "# A **bold** and _italic_ heading with `code`"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>A <b>bold</b> and <i>italic</i> heading with <code>code</code></h1></div>",
        )

    def test_process_code_block_removes_indentation(self):
        from textnode import process_code_block

        block = """```
    line 1
    line 2
    line 3
```"""
        result = process_code_block(block, "pre")
        html = result.to_html()
        # Trailing newline is preserved
        self.assertEqual(html, "<pre><code>line 1\nline 2\nline 3\n</code></pre>")

    def test_process_code_block_preserves_relative_indentation(self):
        from textnode import process_code_block

        block = """```
    def hello():
        print('world')
        return True
```"""
        result = process_code_block(block, "pre")
        html = result.to_html()
        # Should preserve relative indentation (4 spaces for nested content)
        self.assertIn("def hello():\n    print('world')\n    return True", html)

    def test_process_code_block_strips_trailing_whitespace(self):
        from textnode import process_code_block

        block = "```\nline 1   \nline 2\t\t\nline 3\n```"
        result = process_code_block(block, "pre")
        html = result.to_html()
        # Trailing whitespace is stripped from each line, trailing newline is preserved
        self.assertEqual(html, "<pre><code>line 1\nline 2\nline 3\n</code></pre>")


if __name__ == "__main__":
    unittest.main()
