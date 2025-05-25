class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == None or self.props == {}:
            ''

        result = []
        for prop in self.props:
            result.append(f'{prop}="{self.props[prop]}"')
        return ' '.join(result)

    def __repr__(self):
        return f'HTMLNode({self.tag} {self.value} {self.children} {self.props})'
