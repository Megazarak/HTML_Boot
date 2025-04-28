import unittest
import os
import shutil

from markdown_blocks import (
    markdown_to_html_node,
    markdown_to_blocks,
    block_to_block_type,
    extract_title,
    generate_page,
    BlockType,
)


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

def test_extract_title():
    assert extract_title("# Hello") == "Hello"
    assert extract_title("#    Spaced Out Header   ") == "Spaced Out Header"

    try:
        extract_title("No header here")
        assert False, "Should raise an exception if no title is found!"
    except Exception:
        pass

def test_generate_page():
    # Input dummy markdown and template
    with open("dummy.md", "w") as f:
        f.write("# Test\nThis is a test page.")
    with open("dummy_template.html", "w") as f:
        f.write("<html><title>{{ Title }}</title><body>{{ Content }}</body></html>")

    # Output path
    dest_path = "output.html"

    generate_page("dummy.md", "dummy_template.html", dest_path)

    # Verify that the output HTML contains the right replacements
    with open(dest_path, "r") as f:
        result = f.read()
        assert "<title>Test</title>" in result
        assert "<body><h1>Test</h1>\n<p>This is a test page.</p></body>" in result

    # Clean up test files
    os.remove("dummy.md")
    os.remove("dummy_template.html")
    os.remove(dest_path)

def test_public_directory_cleanup():
    # Create a fake `public` directory with some dummy files
    if not os.path.exists("public"):
        os.makedirs("public")
    with open("public/dummy.txt", "w") as f:
        f.write("This is a test file.")

    # Run the cleanup and recreation logic
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.makedirs("public")

    # Confirm that `public` exists but no dummy file is present anymore
    assert os.path.exists("public")
    assert not os.path.exists("public/dummy.txt")

    # Clean up after the test
    shutil.rmtree("public")

if __name__ == "__main__":
    unittest.main()
