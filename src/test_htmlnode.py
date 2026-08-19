import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            tag = "a",
            value = "Searchengine",
            children = None,
            props = {
            "href": "https://www.google.com",
            "target": "_blank",
            }
        )

        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"',)


    def test_props_none(self):
        node2 = HTMLNode(
            tag = "a",
            value = "Searchengine",
            children = None,
            props = None,
        )

        self.assertEqual(
        node2.props_to_html(), "")


    def test_props_empty(self):
        node3 = HTMLNode(
            tag = "a",
            value = "Searchengine",
            children = None,
            props = {},
        )

        self.assertEqual(
        node3.props_to_html(), "")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


    def test_leaf_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')


    def test_leaf_multiple_props(self):
        node = LeafNode("a", "Google",{"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(),'<a href="https://www.google.com" target="_blank">Google</a>')


    def test_leaf_tag_empty(self):
        node = LeafNode(None, "Hello")
        self.assertEqual(node.to_html(), "Hello")



if __name__ == "__main__":
    unittest.main()