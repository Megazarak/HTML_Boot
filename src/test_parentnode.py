from parentnode import ParentNode
from leafnode import LeafNode
import unittest

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_no_children(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", None)
        self.assertEqual(
            str(context.exception), "ParentNode must have a tag and children"
         )
        
    def test_to_html_multiple_children(self):
        child1 = LeafNode("b", "Bold text")
        child2 = LeafNode(None, "TEXT text")
        parent_node = ParentNode("p", [child1, child2])
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>TEXT text</p>"
        )

    def test_to_html_deeply_nested(self):
        grandchild = LeafNode("i", "Italic text")
        child = ParentNode("span", [grandchild])
        parent = ParentNode("div", [child])
        self.assertEqual(
            parent.to_html(),
            "<div><span><i>Italic text</i></span></div>"
        )

    def test_to_html_no_tag(self):
        with self.assertRaises(ValueError) as context:
            ParentNode(None, [LeafNode("span", "child")])
        self.assertEqual(
            str(context.exception), "ParentNode must have a tag and children"
        )

    def test_to_html_empty_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")