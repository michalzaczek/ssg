from enum import Enum
import re
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"  # plain text
    BOLD = "bold"  # **Bold text**
    ITALIC = "italic"  # _Italic text_
    CODE = "code"  # `Code text`
    LINK = "link"  # [anchor text](url)
    IMAGE = "image"  # ![alt text](url)


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, target):
        return (
            self.text == target.text
            and self.text_type == target.text_type
            and self.url == target.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    props = None
    match text_node.text_type:
        case TextType.TEXT:
            tag = None
        case TextType.BOLD:
            tag = "b"
        case TextType.ITALIC:
            tag = "i"
        case TextType.CODE:
            tag = "code"
        case TextType.LINK:
            tag = "a"
            props = {"href": text_node.url}
        case TextType.IMAGE:
            tag = "img"
            props = {"src": text_node.url, "alt": text_node.text}
            return LeafNode(tag, "", props)
        case _:
            raise Exception("Error: Unsupported text type")

    return LeafNode(tag, text_node.text, props)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        # If node is not TEXT type, add it as-is without splitting
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_parts = node.text.split(delimiter)

        # Check if delimiters are matched (odd number of splits means unmatched)
        if len(split_parts) % 2 == 0:
            raise ValueError(
                f"Invalid markdown: unmatched delimiter '{delimiter}' in text: {node.text}"
            )

        split_node_list = []
        for i, split_part in enumerate(split_parts):
            # Even indices (0, 2, 4...) are outside delimiters (TEXT)
            # Odd indices (1, 3, 5...) are between delimiters (text_type)
            if i % 2 == 0:
                split_node_list.append(TextNode(split_part, TextType.TEXT))
            else:
                split_node_list.append(TextNode(split_part, text_type))

        new_nodes.extend(split_node_list)

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # If node is not TEXT type, add it as-is without splitting
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)

        # If no images found, add the node as-is
        if not images:
            new_nodes.append(node)
            continue

        text = node.text
        for alt, url in images:
            md = f"![{alt}]({url})"
            first, rest = text.split(md, 1)
            text = rest
            new_nodes.append(TextNode(first, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

        # Add any remaining text after the last image
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # If node is not TEXT type, add it as-is without splitting
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)

        # If no links found, add the node as-is
        if not links:
            new_nodes.append(node)
            continue

        text = node.text
        for value, href in links:
            md = f"[{value}]({href})"
            first, rest = text.split(md, 1)
            text = rest
            new_nodes.append(TextNode(first, TextType.TEXT))
            new_nodes.append(TextNode(value, TextType.LINK, href))

        # Add any remaining text after the last link
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes
