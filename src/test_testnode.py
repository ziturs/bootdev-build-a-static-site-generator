import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_type(self):
        node3 = TextNode("This is a text node", TextType.ITALIC)
        node4 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node3, node4)

    def test_not_eq_text(self):
        node5 = TextNode("This is a text node", TextType.BOLD)
        node6 = TextNode("This is a test node", TextType.BOLD)
        self.assertNotEqual(node5, node6)

    def test_eq_url(self):
        node7 = TextNode("Link", TextType.LINK, "boot.dev")
        node8 = TextNode("Link", TextType.LINK, "boot.def")
        self.assertNotEqual(node7, node8)


if __name__ == "__main__":
    unittest.main()