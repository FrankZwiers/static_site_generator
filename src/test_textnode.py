import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node with a different text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_link_has_url(self):
        node = TextNode("This is a link node", TextType.LINK, "https://google.com")
        node2 = TextNode("This is a link node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_text_bold_to_html(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(text_node_to_html_node(node).__repr__(), "HTMLNode(b, This is a text node, None, None)")

    def test_text_italic_to_html(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(text_node_to_html_node(node).__repr__(), "HTMLNode(i, This is a text node, None, None)")

    def test_text_code_to_html(self):
        node = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(text_node_to_html_node(node).__repr__(), "HTMLNode(code, This is a text node, None, None)")

    def test_text_link_to_html(self):
        node = TextNode("This is a text node", TextType.LINK, "https://google.com/")
        self.assertEqual(text_node_to_html_node(node).__repr__(), "HTMLNode(a, This is a text node, None, {'href': 'https://google.com/'})")

    def test_text_img_to_html(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://google.com/random_image_1")
        self.assertEqual(text_node_to_html_node(node).__repr__(), "HTMLNode(img, , None, {'src': 'https://google.com/random_image_1', 'alt': 'This is a text node'})")

    def test_text_painting_exception(self):
        node = TextNode("This is a text node", "painting", "https://google.com/random_image_1")
        self.assertRaises(Exception, lambda: text_node_to_html_node(node).__repr__())

if __name__ == "__main__":
    unittest.main()