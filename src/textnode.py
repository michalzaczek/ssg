from enum import Enum


class TextType(Enum):
    TEXT = "text"  # plain text
    BOLD = "bold"  # **Bold text**
    ITALIC = "italic"  # _Italic text_
    CODE = "code"  # `Code text`
    LINK = "link"  # [anchor text](url)
    IMAGE = "image"  # ![alt text](url)
