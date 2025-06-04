import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_basic_title(self):
        md = "# Hello"
        self.assertEqual(extract_title(md), "Hello")

    def test_title_with_whitespace(self):
        md = "   #    Hello World    "
        self.assertEqual(extract_title(md), "Hello World")

    def test_title_not_first_line(self):
        md = "\nSome intro\n# Title Here\nMore text"
        self.assertEqual(extract_title(md), "Title Here")

    def test_no_h1_raises(self):
        md = "## Subheading\nNo h1 here"
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_multiple_headers(self):
        md = "# First Title\n# Second Title"
        self.assertEqual(extract_title(md), "First Title")

if __name__ == "__main__":
    unittest.main()
