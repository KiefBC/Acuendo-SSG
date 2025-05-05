import re
from enum import Enum

from inline import markdown_to_blocks, text_node_to_html_node, text_to_textnodes
from parentnode import ParentNode
from textnode import TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "Paragraph"
    HEADING = "Heading"
    CODE = "Code"
    QUOTE = "Quote"
    UNORDERED_LIST = "Unordered List"
    ORDERED_LIST = "Ordered List"


def block_to_block_type(md):
    md = md.strip()
    if md.startswith("#"):
        return BlockType.HEADING
    if md.startswith("```"):
        return BlockType.CODE
    if md.startswith(">"):
        return BlockType.QUOTE
    if md.startswith("- ") or md.startswith("* "):
        return BlockType.UNORDERED_LIST
    if re.match(r"^\d+\.\s", md):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def text_to_children(text):
    """
    Convert a string of text to a list of HTMLNode objects representing inline elements
    """
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
    return html_nodes


def paragraph_to_html_node(block):
    clean_block = block.replace("\n", " ")
    children = text_to_children(clean_block)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break

    text = block[level:].strip()
    text = text.replace("\n", " ")
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if block.startswith("```"):
        lines = block.split("\n")
        if lines[-1] == "```":
            code_content = "\n".join(lines[1:-1]) + "\n"
        else:
            code_content = "\n".join(lines[1:]) + "\n"
    else:
        code_content = block

    text_node = TextNode(code_content, TextType.NORMAL)
    code_node = text_node_to_html_node(text_node)
    return ParentNode("pre", [ParentNode("code", [code_node])])


def quote_to_html_node(block):
    """Convert a quote block to an HTML node"""
    lines = block.split("\n")
    quote_content = "\n".join(
        [line[1:].strip() if line.startswith(">") else line.strip() for line in lines]
    )
    children = text_to_children(quote_content)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    """Convert an unordered list block to an HTML node"""
    lines = block.split("\n")
    list_items = []

    for line in lines:
        if line.startswith("- "):
            item_text = line[2:].strip()
        elif line.startswith("* "):
            item_text = line[2:].strip()
        else:
            item_text = line.strip()

        if item_text:
            children = text_to_children(item_text)
            list_items.append(ParentNode("li", children))

    return ParentNode("ul", list_items)


def ordered_list_to_html_node(block):
    """Convert an ordered list block to an HTML node"""
    lines = block.split("\n")
    list_items = []

    for line in lines:
        # Extract the text after the number and period
        match = re.match(r"^\d+\.\s*(.*)", line)
        if match:
            item_text = match.group(1).strip()
            children = text_to_children(item_text)
            list_items.append(ParentNode("li", children))

    return ParentNode("ol", list_items)


def markdown_to_html_node(markdown):
    """
    Convert a full markdown document to a single parent HTMLNode
    """
    markdown = markdown.strip("\n")
    blocks = markdown_to_blocks(markdown)

    block_nodes = []
    for block in blocks:
        if not block:
            continue

        block_node = None
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            block_node = paragraph_to_html_node(block)
        elif block_type == BlockType.HEADING:
            block_node = heading_to_html_node(block)
        elif block_type == BlockType.CODE:
            block_node = code_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            block_node = quote_to_html_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            block_node = unordered_list_to_html_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            block_node = ordered_list_to_html_node(block)

        block_nodes.append(block_node)

    return ParentNode("div", block_nodes)
