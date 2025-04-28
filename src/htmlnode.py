

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag #representative of HTML tag names
        self.value = value #string value of the HTML tag
        self.children = children if children is not None else [] # a list of HTMLNode objects
        self.props = props if props is not None else {} # dictionary - attribute of the tag

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:  # Handle empty `props` gracefully
            return ''
        return ' ' + ' '.join(f'{key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"