from leafnode import LeafNode
from textnode import TextNode, TextType
from htmlnode import HTMLNode
from parentnode import ParentNode
import re, os
from enum import Enum

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


def markdown_to_blocks(markdown:str) -> list:
    result = markdown.split("\n\n")

    if result in [[], ['']]:
        return []
    
    result = list(filter(lambda block: block != '', map(lambda block: block.strip(), result))) 

    return result

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'
    
    
def block_to_block_type(block:str) -> BlockType:
    if re.match(r"^(#{1,6})\s+(.*)$", block):
        return BlockType.HEADING
    if re.match(r"^```[\s\S]*?```$", block):
        return BlockType.CODE
    if re.match(r"^>", block):
        return BlockType.QUOTE
    if all(map(lambda line: bool(re.match(r"- ", line)), block.split("\n"))):
        return BlockType.UNORDERED_LIST
     
    numbers_list = [re.match(r"[0-9]+\. ", line) for line in block.split("\n")]
    if all(numbers_list):
        casted_numbers = list(map(lambda match: float(match.group(0)), numbers_list))
         
        if len(casted_numbers) == 1:
            return BlockType.ORDERED_LIST
        
        for pair in zip(casted_numbers[:-1], casted_numbers[1:]):
            if not pair[1] - pair[0] == 1:
                return BlockType.PARAGRAPH
        
        return BlockType.ORDERED_LIST
        

    
    return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown:str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    pairs = [(block, block_to_block_type(block)) for block in blocks]
    nodes = [block_to_node(pair) for pair in pairs]

    return ParentNode('div', nodes)


def block_to_node(pair:(str, BlockType)) -> HTMLNode:
    match pair[1]:
        case BlockType.PARAGRAPH:
            return ParentNode('p', list(map(text_node_to_html_node, text_to_textnodes(normalize_text(pair[0])))))
        case BlockType.CODE:
            text = re.findall(r"^```([\s\S]*?)```$", pair[0])[0].lstrip()

            return ParentNode('pre', [LeafNode('code', text)])
        case BlockType.QUOTE:
            return LeafNode('blockquote', pair[0][1:])
        case BlockType.HEADING:
            header = re.findall(r"^(#{1,6})", pair[0])[0]
            text = re.sub(r"^#{1,6}\s+", "", pair[0]).strip() 

            return LeafNode(f'h{len(header)}', text)
        case BlockType.UNORDERED_LIST:
            items = [item[2:] for item in pair[0].splitlines()]
            return ParentNode('ul', [LeafNode('li', (item)) for item in items])
        case BlockType.ORDERED_LIST:
            items = [re.sub(r"^[0-9]+\.\s", '', item) for item in pair[0].splitlines()]

            return ParentNode('ol', [LeafNode('li', item) for item in items])

        
    return HTMLNode()

def normalize_text(text:str) -> str:
    return ' '.join([line.strip() for line in text.strip().splitlines()])


def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if re.match(r"^#\s", line):
            return line[1:].strip()

    raise ValueError('No h1 header') 
