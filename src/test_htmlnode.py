import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_no_property(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), '')

    def test_props_to_html_one_property(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_more_properties(self):
        node = HTMLNode(props={"href": "https://www.google.com", "style": "color:red;"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" style="color:red;"')

    def test_repr(self):
        node = HTMLNode('a', "Link!", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.__repr__(), "HTMLNode(a, Link!, None, {'href': 'https://www.google.com', 'target': '_blank'})")


if __name__ == "__main__":
    unittest.main()