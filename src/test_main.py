import unittest

from main import extract_title

class TestMain(unittest.TestCase):
    def test_extract_title_1(self):
        text = "# Test"
        self.assertEqual(extract_title(text), "Test")

    def test_extract_title_2(self):
        text = "# Test  "
        self.assertEqual(extract_title(text), "Test")

    def test_extract_title_3(self):
        text = """
# Test

Test

"""
        self.assertEqual(extract_title(text), "Test")

    def test_extract_title_4(self):
        text = """
Test

# Test

"""
        self.assertEqual(extract_title(text), "Test")

    def test_extract_wrong_1(self):
        text = "## Test"
        self.assertRaises(Exception, lambda: extract_title(text))

    def test_extract_wrong_2(self):
        text = "Test"
        self.assertRaises(Exception, lambda: extract_title(text))

if __name__ == "__main__":
    unittest.main()