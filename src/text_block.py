from enum import Enum

import re

from htmlnode import HTMLNode, ParentNode, LeafNode
from split_nodes import text_to_textnodes
from textnode import TextNode , TextType, text_node_to_html_node

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    block_list = []
    for block in blocks:
        block = block.strip()
        if block:
            block_list.append(block)
    return block_list

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown_block) -> BlockType:
    if not markdown_block:
        return BlockType.PARAGRAPH

    lines = markdown_block.splitlines()

    if markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if markdown_block.startswith("```\n") and markdown_block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    is_ordered = True

    for index, line in enumerate(lines):
        expected = f"{index + 1}. "

        if not line.startswith(expected):
            is_ordered = False
            break

    if is_ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    leaf_nodes = []

    for text_node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(text_node))

    return leaf_nodes

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    block_list = []
    for markdown_block in markdown_blocks:
        block_type = block_to_block_type(markdown_block)
        if block_type == BlockType.CODE:
            block_text = markdown_block.removeprefix("```\n").removesuffix("```")
            text_node = TextNode(block_text, TextType.TEXT)
            leaf_node = text_node_to_html_node(text_node)
            code_parent_node = ParentNode("code", [leaf_node])
            parent_node = ParentNode("pre", [code_parent_node])

        elif block_type == BlockType.PARAGRAPH:
            lines = markdown_block.splitlines()
            paragraph_text = " ".join(lines)
            leaf_nodes = text_to_children(paragraph_text)
            parent_node = ParentNode("p", leaf_nodes)

        elif block_type == BlockType.HEADING:
            count = 0

            for char in markdown_block:
                if char != "#":
                    break
                count += 1

            heading_text = markdown_block[count + 1:]
            leaf_nodes = text_to_children(heading_text)
            parent_node = ParentNode("h" + str(count), leaf_nodes)

        elif block_type == BlockType.QUOTE:
            lines = markdown_block.splitlines()
            clean_lines = [] 
            for line in lines:
                line = line.removeprefix(">")
                line = line.removeprefix(" ")
                clean_lines.append(line)

            quote_text = "\n".join(clean_lines)
            leaf_nodes = text_to_children(quote_text)
            parent_node = ParentNode("blockquote", leaf_nodes)

        elif block_type == BlockType.UNORDERED_LIST:
            lines = markdown_block.splitlines()
            list_nodes = []
            for line in lines:
                line = line.removeprefix("- ")
                line_node = text_to_children(line)
                list_node = ParentNode("li", line_node)
                list_nodes.append(list_node) 

            parent_node = ParentNode("ul", list_nodes)

        elif block_type == BlockType.ORDERED_LIST:
            lines = markdown_block.splitlines()
            list_nodes = []
            for line in lines:
                line = line.split(" ", 1)[1]
                line_node = text_to_children(line)
                list_node = ParentNode("li", line_node)
                list_nodes.append(list_node) 

            parent_node = ParentNode("ol", list_nodes)


        block_list.append(parent_node)

    html_parent_node = ParentNode("div", block_list)


    return html_parent_node


