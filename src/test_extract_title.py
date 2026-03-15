import unittest

from main import extract_title

class TestExtract(unittest.TestCase):
    def test_header(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_header_inline(self):
        markdown = "Some intro text\n# Hello\nSome more text"
        self.assertEqual(extract_title(markdown), "Hello")
    
    def test_no_header(self):
        markdown = "## Just a subheading\nSome text"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extra_space(self):
        markdown = "#   Hello   "
        self.assertEqual(extract_title(markdown), "Hello")