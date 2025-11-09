import unittest
import utils

class TestUtils(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        # no delimiter present
        nodes = [utils.TextNode("This is a test", utils.TextType.TEXT)]
        with self.assertRaises(Exception):
            utils.split_nodes_delimiter(nodes, "", utils.TextType.TEXT)
        
        # delimiter **
        nodes = [utils.TextNode("This is **a** test", utils.TextType.TEXT)]
        result = utils.split_nodes_delimiter(nodes, "**", utils.TextType.TEXT)
        expected = [
            utils.TextNode("This is ", utils.TextType.TEXT),
            utils.TextNode("a", utils.TextType.BOLD),
            utils.TextNode(" test", utils.TextType.TEXT),
        ]
        self.assertEqual(result, expected)

        # delimiter *
        nodes = [utils.TextNode("This is *a* test", utils.TextType.TEXT)]
        result = utils.split_nodes_delimiter(nodes, "*", utils.TextType.TEXT)
        expected = [
            utils.TextNode("This is ", utils.TextType.TEXT),
            utils.TextNode("a", utils.TextType.ITALIC),
            utils.TextNode(" test", utils.TextType.TEXT),
        ]
        self.assertEqual(result, expected)

        # delimiter ```
        nodes = [utils.TextNode("This is ``code`` test", utils.TextType.TEXT)]
        result = utils.split_nodes_delimiter(nodes, "``", utils.TextType.TEXT)  
        expected = [
            utils.TextNode("This is ", utils.TextType.TEXT),
            utils.TextNode("code", utils.TextType.CODE),
            utils.TextNode(" test", utils.TextType.TEXT),
        ]
        self.assertEqual(result, expected)
        
    def test_extract_markdown_images(self):
        text = "Here is an image ![alt text](http://example.com/image.png) in markdown."
        result = utils.extract_markdown_images(text)
        expected = [("alt text", "http://example.com/image.png")]
        self.assertEqual(result, expected)

        text = "No images here."
        result = utils.extract_markdown_images(text)
        expected = []
        self.assertEqual(result, expected)

        text = "Multiple images ![first](http://example.com/first.png) and ![second](http://example.com/second.png)."
        result = utils.extract_markdown_images(text)
        expected = [("first", "http://example.com/first.png"), ("second", "http://example.com/second.png")]
        self.assertEqual(result, expected)

    def test_extract_markdown_links(self):
        text = "Here is a link [example](http://example.com) in markdown."
        result = utils.extract_markdown_links(text)
        expected = [("example", "http://example.com")]
        self.assertEqual(result, expected)

        text = "No links here."
        result = utils.extract_markdown_links(text)
        expected = []
        self.assertEqual(result, expected)

        text = "Multiple links [first](http://example.com/first) and [second](http://example.com/second)."
        result = utils.extract_markdown_links(text)
        expected = [("first", "http://example.com/first"), ("second", "http://example.com/second")]
        self.assertEqual(result, expected)

    def test_split_nodes_link(self):
        nodes = [utils.TextNode("This is a [link](http://example.com) test", utils.TextType.TEXT)]
        result = utils.split_nodes_link(nodes)
        expected = [
            utils.TextNode("This is a ", utils.TextType.TEXT),
            utils.TextNode("link", utils.TextType.LINK, "http://example.com"),
            utils.TextNode(" test", utils.TextType.TEXT),
        ]
        self.assertEqual(result, expected)
        
        # test mulitple nodes
        nodes = [utils.TextNode("This is a [link1](http://example.com/1) and [link2](http://example.com/2) test", utils.TextType.TEXT)]
        result = utils.split_nodes_link(nodes)
        expected = [
            utils.TextNode("This is a ", utils.TextType.TEXT),
            utils.TextNode("link1", utils.TextType.LINK, "http://example.com/1"),
            utils.TextNode(" and ", utils.TextType.TEXT),
            utils.TextNode("link2", utils.TextType.LINK, "http://example.com/2"),
            utils.TextNode(" test", utils.TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image(self):
        nodes = [utils.TextNode("This is an ![image](http://example.com/image.png) test", utils.TextType.TEXT)]
        result = utils.split_nodes_image(nodes)
        expected = [
            utils.TextNode("This is an ", utils.TextType.TEXT),
            utils.TextNode("image", utils.TextType.IMAGE, "http://example.com/image.png"),
            utils.TextNode(" test", utils.TextType.TEXT),
        ]
        self.assertEqual(result, expected)
        
        # test multiple nodes
        nodes = [utils.TextNode("This is an ![image1](http://example.com/image1.png) and ![image2](http://example.com/image2.png) test", utils.TextType.TEXT)]
        result = utils.split_nodes_image(nodes)
        expected = [
            utils.TextNode("This is an ", utils.TextType.TEXT),
            utils.TextNode("image1", utils.TextType.IMAGE, "http://example.com/image1.png"),
            utils.TextNode(" and ", utils.TextType.TEXT),
            utils.TextNode("image2", utils.TextType.IMAGE, "http://example.com/image2.png"),
            utils.TextNode(" test", utils.TextType.TEXT),
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()