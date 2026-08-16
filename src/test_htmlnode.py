import unittest
from htmlnode import HTMLNode

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


if __name__ == "__main__":
    unittest.main()