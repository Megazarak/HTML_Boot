from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    return_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            return_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        # If there's an even number of parts, we have unmatched delimiters
        # (Think about it: text`code`more = ["text", "code", "more"] - 3 parts, odd number)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown: unmatched delimiter")
        
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            # if index is even, it's regular text
            if i % 2 == 0:
                return_nodes.append(TextNode(parts[i], TextType.TEXT))
            # if inde is odd, it's the special text type
            else: 
                return_nodes.append(TextNode(parts[i], text_type))
        
    return return_nodes

def extract_markdown_images(text):
    #regex pattern 
    #alt text = ![text]
    #link = (https://...)
    #re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)")
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    #regex pattern 
    #anchor text = [text]
    #link = (https://...)
    #re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)")
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    return_nodes = []
    for node in old_nodes:
        if extract_markdown_images(node.text) == []:
            return_nodes.append(node)
            continue
        elif node.text == "":
            continue
        
        text_extract = node.text
        images = extract_markdown_images(node.text)

        for image_alt, image_url in images:
            #split usin the image markdown
            image_markdown = f"![{image_alt}]({image_url})"
            parts = text_extract.split(image_markdown, 1)

            if parts[0]:
                return_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            return_nodes.append(TextNode(image_alt,TextType.IMAGE, image_url))

            if len(parts) > 1:
                text_extract  = parts[1]
            else:
                text_extract = ""
            
        if text_extract:
            return_nodes.append(TextNode(text_extract,TextType.TEXT))

    return return_nodes

def split_nodes_link(old_nodes):

    return_nodes = []
    for node in old_nodes:
        if extract_markdown_links(node.text) == []:
            return_nodes.append(node)
            continue
        elif node.text == "":
            continue
        
        text_extract = node.text
        links = extract_markdown_links(node.text)

        for link_href, link_url in links:
            #split usin the image markdown
            link_markdown = f"[{link_href}]({link_url})"
            parts = text_extract.split(link_markdown, 1)

            if parts[0]:
                return_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            return_nodes.append(TextNode(link_href,TextType.LINK, link_url))

            if len(parts) > 1:
                text_extract  = parts[1]
            else:
                text_extract = ""
            
        if text_extract:
            return_nodes.append(TextNode(text_extract,TextType.TEXT))

    return return_nodes

def text_to_textnodes(text):
    # Start with a single node containing all the text
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Apply each splitting function in order
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

if __name__ == "__main__":
    node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    new_nodes_link = text_to_textnodes(node)
    print(new_nodes_link)