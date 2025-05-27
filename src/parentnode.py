from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str|None, children: list[HTMLNode], props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    
    def to_html(self) -> str:
        if self.tag in ['', None]:
            raise ValueError('Parent tag is missing')
        
        if self.children in [[], None]:
            raise ValueError('Children are missing')
        
        if any(map(lambda obj: not isinstance(obj, HTMLNode), self.children)):
            raise ValueError('Children are not HTMLNodes')
            
        return f'<{self.tag}{self.props_to_html()}>{''.join(map(lambda child: child.to_html(), self.children))}</{self.tag}>'