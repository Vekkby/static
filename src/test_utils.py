import unittest

from utils import *
from textnode import TextNode


class TestUtils(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_nodes_delimeter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        result = [
                       TextNode("This is text with a ", TextType.TEXT),
                       TextNode("code block", TextType.CODE),
                       TextNode(" word", TextType.TEXT)
                 ]
        
        self.assertEqual(new_nodes, result)

    def test_split_nodes_delimeter_multiple(self):
        node = TextNode("This is `text` with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        result = [
                       TextNode("This is ", TextType.TEXT),
                       TextNode("text", TextType.CODE),
                       TextNode(" with a ", TextType.TEXT),
                       TextNode("code block", TextType.CODE),
                       TextNode(" word", TextType.TEXT)
                 ]
        
        self.assertEqual(new_nodes, result)


    def test_split_nodes_delimeter_multiple_different(self):
        node = TextNode("This is `text` with a `**code block**` **word**", TextType.TEXT)
        new_nodes = split_nodes_delimiter(split_nodes_delimiter([node], "`", TextType.CODE), '**', TextType.BOLD)
        result = [
                       TextNode("This is ", TextType.TEXT),
                       TextNode("text", TextType.CODE),
                       TextNode(" with a ", TextType.TEXT),
                       TextNode("**code block**", TextType.CODE),
                       TextNode(" ", TextType.TEXT),
                       TextNode("word", TextType.BOLD)
                 ]
        
        self.assertEqual(new_nodes, result)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
                                          
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) ![image](https://i.imgur.com/zjjcJKZ2.png)")
                                          
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image", "https://i.imgur.com/zjjcJKZ2.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev)")
                                          
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
                                          
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_only_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_links(text)

        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_only_image(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


if __name__ == "__main__":
    unittest.main()
