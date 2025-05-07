import unittest

from src.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("div", "This is a div", None, None)
        node2 = HTMLNode("div", "This is a div", None, None)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = HTMLNode("div", "This is a div", None, {"class": "my-class"})
        node2 = HTMLNode("div", "This is a div", None, {"class": "my-class"})
        self.assertEqual(node, node2)

    def test_ne(self):
        node = HTMLNode("div", "This is a div", None, {"class": "my-class"})
        node2 = HTMLNode(
            "div", "This is a div", None, {"class": "my-class", "id": "my-id"}
        )
        self.assertNotEqual(node, node2)

    def test_ne1(self):
        node = HTMLNode("div", "This is a div", None, None)
        node2 = HTMLNode("span", "This is a div", None, None)
        self.assertNotEqual(node, node2)

    def test_ne2(self):
        node = HTMLNode("div", "This is a div", None, None)
        node2 = HTMLNode("div", "This is a different div", None, None)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = HTMLNode("div", "This is a div", None, None)
        self.assertEqual(repr(node), "HTMLNode(div, This is a div, None, None)")

    def test_props_to_html(self):
        node = HTMLNode("div", "This is a div", None, {"class": "my-class"})
        self.assertEqual(node.props_to_html(), "class=my-class")

