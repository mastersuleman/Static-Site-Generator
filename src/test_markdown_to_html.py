import unittest
from markdown_to_html import markdown_to_html_node

class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_paragraphs(self):
        md = (
            "This is **bolded** paragraph\n"
            "text in a p\n"
            "tag here\n\n"
            "This is another paragraph with _italic_ text and `code` here\n"
        )
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = (
            "```\n"
            "This is text that _should_ remain\n"
            "the **same** even with inline stuff\n"
            "```\n"
        )
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading_and_quote(self):
        md = (
            "# Heading One\n\n"
            "> Quoted text line\n"
            "> continued quote\n"
        )
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading One</h1><blockquote>Quoted text line continued quote</blockquote></div>",
        )

    def test_unordered_list(self):
        md = (
            "- First bullet\n"
            "- Second bullet\n"
        )
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First bullet</li><li>Second bullet</li></ul></div>",
        )

    def test_ordered_list(self):
        md = (
            "1. First\n"
            "2. Second\n"
        )
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First</li><li>Second</li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()
