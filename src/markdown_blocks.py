from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
    lines = markdown.split("\n")
    blocks = []
    current_block_lines = []
    current_type = None
    in_code_block = False

    for line in lines:
        if line.strip() == "" and not in_code_block:
            if current_block_lines:
                blocks.append("\n".join(current_block_lines).strip())
                current_block_lines = []
                current_type = None
            continue

        if line.strip().startswith("```") and line.strip().endswith("```") and  len(line.strip()) > 6 and not in_code_block:
            if current_block_lines:
                    blocks.append("\n".join(current_block_lines).strip())
                    current_block_lines = []
                    current_type = None
            blocks.append(line.strip())
            continue
        if in_code_block:
            current_block_lines.append(line)
            continue

        line_type = line_to_block_type(line)
        if current_type is None:
            current_type = line_type
            current_block_lines = [line]
        else:
            if line_type == current_type:
                current_block_lines.append(line)
            else:
                blocks.append("\n".join(current_block_lines).strip())
                current_block_lines = [line]
                current_type = line_type
    if current_block_lines:
        blocks.append("\n".join(current_block_lines).strip())
    blocks = [b for b in blocks if b.strip()]
    return blocks


def line_to_block_type(line):
    line = line.lstrip()
    if line.startswith("#"):
        return BlockType.HEADING
    if line.startswith(">"):
        return BlockType.QUOTE
    if line.startswith("- "):
        return BlockType.ULIST
    if len(line) > 2 and line[0].isdigit() and line[1] == "." and line[2] == " ":
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def block_to_block_type(block):
    block = block.strip()
    if block == "":
        return BlockType.PARAGRAPH
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
            if not line:
                continue
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
            return BlockType.ULIST
        if all(ordered_list):
            return BlockType.OLIST
        return BlockType.PARAGRAPH


    
