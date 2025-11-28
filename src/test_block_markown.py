import unittest
import block_markdown as bm

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = bm.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(bm.block_to_block_type(block), bm.BlockType.HEADER)
        block = "```\ncode\n```"
        self.assertEqual(bm.block_to_block_type(block), bm.BlockType.CODE_BLOCK)
        block = "> quote\n> more quote"
        self.assertEqual(bm.block_to_block_type(block), bm.BlockType.BLOCKQUOTE)
        block = "- list\n- items"
        self.assertEqual(bm.block_to_block_type(block), bm.BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(bm.block_to_block_type(block), bm.BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(bm.block_to_block_type(block), bm.BlockType.PARAGRAPH)
if __name__ == "__main__":
    unittest.main()