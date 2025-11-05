from enum import Enum


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
