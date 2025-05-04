import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("This is a leaf node", "Bold")
        node2 = LeafNode("This is a leaf node", "Bold")
        self.assertEqual(node, node2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_span(self):
        node = LeafNode("span", "Hello, world!")
        self.assertEqual(node.to_html(), "<span>Hello, world!</span>")

    def test_ne(self):
        node = LeafNode("This is a leaf node", "Bold")
        node2 = LeafNode("This is a leaf node", "Italic")
        self.assertNotEqual(node, node2)

    def test_ne2(self):
        node = LeafNode("This is a leaf node", "Bold")
        node2 = LeafNode("This is a different leaf node", "Bold")
        self.assertNotEqual(node, node2)