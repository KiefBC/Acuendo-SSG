import unittest

from inline import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    text_node_to_html_node,
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


if __name__ == "__main__":
    unittest.main()
