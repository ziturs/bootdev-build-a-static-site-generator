from enum import Enum

import re

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
    
