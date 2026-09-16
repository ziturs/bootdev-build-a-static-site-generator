def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    block_list = []
    for block in blocks:
        block = block.strip()
        if block:
            block_list.append(block)
    return block_list
