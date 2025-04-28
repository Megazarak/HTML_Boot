from htmlnode import HTMLNode # import parent class

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        # call parent constructor and set children to None (a quality of a leaf)
        super().__init__(tag, value, None, props)
        if value is None:
            raise ValueError("LeafNode must have a value")

    def to_html(self):
        # all leaf nodes need a value
        if self.value is None:
            raise ValueError
        elif self.tag is None:
            return self.value
        
        if self.props is None:
            return f"<{self.tag}>{self.value}<{self.tag}/>"

        props_string = super().props_to_html()
        return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"