from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    NORMAL = "Normal",
    BOLD = "Bold",
    ITALIC = "Italic",
    CODE = "Code"
    URL = "URL"
    IMG = "Image"

# I SPENT SO LONG ON THIS REALIZING I FORGOT TO PASS `tag: None`
# TEST AFTER TEST FOR SOMETHING SO DUMB FUCK
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.URL:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMG:
            return LeafNode("img", None, {"src": text_node.url})
        case _:
            raise ValueError("Invalid text type")


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
