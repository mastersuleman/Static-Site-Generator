from htmlnode import LeafNode
from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        if url is not None:
            self.url = url

    def __eq__(self, other):
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and getattr(self, "url", None) == getattr(other, "url", None)
        )

    def __repr__(self):
        url = getattr(self, "url", None)
        return f"TextNode({self.text}, {self.text_type.value}, {url})"


#def text_node_to_html_node(text_node):
#    if text_node.text_type == TextType.TEXT:
#        return LeafNode(None, text_node.text)
#    if text_node.text_type == TextType.BOLD:
#        return LeafNode("b", text_node.text)
#    if text_node.text_type == TextType.ITALIC:
#        return LeafNode("i", text_node.text)
#    if text_node.text_type == TextType.CODE:
#        return LeafNode("code", text_node.text)
#    if text_node.text_type == TextType.LINK:
#        return LeafNode("a", text_node.text, {"href": text_node.url})
#    if text_node.text_type == TextType.IMAGE:
#        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
#    raise ValueError(f"invalid text type: {text_node.text_type}")
