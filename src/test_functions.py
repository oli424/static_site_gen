import unittest

from functions import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_plain_text(self):
        node = TextNode("This is plain text", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [TextNode("This is plain text", TextType.TEXT)])
        self.assertEqual(split_nodes_delimiter([node], "__", TextType.ITALIC), [TextNode("This is plain text", TextType.TEXT)])
    
    def test_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), [TextNode("This is text with a ", TextType.TEXT),
                                                                             TextNode("code block", TextType.CODE),
                                                                             TextNode(" word", TextType.TEXT)])
                                                                         
    def test_bold(self):
        node = TextNode("This is text with a **bold phrase** in the middle", TextType.BOLD)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [TextNode("This is text with a ", TextType.TEXT),
                                                                              TextNode("bold phrase", TextType.BOLD),
                                                                              TextNode(" in the middle", TextType.TEXT)])
    def test_full_node_delimited(self):
        node = TextNode("**This entire text is bold**", TextType.BOLD)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [TextNode("This entire text is bold", TextType.BOLD)])

    def test_open_ended_delimiter(self):
        node = TextNode("This text has an open **bold delimiter, which raise the invalid syntax exception", TextType.BOLD)
        node1 = TextNode("**This is open ended from the start", TextType.BOLD)
        try:
            split_nodes_delimiter([node], "**", TextType.BOLD)
            split_nodes_delimiter([node1], "**", TextType.BOLD)
        except Exception as e:
            self.assertRaises(Exception)