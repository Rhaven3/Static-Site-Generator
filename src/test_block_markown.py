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

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = bm.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = bm.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()