import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):    
    
    def test_props(self):
        node = HTMLNode("a", None, None, {"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("a", None, None, {"href": "https://www.google.com", "oli": "mado"})

        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
        self.assertEqual(node2.props_to_html(), ' href="https://www.google.com" oli="mado"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Mado", {"href": "https://oliviergaudet.ca"})
        self.assertEqual(node.to_html(), '<a href="https://oliviergaudet.ca">Mado</a>')