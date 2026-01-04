import re

from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    for i, block in enumerate(blocks):
        if block == "":
            blocks.remove(block)
            continue
        blocks[i] = block.strip()
    return blocks

def block_to_block_type(block):
    lines = block.split("\n")
    if block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    elif "#" in lines[0][0]:
        words = lines[0].split()
        if len(words[0]) <= 6:
            for char in words[0]:
                if char != "#":
                    return BlockType.PARAGRAPH
            return BlockType.HEADING
        else:
            return BlockType.PARAGRAPH
    else:
        quote = []
        unordered_list = []
        ordered_list = []

        for line in lines:
            if line[0] == ">":
                quote.append(True)
            else:
                quote.append(False)
            if line[:2] == "- ":
                unordered_list.append(True)
            else:
                unordered_list.append(False)
            if line.split(".", 1)[0].isnumeric():
                ordered_list.append(True)
            else:
                ordered_list.append(False)
        if all(quote):
            return BlockType.QUOTE
        if all(unordered_list):
            return BlockType.UNORDERED_LIST
        if all(ordered_list):
            return BlockType.ORDERED_LIST
        return BlockType.PARAGRAPH


    
