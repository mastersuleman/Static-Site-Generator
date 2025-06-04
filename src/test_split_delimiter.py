import unittest
from textnode import TextNode, TextType
from split_delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link, extract_markdown_images, extract_markdown_links, text_to_textnodes, markdown_to_blocks

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_basic_split_code(self):
        node = TextNode("This is `code` here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_empty_nodes_at_edges(self):
        node = TextNode("`code`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_empty_node_between_delimiters(self):
        node = TextNode("text``more", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("text", TextType.TEXT),
            TextNode("", TextType.CODE),
            TextNode("more", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_no_delimiter_returns_original(self):
        node = TextNode("plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [node])

    def test_non_text_nodes_pass_through(self):
        non_text_node = TextNode("bold text", TextType.BOLD)
        result = split_nodes_delimiter([non_text_node], "`", TextType.CODE)
        self.assertEqual(result, [non_text_node])

    def test_unmatched_delimiter_raises(self):
        node = TextNode("bad `code", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_multiple_nodes_combined(self):
        nodes = [
            TextNode("start `code` ", TextType.TEXT),
            TextNode("and **bold** text", TextType.TEXT),
        ]
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("start ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

class TestMarkdownSplitting(unittest.TestCase):

    # -- Tests for split_nodes_image --

    def test_split_images_basic(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertListEqual(expected, split_nodes_image([node]))

    def test_split_images_duplicates(self):
        node = TextNode(
            "Repeat ![img](url) and ![img](url) again ![img](url)",
            TextType.TEXT,
        )
        expected = [
            TextNode("Repeat ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url"),
            TextNode(" again ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url"),
        ]
        self.assertListEqual(expected, split_nodes_image([node]))

    def test_split_images_edge_cases(self):
        # Image at the start
        node1 = TextNode("![start](url) text after", TextType.TEXT)
        expected1 = [
            TextNode("start", TextType.IMAGE, "url"),
            TextNode(" text after", TextType.TEXT),
        ]
        self.assertListEqual(expected1, split_nodes_image([node1]))

        # Image at the end
        node2 = TextNode("text before ![end](url)", TextType.TEXT)
        expected2 = [
            TextNode("text before ", TextType.TEXT),
            TextNode("end", TextType.IMAGE, "url"),
        ]
        self.assertListEqual(expected2, split_nodes_image([node2]))

    def test_split_images_no_images(self):
        node = TextNode("Just some normal text with no images.", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_images_non_text_nodes(self):
        # Nodes that are not TextType.TEXT should pass through untouched
        non_text_node = TextNode("bold text", TextType.BOLD)
        self.assertListEqual([non_text_node], split_nodes_image([non_text_node]))

    def test_split_images_empty_text_node(self):
        # Empty text nodes should not appear in output
        node = TextNode("", TextType.TEXT)
        self.assertListEqual([], split_nodes_image([node]))


    # -- Tests for split_nodes_link --

    def test_split_links_basic(self):
        node = TextNode(
            "Check [this link](https://example.com) and [another](https://test.com)",
            TextType.TEXT,
        )
        expected = [
            TextNode("Check ", TextType.TEXT),
            TextNode("this link", TextType.LINK, "https://example.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("another", TextType.LINK, "https://test.com"),
        ]
        self.assertListEqual(expected, split_nodes_link([node]))

    def test_split_links_duplicates(self):
        node = TextNode(
            "Links: [same](url) and [same](url) again [same](url)",
            TextType.TEXT,
        )
        expected = [
            TextNode("Links: ", TextType.TEXT),
            TextNode("same", TextType.LINK, "url"),
            TextNode(" and ", TextType.TEXT),
            TextNode("same", TextType.LINK, "url"),
            TextNode(" again ", TextType.TEXT),
            TextNode("same", TextType.LINK, "url"),
        ]
        self.assertListEqual(expected, split_nodes_link([node]))

    def test_split_links_edge_cases(self):
        # Link at the start
        node1 = TextNode("[start](url) is a link", TextType.TEXT)
        expected1 = [
            TextNode("start", TextType.LINK, "url"),
            TextNode(" is a link", TextType.TEXT),
        ]
        self.assertListEqual(expected1, split_nodes_link([node1]))

        # Link at the end
        node2 = TextNode("Link at end [end](url)", TextType.TEXT)
        expected2 = [
            TextNode("Link at end ", TextType.TEXT),
            TextNode("end", TextType.LINK, "url"),
        ]
        self.assertListEqual(expected2, split_nodes_link([node2]))

    def test_split_links_no_links(self):
        node = TextNode("No links here, just text.", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_split_links_non_text_nodes(self):
        non_text_node = TextNode("italic text", TextType.ITALIC)
        self.assertListEqual([non_text_node], split_nodes_link([non_text_node]))

    def test_split_links_empty_text_node(self):
        node = TextNode("", TextType.TEXT)
        self.assertListEqual([], split_nodes_link([node]))

#testing for markdown extractors
class TestMarkdownExtractors(unittest.TestCase):

    def test_extract_markdown_images_basic(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_multiple(self):
        text = "Images: ![one](url1) and ![two](url2)"
        expected = [("one", "url1"), ("two", "url2")]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_empty_alt(self):
        text = "![ ](emptyalt.png) and ![](emptyalt2.png)"
        expected = [(" ", "emptyalt.png"), ("", "emptyalt2.png")]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_no_match(self):
        text = "No images here !notimage(text)"
        self.assertListEqual(extract_markdown_images(text), [])

    def test_extract_markdown_links_basic(self):
        text = "Here is a [link](http://example.com)"
        expected = [("link", "http://example.com")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_multiple(self):
        text = "Links: [one](url1) and [two](url2)"
        expected = [("one", "url1"), ("two", "url2")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_empty_text(self):
        text = "[ ](emptytext.com) and [](emptytext2.com)"
        expected = [(" ", "emptytext.com"), ("", "emptytext2.com")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_links_do_not_match_images(self):
        text = "Image ![alt](url) and link [alt](url)"
        expected_images = [("alt", "url")]
        expected_links = [("alt", "url")]
        self.assertListEqual(extract_markdown_images(text), expected_images)
        self.assertListEqual(extract_markdown_links(text), expected_links)


class TestTextToTextNodes(unittest.TestCase):

    def assertTextNodeEqual(self, node, expected_text, expected_type, expected_url=None):
        self.assertEqual(node.text, expected_text)
        self.assertEqual(node.text_type, expected_type)
        if expected_url is not None:
            self.assertEqual(node.url, expected_url)
        else:
            self.assertFalse(hasattr(node, "url"))

    def test_basic_text(self):
        text = "Just some plain text."
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertTextNodeEqual(nodes[0], text, TextType.TEXT)

    def test_bold_and_italic(self):
        text = "This is **bold** and _italic_."
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 5)
        self.assertTextNodeEqual(nodes[0], "This is ", TextType.TEXT)
        self.assertTextNodeEqual(nodes[1], "bold", TextType.BOLD)
        self.assertTextNodeEqual(nodes[2], " and ", TextType.TEXT)
        self.assertTextNodeEqual(nodes[3], "italic", TextType.ITALIC)
        self.assertTextNodeEqual(nodes[4], ".", TextType.TEXT)

    def test_code_block(self):
        text = "Here is `code` example."
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertTextNodeEqual(nodes[0], "Here is ", TextType.TEXT)
        self.assertTextNodeEqual(nodes[1], "code", TextType.CODE)
        self.assertTextNodeEqual(nodes[2], " example.", TextType.TEXT)

    def test_image(self):
        text = "Look at this ![alt text](https://img.com/pic.png) image."
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertTextNodeEqual(nodes[0], "Look at this ", TextType.TEXT)
        self.assertTextNodeEqual(nodes[1], "alt text", TextType.IMAGE, "https://img.com/pic.png")
        self.assertTextNodeEqual(nodes[2], " image.", TextType.TEXT)

    def test_link(self):
        text = "Go to [Boot.dev](https://boot.dev) now."
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertTextNodeEqual(nodes[0], "Go to ", TextType.TEXT)
        self.assertTextNodeEqual(nodes[1], "Boot.dev", TextType.LINK, "https://boot.dev")
        self.assertTextNodeEqual(nodes[2], " now.", TextType.TEXT)

    def test_mixed(self):
        text = ("**Bold** and _italic_ with `code` plus ![img](http://img.com) "
                "and a [link](https://link.com).")
        nodes = text_to_textnodes(text)
        expected = [
            ("Bold", TextType.BOLD, None),
            (" and ", TextType.TEXT, None),
            ("italic", TextType.ITALIC, None),
            (" with ", TextType.TEXT, None),
            ("code", TextType.CODE, None),
            (" plus ", TextType.TEXT, None),
            ("img", TextType.IMAGE, "http://img.com"),
            (" and a ", TextType.TEXT, None),
            ("link", TextType.LINK, "https://link.com"),
            (".", TextType.TEXT, None),
        ]

        # The first node will be empty text if your code creates that, so skip empty TEXT nodes
        filtered_nodes = [n for n in nodes if not (n.text_type == TextType.TEXT and n.text == "")]
        self.assertEqual(len(filtered_nodes), len(expected))
        for node, (exp_text, exp_type, exp_url) in zip(filtered_nodes, expected):
            self.assertTextNodeEqual(node, exp_text, exp_type, exp_url)

#testing for markdown to blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_leading_and_trailing_newlines(self):
        md = """

# Heading

Content here

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Content here"
            ],
        )

    def test_multiple_blank_lines_between_blocks(self):
        md = """
First block


Second block



Third block
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block",
                "Second block",
                "Third block",
            ],
        )

    def test_single_block(self):
        md = """Just one paragraph with no blank lines."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Just one paragraph with no blank lines."]
        )

    def test_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])





# Run the tests

if __name__ == "__main__":
    unittest.main()