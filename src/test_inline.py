import unittest

from inline import (
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestInline(unittest.TestCase):
    def test_split_nodes_delimiter_with_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
        ]

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_with_multiple_delimiters(self):
        node = TextNode("Text with `multiple` `code` blocks", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("Text with ", TextType.NORMAL),
            TextNode("multiple", TextType.CODE),
            TextNode(" ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" blocks", TextType.NORMAL),
        ]

        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_with_no_delimiters(self):
        node = TextNode("Text with no delimiters", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [TextNode("Text with no delimiters", TextType.NORMAL)]

        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes, expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com)"
        )
        self.assertListEqual([("link", "https://www.google.com")], matches)

    def test_text_node_to_html_node(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMG, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMG, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [second link](https://www.example.com)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("link", TextType.URL, "https://www.google.com"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode("second link", TextType.URL, "https://www.example.com"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_complex(self):
        input_text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )

        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMG, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.URL, "https://boot.dev"),
        ]

        nodes = text_to_textnodes(input_text)
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_plain_text(self):
        input_text = "Just a simple plain text with no markdown."
        expected = [TextNode(input_text, TextType.NORMAL)]

        nodes = text_to_textnodes(input_text)
        self.assertEqual(nodes, expected)

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

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [""])

    def test_markdown_to_blocks_only_whitespace(self):
        md = "   \n  \n\n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["", ""])

    def test_markdown_to_blocks_multiple_blank_lines(self):
        md = "Paragraph one\n\n\n\nParagraph two"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Paragraph one", "", "Paragraph two"])

    def test_markdown_to_blocks_leading_trailing_spaces(self):
        md = "   Leading spaces paragraph   \n\n  Trailing spaces paragraph  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Leading spaces paragraph", "Trailing spaces paragraph"])

    def test_markdown_to_blocks_mixed_whitespace_lines(self):
        md = """
    First paragraph line 1
      First paragraph line 2    

    Second paragraph line 1
    Second paragraph line 2  
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First paragraph line 1\nFirst paragraph line 2",
                "Second paragraph line 1\nSecond paragraph line 2",
            ],
        )


if __name__ == "__main__":
    unittest.main()
