import unittest
from block_markdown import block_to_block_type, BlockType

class TestBlockToBlockType(unittest.TestCase):
    def test_heading_level_1(self):
        block = "# Heading One"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_level_6(self):
        block = "###### Heading Six"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_invalid(self):
        block = "####### Too Many Hashes"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\ncode block\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> Quote line 1\n> Quote line 2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_invalid(self):
        block = "> This is fine\nNot quoted"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_block(self):
        block = "- Item one\n- Item two\n- Item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_block_invalid(self):
        block = "- Item one\n  - Subitem"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_block(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_numbers(self):
        block = "1. First\n3. Wrong Second\n4. Third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph(self):
        block = "This is just a normal paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_mixed_list_wrong(self):
        block = "1. First\n- Mixed with bullet"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_missing_space(self):
        block = "#InvalidHeading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == '__main__':
    unittest.main()
