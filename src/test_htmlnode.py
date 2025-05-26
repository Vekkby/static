import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_to_html(self):
        node= HTMLNode()
        
        self.assertRaises(NotImplementedError, node.to_html)

    def props_to_html(self):
        props = {'key': 'value', 'other_key': 'other_value'} 
        node = HTMLNode(props=props) 

        self.assertEqual(node, ' key=value other_key=other_value')

    def props_to_html_empty_dict(self):
        props = {} 
        node = HTMLNode(props=props) 

        self.assertEqual(node, '')

    def props_to_html_none_props(self): 
        node = HTMLNode() 

        self.assertEqual(node, '')


    def test_repr(self):
        tag = 'tag'
        value = 'value'
        children = [HTMLNode(), HTMLNode()]
        props = {'key': 'value', 'other_key': 'other_value'} 
        node = HTMLNode(tag, value, children, props)
        expected_result = f'HTMLNode({tag} {value} {children} {props})'

        self.assertEqual(str(node), expected_result)

if __name__ == "__main__":
    unittest.main()