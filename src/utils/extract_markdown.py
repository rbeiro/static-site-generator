import re

from textnode import TextNode, TextType
from utils.block_markdown import markdown_to_blocks
from utils.split_nodes_delimiter import split_nodes_delimiter


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def extract_title(markdown: str):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        title = search_block_for_title(block)
        if title:
            return title

    raise Exception("invalid markdown, missing title with h1 tag")


def search_block_for_title(block: str):
    lines = block.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
        return None

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images_data = extract_markdown_images(node.text)
        remaining_text = node.text

        for data in images_data:
            sections = remaining_text.split(f"![{data[0]}]({data[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            remaining_text = sections[1]
            new_nodes.append(TextNode(data[0], TextType.IMAGE, data[1]))

        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        link_data = extract_markdown_links(node.text)
        remaining_text = node.text

        for index, data in enumerate(link_data):
            sections = remaining_text.split(f"[{data[0]}]({data[1]})", 1)
            if len(sections) != 2:
                raise ValueError()
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            remaining_text = sections[1]
            new_nodes.append(TextNode(data[0], TextType.LINK, data[1]))

        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes
