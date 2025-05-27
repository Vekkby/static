from leafnode import LeafNode
from textnode import TextNode, TextType
import re

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


def extract_markdown_images(text) -> list[tuple[str, str]|None]: 
    images_reg = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    
    return re.findall(images_reg, text)

    

def extract_markdown_links(text:str) -> list[tuple[str, str]|None]:
    links_reg = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

    return re.findall(links_reg, text)


def split_images_links(old_nodes, pattern, text_type, extraction_function):
    result = []

    for node in old_nodes: 
        if node.text_type == TextType.TEXT:
            matches:list[tuple[str, str] | None] = extraction_function(node.text)

            if matches == []:
                result.append(node)
                continue

            text_string:str = node.text

            for match in matches:
                delimiter = pattern.format(match[0], match[1])
                split = text_string.split(delimiter, 1)

                if split[0] != '':
                    result.append(TextNode(split[0], TextType.TEXT))


                result.append(TextNode(match[0], text_type, match[1]))

                if len(split) == 1:
                    text_string = ''
                    continue

                text_string = split[1]

            if text_string != '':
                result.append(TextNode(text_string, TextType.TEXT))
        else:
            result.append(node)

    return result


def split_nodes_image(old_nodes): 
    return split_images_links(old_nodes, "![{0}]({1})", TextType.IMAGE, extract_markdown_images)
  

def split_nodes_link(old_nodes):
    return split_images_links(old_nodes, "[{0}]({1})", TextType.LINK, extract_markdown_links)


def text_to_textnodes(text:str) -> list[TextNode | None]:
    result = [TextNode(text, TextType.TEXT)] 
    result = split_nodes_image(result) 
    result = split_nodes_link(result) 
    result = split_nodes_delimiter(result, '`', TextType.CODE)
    result = split_nodes_delimiter(result, '**', TextType.BOLD)
    result = split_nodes_delimiter(result, '_', TextType.ITALIC)

    return result
