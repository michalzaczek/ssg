from enum import Enum
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
    delimeters_dict = {"bold": "**", "italic": "_", "code": "`"}
    d = delimeters_dict[delimiter]
    for node in old_nodes:
        split_parts = node.text.split(d)
        for i, split_part in enumerate(split_parts):
            # Even indices (0, 2, 4...) are outside delimiters (TEXT)
            # Odd indices (1, 3, 5...) are between delimiters (text_type)
            if i % 2 == 0:
                new_nodes.append(TextNode(split_part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_part, text_type))
    return new_nodes


# node = TextNode("This is text with a `code block` word", TextType.TEXT)
# new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)


# [
#     TextNode("This is text with a ", TextType.TEXT),
#     TextNode("code block", TextType.CODE),
#     TextNode(" word", TextType.TEXT),
# ]
