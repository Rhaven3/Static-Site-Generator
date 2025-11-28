import unittest
import inline_markdown

class TestUtils(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        # no delimiter present
        nodes = [inline_markdown.TextNode("This is a test", inline_markdown.TextType.TEXT)]
        with self.assertRaises(Exception):
            inline_markdown.split_nodes_delimiter(nodes, "", inline_markdown.TextType.TEXT)
        
        # delimiter **
        nodes = [inline_markdown.TextNode("This is **a** test", inline_markdown.TextType.TEXT)]
        result = inline_markdown.split_nodes_delimiter(nodes, "**", inline_markdown.TextType.TEXT)
        expected = [
            inline_markdown.TextNode("This is ", inline_markdown.TextType.TEXT),
            inline_markdown.TextNode("a", inline_markdown.TextType.BOLD),
            inline_markdown.TextNode(" test", inline_markdown.TextType.TEXT),
        ]
        self.assertEqual(result, expected)

        # delimiter *
        nodes = [inline_markdown.TextNode("This is *a* test", inline_markdown.TextType.TEXT)]
        result = inline_markdown.split_nodes_delimiter(nodes, "*", inline_markdown.TextType.TEXT)
        expected = [
            inline_markdown.TextNode("This is ", inline_markdown.TextType.TEXT),
            inline_markdown.TextNode("a", inline_markdown.TextType.ITALIC),
            inline_markdown.TextNode(" test", inline_markdown.TextType.TEXT),
        ]
        self.assertEqual(result, expected)

        # delimiter ```
        nodes = [inline_markdown.TextNode("This is ``code`` test", inline_markdown.TextType.TEXT)]
        result = inline_markdown.split_nodes_delimiter(nodes, "``", inline_markdown.TextType.TEXT)  
        expected = [
            inline_markdown.TextNode("This is ", inline_markdown.TextType.TEXT),
            inline_markdown.TextNode("code", inline_markdown.TextType.CODE),
            inline_markdown.TextNode(" test", inline_markdown.TextType.TEXT),
        ]
        self.assertEqual(result, expected)
        
    def test_extract_markdown_images(self):
        text = "Here is an image ![alt text](http://example.com/image.png) in markdown."
        result = inline_markdown.extract_markdown_images(text)
        expected = [("alt text", "http://example.com/image.png")]
        self.assertEqual(result, expected)

        text = "No images here."
        result = inline_markdown.extract_markdown_images(text)
        expected = []
        self.assertEqual(result, expected)

        text = "Multiple images ![first](http://example.com/first.png) and ![second](http://example.com/second.png)."
        result = inline_markdown.extract_markdown_images(text)
        expected = [("first", "http://example.com/first.png"), ("second", "http://example.com/second.png")]
        self.assertEqual(result, expected)

    def test_extract_markdown_links(self):
        text = "Here is a link [example](http://example.com) in markdown."
        result = inline_markdown.extract_markdown_links(text)
        expected = [("example", "http://example.com")]
        self.assertEqual(result, expected)

        text = "No links here."
        result = inline_markdown.extract_markdown_links(text)
        expected = []
        self.assertEqual(result, expected)

        text = "Multiple links [first](http://example.com/first) and [second](http://example.com/second)."
        result = inline_markdown.extract_markdown_links(text)
        expected = [("first", "http://example.com/first"), ("second", "http://example.com/second")]
        self.assertEqual(result, expected)

    def test_split_nodes_link(self):
        nodes = [inline_markdown.TextNode("This is a [link](http://example.com) test", inline_markdown.TextType.TEXT)]
        result = inline_markdown.split_nodes_link(nodes)
        expected = [
            inline_markdown.TextNode("This is a ", inline_markdown.TextType.TEXT),
            inline_markdown.TextNode("link", inline_markdown.TextType.LINK, "http://example.com"),
            inline_markdown.TextNode(" test", inline_markdown.TextType.TEXT),
        ]
        self.assertEqual(result, expected)
        
        # test mulitple nodes
        nodes = [inline_markdown.TextNode("This is a [link1](http://example.com/1) and [link2](http://example.com/2) test", inline_markdown.TextType.TEXT)]
        result = inline_markdown.split_nodes_link(nodes)
        expected = [
            inline_markdown.TextNode("This is a ", inline_markdown.TextType.TEXT),
            inline_markdown.TextNode("link1", inline_markdown.TextType.LINK, "http://example.com/1"),
            inline_markdown.TextNode(" and ", inline_markdown.TextType.TEXT),
            inline_markdown.TextNode("link2", inline_markdown.TextType.LINK, "http://example.com/2"),
            inline_markdown.TextNode(" test", inline_markdown.TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image(self):
        nodes = [inline_markdown.TextNode("This is an ![image](http://example.com/image.png) test", inline_markdown.TextType.TEXT)]
        result = inline_markdown.split_nodes_image(nodes)
        expected = [
            inline_markdown.TextNode("This is an ", inline_markdown.TextType.TEXT),
            inline_markdown.TextNode("image", inline_markdown.TextType.IMAGE, "http://example.com/image.png"),
            inline_markdown.TextNode(" test", inline_markdown.TextType.TEXT),
        ]
        self.assertEqual(result, expected)
        
        # test multiple nodes
        nodes = [inline_markdown.TextNode("This is an ![image1](http://example.com/image1.png) and ![image2](http://example.com/image2.png) test", inline_markdown.TextType.TEXT)]
        result = inline_markdown.split_nodes_image(nodes)
        expected = [
            inline_markdown.TextNode("This is an ", inline_markdown.TextType.TEXT),
            inline_markdown.TextNode("image1", inline_markdown.TextType.IMAGE, "http://example.com/image1.png"),
            inline_markdown.TextNode(" and ", inline_markdown.TextType.TEXT),
            inline_markdown.TextNode("image2", inline_markdown.TextType.IMAGE, "http://example.com/image2.png"),
            inline_markdown.TextNode(" test", inline_markdown.TextType.TEXT),
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()