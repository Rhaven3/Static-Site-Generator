from enum import Enum
from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType (Enum): 
    PARAGRAPH = "paragraph"
    HEADING = "header"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    CODE_BLOCK = "code_block"
    BLOCKQUOTE = "blockquote"

class BlockDelimiter:
    HEADING = ["#", "##", "###", "####", "#####", "######"]
    UNORDERED_LIST = "- "
    ORDERED_LIST = "1. "
    CODE_BLOCK = "```"
    BLOCKQUOTE = "> "

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    body = ParentNode("div", [])
    subHtmlNodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.CODE_BLOCK:
                cParentNode = ParentNode("pre", [ParentNode("code", [LeafNode(None, block.split(BlockDelimiter.CODE_BLOCK)[1][1:])])])
                body.children.append(cParentNode)

            case BlockType.PARAGRAPH:
                pParentNode = ParentNode("p", [])
                textNodes = text_to_textnodes(block)
                subHtmlNodes = [text_node_to_html_node(tn) for tn in textNodes]
                for child in subHtmlNodes:
                    child.value = child.value.replace("\n", " ")
                pParentNode.children.extend(subHtmlNodes)
                body.children.append(pParentNode)

            case BlockType.BLOCKQUOTE:
                qParentNode = ParentNode("blockquote", [])
                textNodes = text_to_textnodes(block)
                subHtmlNodes = [text_node_to_html_node(tn) for tn in textNodes]
                for child in subHtmlNodes:
                    child.value = child.value.replace("> ", "")
                qParentNode.children.extend(subHtmlNodes)
                body.children.append(qParentNode)

            case BlockType.HEADING:
                textNodes = text_to_textnodes(block)
                subHtmlNodes = [text_node_to_html_node(tn) for tn in textNodes]
                headNumber = 1;
                for child in subHtmlNodes:
                    if BlockDelimiter.HEADING[5] in child.value:
                        headNumber = 6
                        child.value = child.value.replace(BlockDelimiter.HEADING[5]+" ", "")
                    elif BlockDelimiter.HEADING[4] in child.value:
                        headNumber = 5
                        child.value = child.value.replace(BlockDelimiter.HEADING[4]+" ", "")
                    elif BlockDelimiter.HEADING[3] in child.value:
                        headNumber = 4
                        child.value = child.value.replace(BlockDelimiter.HEADING[3]+" ", "")
                    elif BlockDelimiter.HEADING[2] in child.value:
                        headNumber = 3
                        child.value = child.value.replace(BlockDelimiter.HEADING[2]+" ", "")
                    elif BlockDelimiter.HEADING[1] in child.value:
                        headNumber = 2
                        child.value = child.value.replace(BlockDelimiter.HEADING[1]+" ", "")
                    else:
                        child.value = child.value.replace(BlockDelimiter.HEADING[0]+" ", "")
                hParentNode = ParentNode(f"h{headNumber}", [])
                hParentNode.children.extend(subHtmlNodes)
                body.children.append(hParentNode)

            case BlockType.UNORDERED_LIST:
                uParentNode = ParentNode("ul", [])
                subHtmlNodes = block.split(BlockDelimiter.UNORDERED_LIST)
                subHtmlNodes = subHtmlNodes[1:]
                
                newSubHtmlNodes = []
                for li in subHtmlNodes:
                    li = li.replace("\n", "")
                    liTextNodes = text_to_textnodes(li)
                    newli = []
                    for tn in liTextNodes:
                        newli.append(text_node_to_html_node(tn))
                    newSubHtmlNodes.append(ParentNode("li", newli))
                uParentNode.children.extend(newSubHtmlNodes)
                body.children.append(uParentNode)

            case BlockType.ORDERED_LIST:
                oParentNode = ParentNode("ol", [])
                subHtmlNodes = block.split("\n")
                
                newSubHtmlNodes = []
                for li in subHtmlNodes:
                    li = li[3:]
                    liTextNodes = text_to_textnodes(li)
                    newli = []
                    for tn in liTextNodes:
                        newli.append(text_node_to_html_node(tn))
                    newSubHtmlNodes.append(ParentNode("li", newli))
                oParentNode.children.extend(newSubHtmlNodes)
                body.children.append(oParentNode)
    return body

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(tuple(BlockDelimiter.HEADING)):
        return BlockType.HEADING

    if len(lines) > 1 and lines[0].startswith(tuple(BlockDelimiter.CODE_BLOCK)) and lines[-1].startswith(tuple(BlockDelimiter.CODE_BLOCK)):
        
        return BlockType.CODE_BLOCK
    
    if block.startswith(tuple(BlockDelimiter.BLOCKQUOTE)):
        for line in lines:
            if not line.startswith(tuple(BlockDelimiter.BLOCKQUOTE)):
                return BlockType.PARAGRAPH
        return BlockType.BLOCKQUOTE
    
    if block.startswith(BlockDelimiter.UNORDERED_LIST):
        for line in lines:
            if not line.startswith(BlockDelimiter.UNORDERED_LIST):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    if block.startswith(BlockDelimiter.ORDERED_LIST):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH