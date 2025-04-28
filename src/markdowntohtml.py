from markdownblocks import *
from parentnode import *
from leafnode import *
from textnode import *
import re

BLOCK_TYPE_TO_TAG = {
    'PARAGRAPH': 'p',
    'HEADING': 'h',
    'UNORDERED_LIST': 'ul',
    'ORDERED_LIST': 'ol',
    'LIST_ITEM': 'li',
    'QUOTE': 'blockquote',
    'CODE': 'pre',
    # Add more mappings as needed
}

def to_blocks(markdown):
    return markdown_to_blocks(markdown)

def extract_text_from_block(block):
    # Use regex to strip out markdown syntax: **bold**, _italic_, `code`
    stripped_text = re.sub(r'(\*\*|__|`|_|\n)', '', block)
    #(\*\*|__||_|\n)`:
    #Matches any markdown-style symbols: **, __, _, \`` (inline code), or \n` (newlines).
    return stripped_text.strip()

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.BOLD:
        # Bold becomes a <b> leaf node
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        # Italic becomes an <i> leaf node
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        # Inline code becomes a <code> leaf node
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.TEXT:
        # Plain text becomes a raw LeafNode with no tag
        return LeafNode(tag=None, value=text_node.text)
      
def text_to_children(text):
    children = []  # This will store `ParentNode` or `LeafNode` elements.

    # Split the input text into lines for processing.
    lines = text.split("\n")
    blockquote_lines = []  # We'll use this to handle multi-line blockquotes.
    processing_blockquote = False

    for line in lines:
        line = line.strip()
        
        if line.startswith(">"):
            # Found the start of a blockquote.
            blockquote_lines.append(line[1:].strip())  # Strip the starting `>` and surrounding whitespace.
            processing_blockquote = True

        else:
            if processing_blockquote:
                # We've reached the end of a blockquote section.
                blockquote_text = " ".join(blockquote_lines)
                blockquote_children = parse_inline_markdown(blockquote_text)
                blockquote_node = ParentNode(tag="blockquote", children=blockquote_children)
                children.append(blockquote_node)
                blockquote_lines = []  # Reset for the next blockquote section.
                processing_blockquote = False

            # Parse non-blockquote lines for inline markdown directly.
            inline_children = parse_inline_markdown(line)
            if inline_children:
                children.extend(inline_children)

    # Handle any remaining blockquote lines if text ends with a quote.
    if blockquote_lines:
        blockquote_text = " ".join(blockquote_lines)
        blockquote_children = parse_inline_markdown(blockquote_text)
        blockquote_node = ParentNode(tag="blockquote", children=blockquote_children)
        children.append(blockquote_node)

    return children

def parse_inline_markdown(text):
    children = []  # This will store LeafNode instances.
    i = 0

    while i < len(text):
        if text[i:i+2] == "**":  # Bold text (**bold**)
            i += 2  # Skip the opening `**`
            closing_idx = text.find("**", i)
            if closing_idx != -1:
                bold_text = text[i:closing_idx]
                children.append(LeafNode(tag="b", value=bold_text))  # Add a bold <b> LeafNode
                i = closing_idx + 2  # Skip the closing `**`
                continue
        elif text[i] == "_":  # Italic text (_italic_)
            i += 1  # Skip opening `_`
            closing_idx = text.find("_", i)
            if closing_idx != -1:
                italic_text = text[i:closing_idx]
                children.append(LeafNode(tag="i", value=italic_text))  # Add an italic <i> LeafNode
                i = closing_idx + 1  # Skip the closing `_`
                continue
        elif text[i] == "`":  # Inline code (`code`)
            i += 1  # Skip opening backtick.
            closing_idx = text.find("`", i)
            if closing_idx != -1:
                code_text = text[i:closing_idx]
                children.append(LeafNode(tag="code", value=code_text))  # Add a <code> LeafNode
                i = closing_idx + 1  # Skip the closing backtick.
                continue
        else:  # Plain text (no markdown syntax)
            plain_start = i  # Mark where the plain text starts.
            while i < len(text) and text[i] not in "*_`":  # Scan until encountering markdown syntax.
                i += 1
            plain_text = text[plain_start:i]  # Extract the plain text.
            if plain_text:  # Only add text nodes if there's actual text.
                children.append(LeafNode(tag="span", value=plain_text))  # Add as a <span> LeafNode.

    return children

def parse_list_items(block):
    """
    Parses a list block and returns a list of `HTMLNode` objects (one for each list item).
    Example:
    "- Item 1\n- Item 2" -> [HTMLNode(tag='li', children=[TextNode("Item 1")]),
                              HTMLNode(tag='li', children=[TextNode("Item 2")])]
    """
    list_item_nodes = []
    # Split the block into individual lines, each representing a list item
    lines = block.split("\n")
    
    for line in lines:
        # Use a regex to strip out the leading list markers (-, *, or digits with a period)
        item_match = re.match(r"^\s*[-*]\s+(.*)|^\s*\d+\.\s+(.*)", line)
        if item_match:
            # Depending on the type of match, get the relevant text
            item_text = item_match.group(1) or item_match.group(2)

            # Convert the list item text into child nodes using the helper
            child_nodes = text_to_children(item_text)  # Inline parsing for bold/italic/code
            # Create a new <li> node for this list item
            li_node = ParentNode(tag="li", children=child_nodes)
            list_item_nodes.append(li_node)

    return list_item_nodes

def markdown_to_html_node(markdown):
    '''
    quote <blockquote>
    unordered list <ul> each item w/ <li>
    ordered list <ol> each item w/ <li>
    code <pre><code></code></pre>
    heading <h1>...<h6> depending on num of #
    paragrapph <p>
    '''
    # set up root node
    root_node = ParentNode(tag='div', children=[])
    
    # split markdown into blocks
    blocks = to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        block_tag = BLOCK_TYPE_TO_TAG.get(block_type.value)
        print(f"{block_tag} | {block_type}")
        if block_tag:

            if block_type.value == 'PARAGRAPH':
                block_text = extract_text_from_block(block)
                # Parse inline markdown
                child_nodes = text_to_children(block_text)  # Multiple children (bold, italics, etc.)
                block_node = ParentNode(tag="p", children=child_nodes)  # Paragraph is a parent element
                root_node.children.append(block_node)

            elif block_type.value == "QUOTE":
                block_text = extract_text_from_block(block)
                # Parse inline markdown for quoted text
                child_nodes = text_to_children(block_text)
                block_node = ParentNode(tag="blockquote", children=child_nodes)
                root_node.children.append(block_node)

            elif block_type.value == "CODE":
                # Keep code block content literal
                block_text = block.strip("`").strip("\n") + "\n"                
                # Create a LeafNode for the <code> content (literal text)
                code_node = LeafNode(tag="code", value=block_text)

                # Wrap the <code> node in a ParentNode for <pre>
                block_node = ParentNode(tag="pre", children=[code_node])
                # Append the <pre> block to the root node
                root_node.children.append(block_node)
            
            elif block_type.value == "HEADING":
                # Extract heading level from the number of #
                match = re.match(r"^(#+)\s+(.*)", block)  # Match heading syntax, e.g. ### Heading
                if match:
                    heading_level = min(len(match.group(1)), 6)  # Limit to <h6> maximum
                    block_text = match.group(2).strip()  # Extract the text of the heading

                    # Create <hN> node where N is the heading level
                    child_nodes = text_to_children(block_text)  # Parse inline markdown for children
                    block_node = ParentNode(tag=f"h{heading_level}", children=child_nodes)

                    # Add the heading node to the root node
                    root_node.children.append(block_node)
                        
            elif block_type.value in ["UNORDERED_LIST", "ORDERED_LIST"]:
                # Determine list type: <ul> for unordered, <ol> for ordered
                list_tag = "ul" if block_type == "UNORDERED_LIST" else "ol"

                # Parse the list items into child nodes
                list_items = parse_list_items(block)  # Returns a list of ParentNode or LeafNode objects

                # Create the list parent node (<ul> or <ol>) and append the items
                block_node = ParentNode(tag=list_tag, children=list_items)

                # Append the list node to the root
                root_node.children.append(block_node)
            
    return root_node

if __name__ == "__main__":
    md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

    node = markdown_to_html_node(md)
    html = node.to_html()
    #print(result)

    md = "- Item 1\n- Item 2\n- Item 3"
    node = markdown_to_html_node(md)
    result = node.to_html()
    #print(result)

    md = "```\nCode block content\n```"
    node = markdown_to_html_node(md)
    result = node.to_html()
    #print(result)

    md = "> This is a _quote_ with **bold** text."
    node = markdown_to_html_node(md)
    result = node.to_html()
    print(result)
