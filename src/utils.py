import re
from textnode import TextType, TextNode

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

            match delimiter:
                case "**":
                    new_nodes.append(type(node)(part, TextType.BOLD, node.url))
                case "*":
                    new_nodes.append(type(node)(part, TextType.ITALIC, node.url))
                case "```":
                    new_nodes.append(type(node)(part, TextType.CODE, node.url))
                case "``":
                    new_nodes.append(type(node)(part, TextType.CODE, node.url))
                case _:
                    raise Exception(f"Unsupported delimiter: {delimiter}, invalid markdown syntax")
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_images(node.text)
        # if no matches, keep the node as is
        if len(matches) == 0 or len(matches[0]) == len(node.text):
            new_nodes.append(node)
            continue

        for matche in matches:
            text_split = node.text.split(f"![{matche[0]}]({matche[1]})", 1)
            for i, part in enumerate(text_split):
                if part:
                    new_nodes.extend(split_nodes_image([TextNode(part, TextType.TEXT)]))
                if i != len(text_split) - 1:
                    new_nodes.append(TextNode(matche[0], TextType.IMAGE, matche[1]))
            
    return new_nodes

def split_nodes_link(old_nodes):
    print()
    new_nodes = []
    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        # if no matches, keep the node as is
        if len(matches) == 0 or len(matches[0]) == len(node.text):
            new_nodes.append(node)
            continue

        for matche in matches:
            text_split = node.text.split(f"[{matche[0]}]({matche[1]})", 1)
            print(f"text_split: {text_split}")
            for i, part in enumerate(text_split):
                # if part == text_split[-1]:
                #    continue
                if i == len(text_split) - 1:
                    new_nodes.append(TextNode(matche[0], TextType.LINK, matche[1]))
                    new_nodes.append(TextNode(part, TextType.TEXT))
                    continue
                new_nodes.append(TextNode(part, TextType.TEXT))
    print(f"new_nodes: {new_nodes}")
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\]]+)\]\(([^\)]+)", text)

    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[([^\]]+)\]\(([^\)]+)", text)
    return matches