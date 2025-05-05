import unittest

from src.block import (
    BlockType,
    block_to_block_type,
    markdown_to_html_node,
)


class BlockTypeTestCase(unittest.TestCase):
    def test_heading_block_type(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Subheading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### H3"), BlockType.HEADING)

    def test_code_block_type(self):
        self.assertEqual(block_to_block_type("``` Code block"), BlockType.CODE)
        self.assertEqual(
            block_to_block_type("```python\ndef hello():\n    print('world')\n```"),
            BlockType.CODE,
        )

    def test_quote_block_type(self):
        self.assertEqual(block_to_block_type("> Quote"), BlockType.QUOTE)
        self.assertEqual(
            block_to_block_type("> Multi-line\n> quote block"), BlockType.QUOTE
        )

    def test_unordered_list_block_type(self):
        self.assertEqual(
            block_to_block_type("- Unordered list"), BlockType.UNORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("* Another unordered list"), BlockType.UNORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("- Item 1\n- Item 2"), BlockType.UNORDERED_LIST
        )

    def test_ordered_list_block_type(self):
        self.assertEqual(block_to_block_type("1. Ordered list"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("2. Second item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("10. Tenth item"), BlockType.ORDERED_LIST)

    def test_paragraph_block_type(self):
        self.assertEqual(block_to_block_type("Paragraph text"), BlockType.PARAGRAPH)
        self.assertEqual(
            block_to_block_type("This is a simple paragraph."), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("Text with **bold** and _italic_"), BlockType.PARAGRAPH
        )

    def test_edge_cases(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("    Indented text"), BlockType.PARAGRAPH)
        self.assertEqual(
            block_to_block_type("a. Not an ordered list"), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("-Not a list without space"), BlockType.PARAGRAPH
        )

    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
