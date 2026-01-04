import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image, text_to_textnodes
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_plain_text(self):
        node = TextNode("This is plain text", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD),
                            [TextNode("This is plain text", TextType.TEXT)]
                        )
        self.assertEqual(split_nodes_delimiter([node], "__", TextType.ITALIC), 
                            [TextNode("This is plain text", TextType.TEXT)]
                        )
    
    def test_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE),
                            [TextNode("This is text with a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" word", TextType.TEXT)]
                        )
                                                                         
    def test_bold(self):
        node = TextNode("This is text with a **bold phrase** in the middle", TextType.BOLD)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD),
                            [TextNode("This is text with a ", TextType.TEXT),
                            TextNode("bold phrase", TextType.BOLD),
                            TextNode(" in the middle", TextType.TEXT)]
                        )
        
    def test_full_node_delimited(self):
        node = TextNode("**This entire text is bold**", TextType.BOLD)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD),
                            [TextNode("This entire text is bold", TextType.BOLD)]
                        )

    def test_open_ended_delimiter(self):
        node = TextNode("This text has an open **bold delimiter, which raise " \
                        "the invalid syntax exception", TextType.BOLD)
        node1 = TextNode("**This is open ended from the start", TextType.BOLD)
        try:
            split_nodes_delimiter([node], "**", TextType.BOLD)
            split_nodes_delimiter([node1], "**", TextType.BOLD)
        except Exception as e:
            self.assertRaises(Exception)


class TextExtractMarkdownImages(unittest.TestCase):

    def test_no_image(self):
        text = "This text has to image"
        self.assertEqual(extract_markdown_images(text), [])
    
    def test_images_tuple_list(self):
        text = "This is a text with a ![rick roll](https://i.imgur.com/aKa0qIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [('rick roll', 'https://i.imgur.com/aKa0qIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')])


class TestExtractMarkdownLinks(unittest.TestCase):

    def test_no_link(self):
        text = "This text has no link"
        self.assertEqual(extract_markdown_links(text), [])

    def test_links_tuple_list(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])


class TestSplitNodesLink(unittest.TestCase):

    def test_split_link(self):
        node = [TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT), TextNode("This is another text with a link: [link](url)", TextType.TEXT)]
        new_nodes = split_nodes_link(node)
        self.assertListEqual([
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            TextNode("This is another text with a link: ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url")
            ], new_nodes
        )

    def test_link_first(self):
        node = TextNode("[link](url) this text starts with a link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("link", TextType.LINK, "url"),
            TextNode(" this text starts with a link", TextType.TEXT)
        ], new_nodes)

    def test_link_last(self):
        node = TextNode("This text ends with a link [link](url)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This text ends with a link ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url")
            ], new_nodes)
        
    def test_only_link(self):
        node = TextNode("[link](url)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("link", TextType.LINK, "url")], new_nodes)

    def test_no_link(self):
        node = TextNode("This text has no link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This text has no link", TextType.TEXT)], new_nodes)

    def test_back_to_back_images(self):
        node = TextNode("[link1](url1)[link2](url2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("link1", TextType.LINK, "url1"),
            TextNode("link2", TextType.LINK, "url2")
        ], new_nodes)

    def test_already_image_type(self):
        node = TextNode("link", TextType.LINK, "url")
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

class TestSplitNodesImage(unittest.TestCase):

    def test_split_image(self):
        node = [TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT), TextNode("This is another text with another image: ![image](url)", TextType.TEXT)]
        new_nodes = split_nodes_image(node)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode("This is another text with another image: ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "url")
            ],
            new_nodes
        )

    def test_image_first(self):
        node = TextNode("![image](url) This text starts with an image", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "url"),
                TextNode(" This text starts with an image", TextType.TEXT),
            ], new_nodes)

    def test_image_last(self):
        node = TextNode("This text ends with an image ![image](url)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This text ends with an image ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "url")
            ], new_nodes)

    def test_only_image(self):
        node = TextNode("![image](url)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("image", TextType.IMAGE, "url")], new_nodes)

    def test_no_image(self):
        node = TextNode("This text has no image", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This text has no image", TextType.TEXT)], new_nodes)

    def test_back_to_back_images(self):
        node = TextNode("![image1](url)![image2](url)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("image1", TextType.IMAGE, "url"),
            TextNode("image2", TextType.IMAGE, "url")
        ], new_nodes)

    def test_already_image_type(self):
        node = TextNode("image", TextType.IMAGE, "url")
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)


class TestMixedNodes(unittest.TestCase):

    def test_mixed_input_list(self):
        nodes = [
            TextNode("This is plain text", TextType.TEXT),
            TextNode("This is an image: ![image](url)", TextType.TEXT),
            TextNode("This text has a link: [link](url)", TextType.TEXT),
            TextNode("this is already an image", TextType.IMAGE, "url"),
            TextNode("this is already a link", TextType.LINK, "url"),
            TextNode("This text has an image: ![image](url) and a link [link](url)", TextType.TEXT),
        ]
        split_image_and_link = split_nodes_link(split_nodes_image(nodes))

        self.assertListEqual([
            TextNode("This is plain text", TextType.TEXT),
            TextNode("This is an image: ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url"),
            TextNode("This text has a link: ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode("this is already an image", TextType.IMAGE, "url"),
            TextNode("this is already a link", TextType.LINK, "url"),
            TextNode("This text has an image: ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url"),
            TextNode(" and a link ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
        ], split_image_and_link)


class TestTextToTextNodes(unittest.TestCase):

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ], new_nodes)