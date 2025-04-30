import unittest

from leafnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_leaf_to_html_p_no_properties(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode('a', "Link!", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\" target=\"_blank\">Link!</a>")

    def test_leaf_to_raw_text(self):
        node = LeafNode(None, "Link!", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), "Link!")

    def test_leaf_no_value(self):
        node = LeafNode(None, None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertRaises(ValueError, lambda: node.to_html())

if __name__ == "__main__":
    unittest.main()