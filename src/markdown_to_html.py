from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType
from converters import text_node_to_html_node
from block_markdown import block_to_block_type, BlockType
from split_delimiter import markdown_to_blocks, text_to_textnodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.CODE:
            code_content = block.strip("`")
            if code_content.startswith("\n"):
                code_content = code_content[1:]
            code_node = LeafNode("code", code_content)
            html_node = ParentNode("pre", [code_node])


        elif block_type == BlockType.QUOTE:
            quote_lines = [line[1:].strip() for line in block.splitlines()]
            quote_text = " ".join(quote_lines)
            inline_nodes = text_to_textnodes(quote_text)
            child_nodes = [text_node_to_html_node(n) for n in inline_nodes]
            html_node = ParentNode("blockquote", child_nodes)

        elif block_type == BlockType.UNORDERED_LIST:
            html_node = handle_list_block(block, ordered=False)

        elif block_type == BlockType.ORDERED_LIST:
            html_node = handle_list_block(block, ordered=True)

        elif block_type == BlockType.PARAGRAPH:
            paragraph_text = " ".join(line.strip() for line in block.splitlines())
            inline_nodes = text_to_textnodes(paragraph_text)
            child_nodes = [text_node_to_html_node(n) for n in inline_nodes]
            html_node = ParentNode("p", child_nodes)

        elif block_type == BlockType.HEADING:
            first_space = block.find(" ")
            if first_space == -1:
                level = len(block)
                content = ""
            else:
                level = block.count("#", 0, first_space)
                content = block[first_space:].strip()
            inline_nodes = text_to_textnodes(content)
            child_nodes = [text_node_to_html_node(n) for n in inline_nodes]
            html_node = ParentNode(f"h{level}", child_nodes)

        else:
            raise ValueError(f"Unsupported block type: {block_type}")

        children.append(html_node)

    return ParentNode("div", children)

def handle_list_block(block, ordered=False):
    lines = block.splitlines()
    tag = "ol" if ordered else "ul"
    children = []

    for line in lines:
        if ordered:
            line = line.split(". ", 1)[-1]
        else:
            line = line[2:]

        inline_nodes = text_to_textnodes(line.strip())
        li_children = [text_node_to_html_node(n) for n in inline_nodes]
        children.append(ParentNode("li", li_children))

    return ParentNode(tag, children)
