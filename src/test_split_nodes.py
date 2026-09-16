import unittest

from split_nodes import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_code(self):
        split_node1 = TextNode("This is text with a `code block` word", TextType.TEXT)

        result = split_nodes_delimiter([split_node1], "`", TextType.CODE)

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
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
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_markdown_links_ignores_images(self):
        matches = extract_markdown_links(
            "Here is [a link](https://example.com) and ![an image](https://example.com/image.png)"
        )

        self.assertListEqual(
            [("a link", "https://example.com")],
            matches,
        )

    def test_split_node_image(self):
        node = TextNode(
            "Here is ![an image](https://example.com/image.png)", TextType.TEXT
        )
        matches = split_nodes_image([node])
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("an image", TextType.IMAGE, "https://example.com/image.png"),
        ]
        self.assertListEqual(expected, matches)

    def test_split_node_images(self):
        node = TextNode(
            "Here is ![an image](https://example.com/image.png) and ![an image](https://example.com/image.png)",
            TextType.TEXT,
        )
        matches = split_nodes_image([node])
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("an image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("an image", TextType.IMAGE, "https://example.com/image.png"),
        ]

        self.assertListEqual(expected, matches)

    def test_split_node_no_images(self):
        node = TextNode("Here is just plain Text", TextType.TEXT)
        matches = split_nodes_image([node])
        expected = [
            TextNode("Here is just plain Text", TextType.TEXT),
        ]
        self.assertListEqual(expected, matches)

    def test_split_nodes_link(self):
        node = TextNode(
            "Here is [a link](https://example.com) to nowhere!", TextType.TEXT
        )
        matches = split_nodes_link([node])
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("a link", TextType.LINK, "https://example.com"),
            TextNode(" to nowhere!", TextType.TEXT),
        ]
        self.assertListEqual(expected, matches)

    def test_split_nodes_no_link(self):
        node = TextNode("Here is just plain Text", TextType.TEXT)
        matches = split_nodes_link([node])
        expected = [
            TextNode("Here is just plain Text", TextType.TEXT),
        ]
        self.assertListEqual(expected, matches)

    def test_split_nodes_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        matches = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertListEqual(expected, matches)

    def test_split_nodes_link_with_image(self):
        node = TextNode(
            "Here is ![an image](https://example.com/image.png)", TextType.TEXT
        )
        matches = split_nodes_link([node])
        expected = [
            TextNode(
                "Here is ![an image](https://example.com/image.png)", TextType.TEXT
            ),
        ]
        self.assertListEqual(expected, matches)

    def test_text_to_textnodes1(self):
        test_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(test_text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertListEqual(expected, result)

    def test_text_to_textnodes2(self):
        test_text = "Start with **bold**, then _italic_, some `code`, an ![image](https://example.com/pic.png), and finally a [link](https://example.com)."
        result = text_to_textnodes(test_text)
        expected = [
            TextNode("Start with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", then ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", some ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/pic.png"),
            TextNode(", and finally a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.TEXT),
        ]

        self.assertListEqual(expected, result)
