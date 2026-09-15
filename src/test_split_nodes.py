import unittest

from split_nodes import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_code(self):
        split_node1 = TextNode("This is text with a `code block` word", TextType.TEXT)

        result = split_nodes_delimiter([split_node1], "`", TextType.CODE)

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(result, expected)


    def test_split_nodes_not_closed(self):
        split_node2 = TextNode("This is text with a `code block word", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([split_node2], "`", TextType.CODE)

    def test_split_nodes_italic(self):
        split_node3 = TextNode("This is text with a __code block__ word", TextType.TEXT)

        result = split_nodes_delimiter([split_node3], "__", TextType.ITALIC)

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(result, expected)