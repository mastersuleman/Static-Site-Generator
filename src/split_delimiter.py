import re
from textnode import TextNode, TextType

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = [node for node in nodes if node.text != ""]
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            # If the node is not a text node, append it directly
            result.append(node)
            continue
        
        if delimiter not in node.text:
            # If the delimiter is not found, append the node as is
            result.append(node)
            continue

        # Split the text node by the delimiter
        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter {delimiter!r} in {node.text!r}")
        
        for i, part in enumerate(parts):
            if i % 2 == 0:
                result.append(TextNode(part, TextType.TEXT))
            else:
                result.append(TextNode(part, text_type))

    return result

#split images and links

def split_nodes_image(old_nodes):
    result = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            result.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)

        if not images:
            if text != "":
                result.append(node)
            continue

        # Process first image only
        alt, url = images[0]
        md_image = f"![{alt}]({url})"

        # Split once at first occurrence
        before, after = text.split(md_image, 1)

        if before != "":
            result.append(TextNode(before, TextType.TEXT))

        result.append(TextNode(alt, TextType.IMAGE, url))

        # Recurse on the remaining text after the first image
        result.extend(split_nodes_image([TextNode(after, TextType.TEXT)]))

    return result


def split_nodes_link(old_nodes):
    result = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            result.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)

        if not links:
            if text != "":
                result.append(node)
            continue

        text_link, url = links[0]
        md_link = f"[{text_link}]({url})"

        before, after = text.split(md_link, 1)

        if before != "":
            result.append(TextNode(before, TextType.TEXT))

        result.append(TextNode(text_link, TextType.LINK, url))

        result.extend(split_nodes_link([TextNode(after, TextType.TEXT)]))

    return result

# Extracting markdown images and links from text
def extract_markdown_images(text):
    """
    Extract all markdown images of the form ![alt text](url)
    Returns a list of tuples: (alt_text, url)
    """
    pattern = r'!\[([^\]]*?)\]\((.*?)\)'
    return re.findall(pattern, text)

def extract_markdown_links(text):
    """
    Extract all markdown links of the form [anchor text](url)
    Returns a list of tuples: (anchor_text, url)
    """
    # Make sure not to match images, which start with '!'
    pattern = r'(?<!\!)\[([^\]]*?)\]\((.*?)\)'
    return re.findall(pattern, text)


#markdown to blocks
def markdown_to_blocks(markdown):
    raw_blocks = re.split(r"\n\s*\n", markdown)
    blocks = [block.strip() for block in raw_blocks if block.strip() != ""]
    return blocks