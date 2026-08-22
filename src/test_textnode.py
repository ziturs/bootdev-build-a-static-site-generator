import unittest
from textnode import TextNode, TextType, text_node_to_html_node

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


    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")


    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "boot.def")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "boot.def"} )


    def test_image(self):
        node = TextNode("image.png", TextType.IMAGE, "image url")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {
            "src": "image url",
            "alt": "image.png"
            })


if __name__ == "__main__":
    unittest.main()