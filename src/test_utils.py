import unittest
import utils

class TestSplitNodesDelimiter(unittest.TestCase):
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

        # delimiter `
        nodes = [utils.TextNode("This is `code` test", utils.TextType.TEXT)]
        result = utils.split_nodes_delimiter(nodes, "`", utils.TextType.TEXT)  
        expected = [
            utils.TextNode("This is ", utils.TextType.TEXT),
            utils.TextNode("code", utils.TextType.CODE),
            utils.TextNode(" test", utils.TextType.TEXT),
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()