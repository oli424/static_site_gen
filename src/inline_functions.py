import re

from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if delimiter not in node.text:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
                raise Exception("Invalid Markdown syntax")
        
        for i, part in enumerate(parts):
            if part == "":
                continue

            if i % 2 == 0:
                 new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                 new_nodes.append(TextNode(part, text_type))
    
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.IMAGE:
            new_nodes.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        if images == []:
            new_nodes.append(old_node)
            continue
        
        image_alt = images[0][0]
        image_url = images[0][1]
        
        sections = old_node.text.split(f"![{image_alt}]({image_url})", 1)
        if sections[0] != "":
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
        new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))

        if sections[1] == "":
            continue
        elif extract_markdown_images(sections[1]) != []:
            new_nodes.extend(split_nodes_image([TextNode(sections[1], TextType.TEXT)]))
        else:
            new_nodes.append(TextNode(sections[1], TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.LINK:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        if links == []:
            new_nodes.append(old_node)
            continue
        
        link_desc = links[0][0]
        link_url = links[0][1]
        
        sections = old_node.text.split(f"[{link_desc}]({link_url})", 1)
        if sections[0] != "":
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
        new_nodes.append(TextNode(link_desc, TextType.LINK, link_url))

        if sections[1] == "":
            continue
        if extract_markdown_links(sections[1]) != []:
            new_nodes.extend(split_nodes_link([TextNode(sections[1], TextType.TEXT)]))
        else:
            new_nodes.append(TextNode(sections[1], TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    original_text = [TextNode(text, TextType.TEXT)]
    split_bold = split_nodes_delimiter(original_text, "**", TextType.BOLD)
    split_italic = split_nodes_delimiter(split_bold, "_", TextType.ITALIC)
    split_code_block = split_nodes_delimiter(split_italic, "`", TextType.CODE)
    split_image = split_nodes_image(split_code_block)
    split_link = split_nodes_link(split_image)
    return split_link



        