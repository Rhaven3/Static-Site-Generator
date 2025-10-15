import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )
    
    def test_leaf_to_html(self):
        leaf = LeafNode("span", "Leaf content", {"style": "color:red"})
        self.assertEqual(
            leaf.to_html(),
            '<span style="color:red">Leaf content</span>'
        )
        
        # 2
        leaf_no_tag = LeafNode(None, "Just text")
        self.assertEqual(
            leaf_no_tag.to_html(),
            'Just text'
        )

        # 3
        leaf_no_value = LeafNode("div", None)
        with self.assertRaises(ValueError):
            leaf_no_value.to_html()
            
        # 4
        leaf_no_props = LeafNode("p", "No props here")
        self.assertEqual(
            leaf_no_props.to_html(),
            '<p>No props here</p>'
        )
        
    def test_Parent_to_html(self):
        child1 = LeafNode("span", "Child 1")
        child2 = LeafNode("span", "Child 2", {"class": "highlight"})
        parent = ParentNode("div", [child1, child2], {"id": "parent"})

        self.assertEqual(
            parent.to_html(),
            '<div id="parent"><span>Child 1</span><span class="highlight">Child 2</span></div>'
        )

        # 2
        parent_no_tag = ParentNode(None, [child1])
        with self.assertRaises(ValueError):
            parent_no_tag.to_html()

        # 3
        parent_no_children = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_no_children.to_html()
            
        # 4
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()

