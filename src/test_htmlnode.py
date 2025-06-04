import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single(self):
        node = HTMLNode(props={"href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev"')

    def test_props_to_html_multiple(self):
        node = HTMLNode(props={"href": "https://boot.dev", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev" target="_blank"')

    def test_props_to_html_empty(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_none(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")
        
    def test_repr(self):
        node = HTMLNode(tag="a", value="Click here", children=[], props={"href": "https://boot.dev"})
        expected_repr = "HTMLNode(tag=a, value=Click here, children=[], props={'href': 'https://boot.dev'})"
        self.assertEqual(repr(node), expected_repr)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")

    def test_leaf_to_html_value_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_parent_to_html(self):
        child1 = LeafNode("p", "Hello, world!")
        child2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node = ParentNode("div", [child1, child2])
        expected_html = '<div><p>Hello, world!</p><a href="https://www.google.com">Click me!</a></div>'
        self.assertEqual(node.to_html(), expected_html)

    def test_parent_to_html_no_tag(self):
        child1 = LeafNode("p", "Hello, world!")
        with self.assertRaises(ValueError):
            ParentNode(None, [child1]).to_html()

    def test_parent_to_html_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_parent_to_html_empty_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

    def test_parent_to_html_child_without_to_html(self):
        class NonHTMLNode:
            pass

        child1 = NonHTMLNode()
        with self.assertRaises(TypeError):
            ParentNode("div", [child1]).to_html()

    def test_parent_to_html_child_with_invalid_type(self):
        class InvalidChild:
            def __init__(self):
                self.to_html = None

        child1 = InvalidChild()
        with self.assertRaises(TypeError):
            ParentNode("div", [child1]).to_html()

    def test_parent_to_html_child_with_none(self):
        child1 = None
        with self.assertRaises(TypeError):
            ParentNode("div", [child1]).to_html()

    def test_parent_to_html_child_with_empty_string(self):
        child1 = LeafNode("p", "")
        node = ParentNode("div", [child1])
        expected_html = "<div><p></p></div>"
        self.assertEqual(node.to_html(), expected_html)

if __name__ == "__main__":
    unittest.main()