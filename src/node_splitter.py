from textnode import TextNode, TextType
from extractor import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        splitted_nodes = node.text.split(delimiter)
        num_splitted_nodes = len(splitted_nodes)
        if num_splitted_nodes == 1:
            new_nodes.append(node)
            continue

        if (num_splitted_nodes != 3):
            raise Exception("Invalid markdown syntax")

        for i in range(0, 3):
            new_nodes.append(TextNode(splitted_nodes[i], TextType.TEXT if i % 2 == 0 else text_type))

    return new_nodes

def split_nodes_code(old_nodes):
    return split_nodes_delimiter(old_nodes, "`", TextType.CODE)

def split_nodes_bold(old_nodes):
    return split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

def split_nodes_italic(old_nodes):
    return split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)

def split_nodes_image(old_nodes):
    return _split_nodes(old_nodes, TextType.IMAGE)

def split_nodes_link(old_nodes):
    return _split_nodes(old_nodes, TextType.LINK)

def _split_nodes(old_nodes, text_type):
    new_nodes = []
    match text_type:
        case TextType.IMAGE:
            func = extract_markdown_images
            delimiter = "![{}]({})"
        case TextType.LINK:
            func = extract_markdown_links
            delimiter = "[{}]({})"
        case _:
            raise Exception("Unsupported text type for function")

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = func(node.text)
        remaining_text = node.text

        node_replacements = []

        if len(matches) == 0:
            new_nodes.append(node)
            continue

        for match in matches:
            parts = remaining_text.split(delimiter.format(match[0], match[1]), 1)
            node_replacements.extend([TextNode(parts[0], TextType.TEXT), TextNode(match[0], text_type, match[1])])

            remaining_text = parts[1] if len(parts) > 1 else ""

        if (remaining_text != ""):
            node_replacements.append(TextNode(remaining_text, TextType.TEXT))

        new_nodes.extend(node_replacements)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    for text_type in list(TextType):
        match (text_type):
            case TextType.BOLD:
                func = split_nodes_bold
            case TextType.ITALIC:
                func = split_nodes_italic
            case TextType.CODE:
                func = split_nodes_code
            case TextType.LINK:
                func = split_nodes_link
            case TextType.IMAGE:
                func = split_nodes_image
            case _:
                continue

        nodes = func(nodes)

    return nodes