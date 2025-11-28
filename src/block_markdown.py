from enum import Enum

class BlockType (Enum): 
    PARAGRAPH = "paragraph"
    HEADER = "header"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    CODE_BLOCK = "code_block"
    BLOCKQUOTE = "blockquote"

class BlockDelimiter:
    HEADER = ["#", "##", "###", "####", "#####", "######"]
    UNORDERED_LIST = ["- ", "* ", "+ "]
    ORDERED_LIST = ["1. "]
    CODE_BLOCK = ["```"]
    BLOCKQUOTE = ["> "]

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleaned_blocks = [block.strip() for block in blocks if block.strip() != ""]
    return cleaned_blocks   

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(BlockDelimiter.ORDERED_LIST[0]):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    if block.startswith(tuple(BlockDelimiter.HEADER)):
        return BlockType.HEADER

    if len(lines) > 1 and lines[0].startswith(tuple(BlockDelimiter.CODE_BLOCK)) and lines[-1].startswith(tuple(BlockDelimiter.CODE_BLOCK)):
        return BlockType.CODE_BLOCK

    if block.startswith(tuple(BlockDelimiter.BLOCKQUOTE)):
        for line in lines:
            if not line.startswith(tuple(BlockDelimiter.BLOCKQUOTE)):
                return BlockType.PARAGRAPH
        return BlockType.BLOCKQUOTE

    if block.startswith(BlockDelimiter.UNORDERED_LIST[0]):
        for line in lines:
            if not line.startswith(BlockDelimiter.UNORDERED_LIST[0]):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    
    return BlockType.PARAGRAPH