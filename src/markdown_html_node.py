import os
from markdown_blocks import BlockType, markdown_to_blocks, block_to_block_type
from htmlnode import HTMLNode, ParentNode, text_node_to_html_node
from textnode import TextNode
from inline_markdown import text_to_textnodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        if block.strip() == "":
            continue
        node = block_to_html(block)
        children.append(node)
    html_node = ParentNode("div", children)
    return html_node

def block_to_html(block):
    block = block.rstrip("\n")
    if block.strip() == "":
        raise ValueError("Empty block")
    line = block.split("\n")[0]
    if not line:
        raise ValueError("Empty first line in block")
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            content = block.strip().split("\n")
            content = " ".join(content)
            children = text_to_children(content)
            return ParentNode(tag="p", children=children)
        case BlockType.HEADING:
            text = block.lstrip("#")
            count = len(block) - len(text)
            tag = f"h{count}"
            children = text_to_children(text.lstrip())
            return ParentNode(tag=tag, children=children)
        case BlockType.CODE:
            outer_tag = "pre"
            lines = block.split("\n")
            if len(lines) == 1 and lines[0].startswith("```") and lines[0].endswith("```"):
                content = lines[0][3:-3]
            else:
                content = "\n".join(lines[1:-1]) + "\n"
            text_node = TextNode(content, "code")
            html_node = text_node_to_html_node(text_node)
            return ParentNode(outer_tag, [html_node])
        case BlockType.QUOTE:
            tag = "blockquote"
            lines = block.split("\n")
            for i, line in enumerate(lines):
                lines[i] = line.lstrip(">").lstrip()
            content = " ".join(lines)
            children = text_to_children(content)
            return ParentNode(tag, children)
        case BlockType.ULIST:
            outer_tag = "ul"
            tag = "li"
            lines = block.split("\n")
            children = []
            for line in lines:
                line = line.lstrip("-").lstrip()
                line_children = text_to_children(line)
                li_node = ParentNode(tag, line_children)
                children.append(li_node)
            return ParentNode(outer_tag, children)
        case BlockType.OLIST:
            outer_tag = "ol"
            tag = "li"
            lines = block.split("\n")
            children = []
            for line in lines:
                if not line.strip():
                    continue
                number_and_rest = line.split(".", 1)
                line_children = text_to_children(number_and_rest[1].lstrip())
                li_node = ParentNode(tag, line_children)
                children.append(li_node)
            return ParentNode(outer_tag, children)
        case _:
            raise ValueError(f"Unknown block type: {block_type}")
        
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            count = len(block) - len(block.lstrip("#"))
            if count == 1:
                text = block.lstrip("#").lstrip()
                return text
    raise Exception("No heading found in markdown")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_content = open(from_path, "r").read()
    template_content = open(template_path, "r").read()
    html_string = markdown_to_html_node(md_content).to_html()
    title = extract_title(md_content)
    final_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    final_content = final_content.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as f:
        f.write(final_content)

def generate_pages_recursive(dir_path_content, dir_path_template, dest_dir_path, basepath):
    for file in os.listdir(dir_path_content):
        if os.path.isfile(os.path.join(dir_path_content, file)):
            if file.endswith(".md"):
                from_path = os.path.join(dir_path_content, file)
                dest_path = os.path.join(dest_dir_path, file[:-3] + ".html")
                generate_page(from_path, dir_path_template, dest_path, basepath)
        elif os.path.isdir(os.path.join(dir_path_content, file)):
            new_dir_path_content = os.path.join(dir_path_content, file)
            new_dest_dir_path = os.path.join(dest_dir_path, file)
            generate_pages_recursive(new_dir_path_content, dir_path_template, new_dest_dir_path, basepath)
    