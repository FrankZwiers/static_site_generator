from enum import Enum
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import text_node_to_html_node
from node_splitter import *
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    return list(map(lambda item: item.strip(), filter(lambda item: item, markdown.split("\n\n"))))

def block_to_block_type(text):
    if text == "":
        return BlockType.PARAGRAPH

    if re.match("^#{1,6} ", text) != None:
        return BlockType.HEADING
    if re.match("```(\n.*)+```", text) != None:
        return BlockType.CODE

    can_be_quote = True
    can_be_ul = True
    can_be_ol = 0
    for line in text.split("\n"):
        can_be_quote = can_be_quote and line[0] == ">"
        can_be_ul = can_be_ul and line[0:2] == "- "
        if can_be_ol != -1:
            if line[0] == f"{can_be_ol + 1}" and line[1] == ".":
                can_be_ol += 1
            else:
                can_be_ol = -1

    if can_be_quote:
        return BlockType.QUOTE

    if can_be_ul:
        return BlockType.UNORDERED_LIST

    return BlockType.ORDERED_LIST if can_be_ol > 0 else BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match(block_type):
            case BlockType.PARAGRAPH:
                child_nodes.append(ParentNode("p", text_to_children(block)))
            case BlockType.HEADING:
                child_nodes.append(ParentNode(f"{get_h_tag(block)}", text_to_children(re.sub("^#{1,6} ", "", block))))
            case BlockType.CODE:
                child_nodes.append(ParentNode("pre", [LeafNode("code", block[4:-3])]))
            case BlockType.QUOTE:
                lines = block.split("\n")
                child_nodes.append(ParentNode(
                    "blockquote", [LeafNode("p", " ".join(list(map(lambda line: line[2:], lines))))]))
            case BlockType.UNORDERED_LIST:
                lines = block.split("\n")
                child_nodes.append(ParentNode("ul", list(map(lambda child: LeafNode('li', child), list(map(lambda line: line[2:], lines))))))
            case BlockType.ORDERED_LIST:
                lines = block.split("\n")
                child_nodes.append(ParentNode("ol", list(map(lambda child: LeafNode('li', child), list(map(lambda line: re.sub("^(\\d+)\\. ", "", line), lines))))))

    return ParentNode("div", child_nodes)

def get_h_tag(block):
    return f"h{block.count("#")}"

def text_to_children(text):
    html_nodes = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))

    return html_nodes