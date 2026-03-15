from enum import Enum
from markdown_to_blocks import *
from htmlnode import *
from inline_markdown import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    lines = block.split("\n")
    if len(lines) > 1:
        if lines[0].startswith("```") and lines[-1].strip().startswith("```"):
            return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1."):
        num = 1
        for line in lines: 
            if not line.startswith(f"{num}. "):
                return BlockType.PARAGRAPH
            else:
                num += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_children(text):
    nodes = text_to_textnodes(text)
    html_nodes = []
    for node in nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    transformed_blocks = []
    for block in blocks:
        if block_to_block_type(block) == BlockType.PARAGRAPH:
            new_block = " ".join(line.strip() for line in block.split("\n"))
            if new_block:
                transformed_blocks.append(ParentNode("p", text_to_children(new_block)))
        
        elif block_to_block_type(block) == BlockType.HEADING:
            i = block.count("#")
            new_block = block[i + 1:]
            transformed_blocks.append(ParentNode(f"h{i}", text_to_children(new_block)))
        
        elif block_to_block_type(block) == BlockType.CODE:
            lines = block[4:-4].split("\n")
            new_block = "\n".join(line.strip() for line in lines)
            code_node = text_node_to_html_node(TextNode(new_block, TextType.TEXT))
            code = ParentNode("code", [code_node])
            pre = ParentNode("pre", [code])
            transformed_blocks.append(pre)
        
        elif block_to_block_type(block) == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                parts = line.split(". ", 1)
                text = parts[1]
                new_lines.append(ParentNode("li", text_to_children(text)))
            transformed_blocks.append(ParentNode("ol", new_lines))
        
        elif block_to_block_type(block) == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                text = line[2:]
                new_lines.append(ParentNode("li", text_to_children(text)))
            transformed_blocks.append(ParentNode("ul", new_lines))
        
        elif block_to_block_type(block) == BlockType.QUOTE:
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                text = line.lstrip(">").strip()
                new_lines.append(text)
            content = " ".join(new_lines)
            transformed_blocks.append(ParentNode("blockquote", text_to_children(content)))
    return ParentNode("div", transformed_blocks)
            