import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("text node", TextType.BOLD)
        node1 = TextNode("not text node", TextType.ITALIC)
        self.assertNotEqual(node, node1)

    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://bit")

        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
