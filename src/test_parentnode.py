import unittest

from leafnode import LeafNode
from parentnode import ParentNode

class TestTextNode(unittest.TestCase): 
    def test_no_children(self):
        node = ParentNode("p", [])
        self.assertRaises(ValueError, node.to_html)

    def test_none_children(self):
        node = ParentNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_wrong_children(self):
        node = ParentNode("p", ['NOT HTMLNODE'])
        self.assertRaises(ValueError, node.to_html)

    def test_empty_tag(self):
        node =  ParentNode(None, ['value'])
        self.assertRaises(ValueError, node.to_html)


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )