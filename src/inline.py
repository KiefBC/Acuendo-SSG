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


def text_to_textnodes(text):
    # Start with one big normal text node
    nodes = [TextNode(text, TextType.NORMAL)]

    # First split code blocks (backticks)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    # Then split bold (double asterisks)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    # Then split italic (underscores)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    # Then split images
    nodes = split_nodes_image(nodes)

    # Then split links
    nodes = split_nodes_link(nodes)

    return nodes


def split_nodes_image(old_nodes):
    result = []

    for old_node in old_nodes:
        if not isinstance(old_node, TextNode) or old_node.text_type != TextType.NORMAL:
            result.append(old_node)
            continue

        matches = extract_markdown_images(old_node.text)

        if not matches:
            result.append(old_node)
            continue

        # Split the text into parts
        parts = []
        last_index = 0

        for alt_text, url in matches:
            start_index = old_node.text.index(f"![{alt_text}]({url})", last_index)
            if start_index > last_index:
                parts.append(
                    TextNode(old_node.text[last_index:start_index], TextType.NORMAL)
                )
            parts.append(TextNode(alt_text, TextType.IMG, url))
            last_index = start_index + len(f"![{alt_text}]({url})")

        if last_index < len(old_node.text):
            parts.append(TextNode(old_node.text[last_index:], TextType.NORMAL))

        result.extend(parts)

    return result


def split_nodes_link(old_nodes):
    result = []

    for old_node in old_nodes:
        if not isinstance(old_node, TextNode) or old_node.text_type != TextType.NORMAL:
            result.append(old_node)
            continue

        text = old_node.text
        matches = extract_markdown_links(text)

        if not matches:
            result.append(old_node)
            continue

        last_index = 0

        for link_text, url in matches:
            # Find the position of this link markdown in the text starting from last_index
            link_markdown = f"[{link_text}]({url})"
            start_index = text.index(link_markdown, last_index)

            # Text before the link
            if start_index > last_index:
                before_text = text[last_index:start_index]
                if before_text:
                    result.append(TextNode(before_text, TextType.NORMAL))

            # Link node
            result.append(TextNode(link_text, TextType.URL, url))

            # Update last_index to after this link markdown
            last_index = start_index + len(link_markdown)

        # Text after the last link markdown
        if last_index < len(text):
            after_text = text[last_index:]
            if after_text:
                result.append(TextNode(after_text, TextType.NORMAL))

    return result


def extract_markdown_images(text):
    return re.findall(r"!\[([^]]+)]\(([^)]+)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[([^]]+)]\(([^)]+)\)", text)


def markdown_to_blocks(markdown):
    splits = markdown.split("\n\n")
    blocks = []

    for block in splits:
        # Split into individual lines
        lines = block.split("\n")

        # Strip whitespaces
        stripped_lines = [line.strip() for line in lines]
        cleaned_block = "\n".join(stripped_lines)
        blocks.append(cleaned_block.strip("\n"))

    return blocks

