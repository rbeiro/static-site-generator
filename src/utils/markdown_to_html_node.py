from typing import List
from htmlnode import HTMLNode, ParentNode
from leafnode import LeafNode
from textnode import text_node_to_html_node
from utils.block_markdown import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
)
from utils.extract_markdown import text_to_textnodes


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    html_blocks = []
    for block in blocks:
        html_block = block_to_html(block)
        html_blocks.append(html_block)
    return ParentNode("div", html_blocks)

def block_to_html(block: str):
    block_type = block_to_block_type(block)
    html_tag: str | None = None

    text: str | None = None
    lines = block.split("\n")

    match block_type:
        case BlockType.PARAGRAPH:
            text = " ".join(lines)
            html_tag = "p"

        case BlockType.HEADING:
            heading_size = get_heading_size(block)
            html_tag = f"h{heading_size}"
            text = block[heading_size + 1 :]

        case BlockType.CODE:
            clean_lines = []
            for line in lines:
                if line.strip() != "```" and len(line) > 1:
                    clean_lines.append(line.strip())
            text = "\n".join(clean_lines) + "\n"
            html_tag = "pre"

        case BlockType.QUOTE:
            clean_lines = []
            for line in lines:
                clean_lines.append(line.lstrip(">").strip())
            text = " ".join(clean_lines)
            html_tag = "blockquote"

        case BlockType.ULIST:
            clean_lines = []
            for line in lines:
                clean_lines.append(line[2:])
            text = "\n".join(clean_lines)
            html_tag = "ul"
        case BlockType.OLIST:
            clean_lines = []
            for line in lines:
                clean_lines.append(line[3:])
            text = "\n".join(clean_lines)
            html_tag = "ol"

        case _:
            raise ValueError("invalid block")

    children: None | List[HTMLNode] | LeafNode = None

    if block_type == BlockType.CODE:
        children = [LeafNode("code", text)]
    elif block_type == BlockType.ULIST or block_type == BlockType.OLIST:
        children = text_to_list_items(text)
    else:
        children = text_to_children(text)

    return ParentNode(html_tag, children, None)

def text_to_list_items(text):
    text_list_items = text.split("\n")
    list_items = []
    for li in text_list_items:

        children = text_to_children(li)
        if len(children) > 1:
            list_items.append(ParentNode("li", children))
        else:
            list_items.append(LeafNode("li", li))
    return list_items

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    html_nodes = []

    for text_node in textnodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes


def get_heading_size(block: str) -> int:
    heading_size = 0

    for l in block:
        if l == "#":
            heading_size += 1
            continue
        break

    return heading_size
