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
                case "`":
                    new_nodes.append(type(node)(part, TextType.CODE, node.url))
                case _:
                    raise Exception(f"Unsupported delimiter: {delimiter}, invalid markdown syntax")
    return new_nodes