import re

from leafnode import LeafNode
from textnode import TextNode, TextType


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


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []

    for old_node in old_nodes:
        if not isinstance(old_node, TextNode) or old_node.text_type != TextType.NORMAL:
            result.append(old_node)
            continue

        splits = old_node.text.split(delimiter)

        if len(splits) == 1:
            result.append(old_node)
            continue

        for i in range(len(splits)):
            if i % 2 == 0:
                # Even index: normal text
                if splits[i]:  # Only add non-empty text
                    result.append(TextNode(splits[i], TextType.NORMAL))
            else:
                # Odd index: special text_type
                if splits[i]:  # Only add non-empty text
                    result.append(TextNode(splits[i], text_type))

    return result


def extract_markdown_images(text):
    return re.findall(r"!\[([^]]+)]\(([^)]+)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[([^]]+)]\(([^)]+)\)", text)
