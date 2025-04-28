import unittest
from textnode import TextNode, TextType
from nodesplitter import *  
class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_no_delimiter(self):
        # Test case with no delimiter present
        node = TextNode("Plain text with no delimiter", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Plain text with no delimiter")
        self.assertEqual(result[0].text_type, TextType.TEXT)
    
    def test_one_delimiter_pair(self):
        # Test with one pair of delimiters
        node = TextNode("Text with `code block` in it", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Text with ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "code block")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " in it")
        self.assertEqual(result[2].text_type, TextType.TEXT)
    
    def test_multiple_delimiter_pairs(self):
        # Test with multiple pairs of delimiters
        node = TextNode("Text with `one code` and `another code` block", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_bold_delimiter(self):
        # Test with bold delimiters
        node = TextNode("Text with **bold text** in it", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Text with ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold text")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " in it")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_italic_delimiter(self):
        # Test with italic delimiters
        node = TextNode("Text with _italic text_ in it", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Text with ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "italic text")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, " in it")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.testsite.com)"
        )
        self.assertListEqual([("link", "https://www.testsite.com")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.imgur.com/) and another [second link](https://www.imgur.com/)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.imgur.com/"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.imgur.com/"
                ),
            ],
            new_nodes,
        )
    
    def test_empty_text_image(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_no_images(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_consecutive_links(self):
        node = TextNode(
            "Check [first](https://example.com)[second](https://example.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        # Expected result with appropriate assertions

    def test_image_at_start(self):
        node = TextNode(
            "![image](https://example.com/img.jpg) followed by text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        # Expected result with appropriate assertions

    def test_link_at_end(self):
        node = TextNode(
            "Text followed by [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        # Expected result with appropriate assertions

    def test_malformed_image(self):
        node = TextNode(
            "This has a ![broken image(https://example.com/img.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        # The malformed image shouldn't be extracted
        self.assertListEqual([node], new_nodes)

    def test_invalid_url_link(self):
        node = TextNode(
            "This has a [link with spaces](https://example.com/path with spaces)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        # Test the behavior with spaces in URL

    def test_multiple_input_nodes(self):
        node1 = TextNode("Text with [link](https://example.com)", TextType.TEXT)
        node2 = TextNode("More text with [another](https://example.org)", TextType.TEXT)
        new_nodes = split_nodes_link([node1, node2])
        # Test that both nodes are processed correctly

    def test_non_text_node(self):
        node = TextNode("This is bold", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        # Should return the original node unchanged
        self.assertListEqual([node], new_nodes)

    def test_text_to_textnodes(self):
        # Test 1: Basic text without any markdown
        text1 = "Just plain text"
        expected1 = [TextNode("Just plain text", TextType.TEXT)]
        assert text_to_textnodes(text1) == expected1
        
        # Test 2: Bold text
        text2 = "This is **bold** text"
        expected2 = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        assert text_to_textnodes(text2) == expected2
        
        # Test 3: Italic text
        text3 = "This is _italic_ text"
        expected3 = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        assert text_to_textnodes(text3) == expected3
        
        # Test 4: Code blocks
        text4 = "This is `code` text"
        expected4 = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT)
        ]
        assert text_to_textnodes(text4) == expected4
        
        # Test 5: Links
        text5 = "This is a [link](https://boot.dev) text"
        expected5 = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" text", TextType.TEXT)
        ]
        assert text_to_textnodes(text5) == expected5
        
    # Test 6: Images
    text6 = "This is an ![image](https://example.com/img.jpg) text"
    expected6 = [
        TextNode("This is an ", TextType.TEXT),
        TextNode("image", TextType.IMAGE, "https://example.com/img.jpg"),
        TextNode(" text", TextType.TEXT)
    ]
    assert text_to_textnodes(text6) == expected6
    
    # Test 7: Multiple formatting in one text
    text7 = "**Bold** and _italic_ and `code`"
    expected7 = [
        TextNode("Bold", TextType.BOLD),
        TextNode(" and ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" and ", TextType.TEXT),
        TextNode("code", TextType.CODE)
    ]
    assert text_to_textnodes(text7) == expected7
    
    # Test 8: Nested delimiters (though not supported in our parser)
    text8 = "This **bold _should not be italic_**"
    expected8 = [
        TextNode("This ", TextType.TEXT),
        TextNode("bold _should not be italic_", TextType.BOLD)
    ]
    assert text_to_textnodes(text8) == expected8
    
    # Test 9: Empty string
    text9 = ""
    expected9 = []
    assert text_to_textnodes(text9) == expected9

    # Test 10: The example from the assignment
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    expected = [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
    ]
    assert text_to_textnodes(text) == expected