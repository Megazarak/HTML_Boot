from htmlnode import HTMLNode

html_node = HTMLNode(tag="p", props={"id": "main"})
assert html_node.props_to_html() == ' id="main"'

html_node = HTMLNode(tag="p", props={"class": "highlight", "data-value": "42"})
assert html_node.props_to_html() == ' class="highlight" data-value="42"'

html_node = HTMLNode(tag="p", props={})
assert html_node.props_to_html() == ''

html_node = HTMLNode(tag="p", props={"onclick": "alert('hello')"})
assert html_node.props_to_html() == ' onclick="alert(\'hello\')"'
