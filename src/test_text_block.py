import unittest

from text_block import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node


class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks1(self):
        block = """# This is a heading

    This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

    - This is the first list item in a list block
    - This is a list item
    - This is another list item"""

        result = markdown_to_blocks(block)

        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            """- This is the first list item in a list block
    - This is a list item
    - This is another list item""",
        ]

        self.assertListEqual(expected, result)

    def test_markdown_to_blocks2(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_different_line_between(self):
        block = """> This starts like a quote
but this line does not
> this one does again"""

        result = block_to_block_type(block)

        expected = BlockType.PARAGRAPH

        self.assertEqual(expected, result)

    def test_block_to_block_type_empty(self):
        block = ""

        result = block_to_block_type(block)

        expected = BlockType.PARAGRAPH

        self.assertEqual(expected, result)

    def test_block_to_block_type_ordered_list(self):
        block = """1. First item
2. Second item
3. Third item
4. Fourth item"""

        result = block_to_block_type(block)

        expected = BlockType.ORDERED_LIST

        self.assertEqual(expected, result)

    def test_block_to_block_type_false_ordered_list(self):
        block = """1. First item
2. Second item
4. Fourth item"""

        result = block_to_block_type(block)

        expected = BlockType.PARAGRAPH

        self.assertEqual(expected, result)


    def test_block_to_block_type_heading(self):
        block = """### Example heading"""

        result = block_to_block_type(block)

        expected = BlockType.HEADING

        self.assertEqual(expected, result)

    def test_block_to_block_type_code(self):
        block = """```
print("hello")
print("world")
```"""

        result = block_to_block_type(block)

        expected = BlockType.CODE

        self.assertEqual(expected, result)

    def test_block_to_block_type_quote(self):
        block = """> First quote line
> Second quote line
> Third quote line"""

        result = block_to_block_type(block)

        expected = BlockType.QUOTE

        self.assertEqual(expected, result)

    def test_block_to_block_type_unordered_list(self):
        block = """- First item
- Second item
- Third item"""

        result = block_to_block_type(block)

        expected = BlockType.UNORDERED_LIST

        self.assertEqual(expected, result)

    def test_block_to_block_type_paragraph(self):
        block = """This is just a normal paragraph
with a second line."""

        result = block_to_block_type(block)

        expected = BlockType.PARAGRAPH

        self.assertEqual(expected, result)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_Heading_quote_ul_ol(self):
        md = """### Hello **world**

> First line
> second _line_

- First item
- **Second** item

1. First item
2. `Second` item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            """<div><h3>Hello <b>world</b></h3><blockquote>First line
second <i>line</i></blockquote><ul><li>First item</li><li><b>Second</b> item</li></ul><ol><li>First item</li><li><code>Second</code> item</li></ol></div>""",
                )