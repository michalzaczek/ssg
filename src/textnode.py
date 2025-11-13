from enum import Enum
import enum
import re
from htmlnode import LeafNode, ParentNode


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


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block_md):
    # Check for heading: 1-6 # characters followed by a space
    if re.match(r"^#{1,6} ", block_md):
        return BlockType.HEADING
    # Check for code block: starts and ends with exactly 3 backticks
    elif (
        len(block_md) > 6
        and block_md[:3] == "```"
        and block_md[-3:] == "```"
        and block_md[3] != "`"
        and block_md[-4] != "`"
    ):
        return BlockType.CODE
    # Check for quote: every line starts with >
    elif all([n.startswith(">") for n in block_md.split("\n")]):
        return BlockType.QUOTE
    # Check for unordered list: every line starts with "- "
    elif all([n.startswith("- ") for n in block_md.split("\n")]):
        return BlockType.UNORDERED_LIST
    # Check for ordered list: every line starts with number. and numbers are sequential
    else:
        lines = block_md.split("\n")
        if all([re.match(r"^\d+\. ", line) for line in lines]):
            # Check if numbers start at 1 and increment by 1
            for i, line in enumerate(lines):
                match = re.match(r"^(\d+)\. ", line)
                if match:
                    expected_num = i + 1
                    actual_num = int(match.group(1))
                    if actual_num != expected_num:
                        return BlockType.PARAGRAPH
            return BlockType.ORDERED_LIST
        return BlockType.PARAGRAPH


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


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes_with_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodes_with_italic = split_nodes_delimiter(nodes_with_bold, "_", TextType.ITALIC)
    nodes_with_code = split_nodes_delimiter(nodes_with_italic, "`", TextType.CODE)
    nodes_with_images = split_nodes_image(nodes_with_code)
    all_nodes = split_nodes_link(nodes_with_images)
    return all_nodes


def markdown_to_blocks(markdown):
    blocks = [md.strip() for md in markdown.split("\n\n")]
    return [b for b in blocks if b]


def block_has_various_children(block):
    return any(tn.text_type != TextType.TEXT for tn in block)


def block_type_to_tag(block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            return "h1"  # Default heading level; caller should determine actual level from block content
        case BlockType.CODE:
            return "pre"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
        case _:
            raise ValueError(f"Unsupported block type: {block_type}")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        tag = block_type_to_tag(block_type)

        # Code blocks are special: no inline markdown parsing
        if block_type == BlockType.CODE:
            # Strip the triple backticks from start and end
            code_content = block[3:-3].strip()
            # Manually create TextNode and convert - no inline parsing
            text_node = TextNode(code_content, TextType.TEXT)
            html_node = text_node_to_html_node(text_node)
            current_node = ParentNode(tag, [html_node])
        else:
            text_nodes = text_to_textnodes(block)
            # Convert TextNode objects to HTMLNode objects
            html_children = [text_node_to_html_node(tn) for tn in text_nodes]
            if block_has_various_children(text_nodes):
                current_node = ParentNode(tag, html_children)
            else:
                # If all are TEXT nodes, concatenate them into a single string
                text_value = "".join(tn.text for tn in text_nodes)
                current_node = LeafNode(tag, text_value)

        html_nodes.append(current_node)

    # Wrap all block nodes in a single parent div
    return ParentNode("div", html_nodes)


md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

res = markdown_to_html_node(md)
print(res.to_html())
