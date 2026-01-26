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
        self.assertEqual(bm.block_to_block_type(block), bm.BlockType.HEADING)
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
    
    def test_blockquote(self):
        md = """
> Je suis cerise !! la **GROSSE** fée ![belle fée](https://laGrosseFee.png)
> j'aime la fée

> et ça c'est un autre testblock
"""

        node = bm.markdown_to_html_node(md)
        html = node.to_html()
        self.maxDiff = None
        self.assertEqual(
            html,
            "<div><blockquote>Je suis cerise !! la <b>GROSSE</b> fée <img src=\"https://laGrosseFee.png\" alt=\"belle fée\"></img>\nj'aime la fée</blockquote><blockquote>et ça c'est un autre testblock</blockquote></div>"
        )
    
    def test_heading(self):
        md = """
# big h1

## **ptit** h2

### _grand_ h3

##### h5 ça mère la pute il est long celui là dis donc

#### h4

###### eheh 6
"""
        node = bm.markdown_to_html_node(md)
        html = node.to_html()
        self.maxDiff = None
        self.assertEqual(
            html,
            "<div><h1>big h1</h1><h2><b>ptit</b> h2</h2><h3><i>grand</i> h3</h3><h5>h5 ça mère la pute il est long celui là dis donc</h5><h4>h4</h4><h6>eheh 6</h6></div>"
        )

    def test_unorderedList(self):
        md = """
- Chocolat
- _Fraise_ banane
- Cerise

- 2eme ul
- tarte
- pastèque
- **framboise**
"""
        node = bm.markdown_to_html_node(md)
        html = node.to_html()
        self.maxDiff = None
        self.assertEqual(
            html,
            "<div><ul><li>Chocolat</li><li><i>Fraise</i> banane</li><li>Cerise</li></ul><ul><li>2eme ul</li><li>tarte</li><li>pastèque</li><li><b>framboise</b></li></ul></div>"
        )
    
    def test_orderedList(self):
        md = """
1. chocolatine
2. titus **mordecus** plasphemus
3. Mordekeinen 3eme du [nom](https://www.Wikidot.fr/mordekeinen)

1. 2eme ol
2. tartiflete
"""
        node = bm.markdown_to_html_node(md)
        html = node.to_html()
        self.maxDiff = None
        self.assertEqual(
            html,
            "<div><ol><li>chocolatine</li><li>titus <b>mordecus</b> plasphemus</li><li>Mordekeinen 3eme du <a href=\"https://www.Wikidot.fr/mordekeinen\">nom</a></li></ol><ol><li>2eme ol</li><li>tartiflete</li></ol></div>"
        )

if __name__ == "__main__":
    unittest.main()