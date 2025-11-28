import re
from textnode import TextType, TextNode, TextDelimiter


def text_to_textnodes(text):
    old_node = [TextNode(text, TextType.TEXT)]
    new_nodes = []
    
    delimiters = []

    for delim in TextDelimiter:
        delimiters.extend(delim.value)

    for delimiter in delimiters:
        new_nodes = split_nodes_delimiter(old_node, delimiter, TextType.TEXT)
        old_node = new_nodes
        
    new_nodes = split_nodes_image(old_node)
    old_node = new_nodes
    new_nodes = split_nodes_link(old_node)
    return new_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # Only process nodes of the specified text_type
        if node.text_type != text_type:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        for i, part in enumerate(parts):
            if not part:
                raise Exception("Empty text node found")
            if i != 1:  # not the delimiter part
                new_nodes.append(type(node)(part, TextType.TEXT, node.url))
                continue

            for textDelimiter in TextDelimiter:
                if delimiter in textDelimiter.value:
                    name = textDelimiter.name
                    new_nodes.append(type(node)(part, TextType[name], node.url))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\]]+)\]\(([^\)]+)", text)

    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[([^\]]+)\]\(([^\)]+)", text)
    return matches