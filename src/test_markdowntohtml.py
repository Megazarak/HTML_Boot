'''
import unittest
from markdowntohtml import markdown_to_html_node
from parentnode import ParentNode
from leafnode import LeafNode

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraph(self):
        md = "This is **bold** and _italic_ text."
        node = markdown_to_html_node(md)
        result = node.to_html()
        self.assertEqual(result, "<div><p>This is <b>bold</b> and <i>italic</i> text.</p></div>")

    def test_heading(self):
        md = "## This is a heading"
        node = markdown_to_html_node(md)
        result = node.to_html()
        self.assertEqual(result, "<div><h2>This is a heading</h2></div>")

    def test_unordered_list(self):
        md = "- Item 1\n- Item 2\n- Item 3"
        node = markdown_to_html_node(md)
        result = node.to_html()
        self.assertEqual(result, "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>")

    def test_code_block(self):
        md = "```\nCode block content\n```"
        node = markdown_to_html_node(md)
        result = node.to_html()
        self.assertEqual(result, "<div><pre><code>Code block content\n</code></pre></div>")

    def test_quote_block(self):
        md = "> This is a _quote_ with **bold** text."
        node = markdown_to_html_node(md)
        result = node.to_html()
        self.assertEqual(result, "<div><blockquote>This is a <i>quote</i> with <b>bold</b> text.</blockquote></div>")
   
if __name__ == "__main__":
    unittest.main()
'''