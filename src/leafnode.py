from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    
    def to_html(self) -> str:
        if self.value == None:
            raise ValueError('LeafNode value is missing')
        
        if self.tag in ['', None]:
            return self.value
        
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'