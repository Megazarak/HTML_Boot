from leafnode import LeafNode

leaf_node = LeafNode(tag="p", value="This is text.", props={})
assert leaf_node.to_html() == "<p>This is text.</p>"

leaf_node = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})
assert leaf_node.to_html() == '<a href="https://www.google.com">Click me!</a>'

try:
    leaf_node = LeafNode(tag="p", value=None, props={})
    leaf_node.to_html()
    assert False, "Expected ValueError was not raised"
except ValueError:
# This is what we want
    pass