import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, 'some url')

        self.assertNotEqual(node, node2)

    def test_repr(self):
        text = "This is a text node"
        text_type = TextType.BOLD
        url = 'some url'
        node = TextNode(text, text_type, url)
        expected_result = f'TextNode({text}, {text_type.value}, {url})'

        self.assertEqual(str(node), expected_result)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()
