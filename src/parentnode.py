from htmlnode import HTMLNode # import parent class

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, "", children, props)
        if tag is None or children is None:
            raise ValueError("ParentNode must have a tag and children")

    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag.")
        elif not self.children:
            return f"<{self.tag}></{self.tag}>"
        if self.props is not None:
            props_string = super().props_to_html()
            final_html = f"<{self.tag}{props_string}>"
        else:
            final_html = f"<{self.tag}>"
        
        # Base case: If a child is a LeafNode, its to_html() does not recurse.
        # Recursive case: If a child is a ParentNode, its to_html() calls its children.
        children_html = "".join(child.to_html() for child in self.children)
        
        final_html += f"{children_html}</{self.tag}>" 
        return final_html