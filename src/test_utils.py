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


    def test_image_ult(self):
        nodes =  [TextNode('This is ', TextType.TEXT), TextNode('text', TextType.BOLD), TextNode(' with an ', TextType.TEXT), TextNode('italic', TextType.ITALIC), TextNode(' word and a ', TextType.TEXT), TextNode('code block', TextType.CODE), TextNode(' and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)', TextType.TEXT)] 

        result = [TextNode('This is ', TextType.TEXT), TextNode('text', TextType.BOLD), TextNode(' with an ', TextType.TEXT), TextNode('italic', TextType.ITALIC), TextNode(' word and a ', TextType.TEXT), TextNode('code block', TextType.CODE), TextNode(' and an ', TextType.TEXT), TextNode('obi wan image', TextType.IMAGE, 'https://i.imgur.com/fJRm4Vk.jpeg'), TextNode(' and a [link](https://boot.dev)', TextType.TEXT)] 

        self.assertEqual(result, split_nodes_image(nodes))

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([TextNode("text", TextType.BOLD), node])

        self.assertListEqual(
            [
                TextNode("text", TextType.BOLD),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes
        )


    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([TextNode("text", TextType.BOLD), node, TextNode("text", TextType.BOLD)])

        self.assertListEqual(
            [
                TextNode("text", TextType.BOLD),
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT), 
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode("text", TextType.BOLD)
            ],
            new_nodes
        )

    def test_all_split(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = [
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
                ]
        actual = text_to_textnodes(text) 
        self.assertEqual(result, actual)


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

    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Final Level"), BlockType.HEADING)

    def test_code_block(self):
        block = '```print("Hello")```'
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> This is a quote\n> Second line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_broken_ordered_list(self):
        block = "1. First\n3. Second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)  # fails sequence

    def test_paragraph(self):
        block = "This is a simple paragraph.\nWith two lines."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
