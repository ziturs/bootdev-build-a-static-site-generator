import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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


class TestParentNode(unittest.TestCase):
    def test_parent_to_html_p(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    
    def test_parent_to_html_with_parents(self):
                node = ParentNode(
                    "p",
                    [
                        ParentNode(
                            "p",
                            [
                                LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"),
                            ],
                        ),
                         ParentNode(
                            "p",
                            [
                                LeafNode("i", "italic text"),
                                LeafNode(None, "Normal text"),
                            ],
                        )
                    ],
                )

                self.assertEqual(node.to_html(), "<p><p><b>Bold text</b>Normal text</p><p><i>italic text</i>Normal text</p></p>")


    def test_parent_to_html_no_tag(self):
        node = ParentNode(
            None,
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        
        with self.assertRaises(ValueError):
            node.to_html()



    def test_parent_to_html_missing_children(self):
        node = ParentNode(
            "p",
            None,
        )
        
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()