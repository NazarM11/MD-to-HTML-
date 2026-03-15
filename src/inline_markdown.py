import re
from textnode import *

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    return_list = []
    for node in old_nodes:  
        if len(extract_markdown_images(node.text)) == 0:
            return_list.append(node)
            continue
        imgs = extract_markdown_images(node.text)
        original_text = node.text
        for img in imgs: 
            sections = original_text.split(f"![{img[0]}]({img[1]})", 1)
            if sections[0] != "":
                return_list.append(TextNode(sections[0], TextType.TEXT))
            return_list.append(TextNode(img[0], TextType.IMAGE, img[1]))
            original_text = sections[1]
        if original_text != "":
            return_list.append(TextNode(original_text, TextType.TEXT))
    return return_list

def split_nodes_link(old_nodes):
    return_list = []
    for node in old_nodes:  
        if len(extract_markdown_links(node.text)) == 0:
            return_list.append(node)
            continue
        links = extract_markdown_links(node.text)
        original_text = node.text
        for link in links: 
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if sections[0] != "":
                return_list.append(TextNode(sections[0], TextType.TEXT))
            return_list.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            return_list.append(TextNode(original_text, TextType.TEXT))
    return return_list

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            sections = old_node.text.split(delimiter)
            if len(sections) % 2 == 0:
                raise ValueError("invalid Markdown: missing closing delimiter")
            
            for i, str in enumerate(sections):
                if i % 2 == 0:
                    new_nodes.append(TextNode(str, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(str, text_type))
    return new_nodes

def text_to_textnodes(text):
    original_text = [TextNode(text, TextType.TEXT)]
    original_text = split_nodes_delimiter(original_text, "**", TextType.BOLD)
    original_text = split_nodes_delimiter(original_text, "_", TextType.ITALIC)
    original_text = split_nodes_delimiter(original_text, "`", TextType.CODE)
    original_text = split_nodes_image(original_text)
    original_text = split_nodes_link(original_text)  
    return original_text   