import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_parent_node_with_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        node.to_html()
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parent_node_children_none(self):
        node = ParentNode("p", None)
        self.assertRaises(ValueError, lambda: node.to_html())

    def test_parent_node_children_empty(self):
        node = ParentNode("p", [])
        self.assertRaises(ValueError, lambda: node.to_html())

    def test_nested_nodes(self):
        node = ParentNode("ul", [
            LeafNode("li", "Item 1", {"style": "font-weight: 200;"}),
            ParentNode("ul", [
                LeafNode("li", "Item 2"),
                ParentNode("li", [
                    LeafNode("a", "Item 3", {"href": "https://www.google.com", "target": "_blank"})
                ]),
                LeafNode("li", "Item 4"),
            ]),
            LeafNode("li", "Item 5"),
            LeafNode("li", "Item 6"),
        ])

        self.assertEqual(node.to_html(), '<ul><li style="font-weight: 200;">Item 1</li><ul><li>Item 2</li><li><a href="https://www.google.com" target="_blank">Item 3</a></li><li>Item 4</li></ul><li>Item 5</li><li>Item 6</li></ul>')

if __name__ == "__main__":
    unittest.main()