import unittest

from extractor import extract_markdown_images, extract_markdown_links


class TestExtractor(unittest.TestCase):
    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], extract_markdown_links(text))

    def test_extract_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        self.assertEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], extract_markdown_images(text))

    def test_dont_extract_links_as_images(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual([], extract_markdown_images(text))

    def test_dont_extract_images_as_links(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        self.assertEqual([], extract_markdown_links(text))

if __name__ == "__main__":
    unittest.main()