from leafnode import LeafNode
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter:str, text_type:TextType) -> list:
    result = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            for index, text in enumerate(node.text.split(delimiter)):
                if text == '':
                    continue

                if index % 2 == 0:
                    result.append(TextNode(text, TextType.TEXT))
                else:
                    result.append(TextNode(text, text_type))
        else:
            result.append(node)
            
    return result
            

def text_node_to_html_node(node:TextNode) -> LeafNode:
        match node.text_type:
            case TextType.TEXT:
                return LeafNode(None, node.text)
            case TextType.BOLD:
                return LeafNode('b', node.text)
            case TextType.ITALIC:
                return LeafNode('i', node.text)
            case TextType.CODE:
                return LeafNode('code', node.text)
            case TextType.LINK:
                return LeafNode('a', node.text, {'href': node.url})
            case TextType.IMAGE:
                return LeafNode('img', '', {'src': node.url, 'alt': node.text})
            
        raise ValueError('Wrong TextType')