from enum import Enum, auto

class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()

def block_to_block_type(block):
    lines = block.split('\n')

    # Code block: starts and ends with ```
    if block.startswith("```") and block.endswith("```") and len(lines) >= 2:
        return BlockType.CODE

    # Heading: starts with 1-6 # followed by a space
    if lines[0].startswith("#"):
        i = 0
        while i < len(lines[0]) and lines[0][i] == "#":
            i += 1
        if 1 <= i <= 6 and len(lines[0]) > i and lines[0][i] == " ":
            return BlockType.HEADING

    # Quote block: all lines start with >
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list: all lines start with "- "
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list: starts with 1. then 2. and so on
    ordered = True
    for idx, line in enumerate(lines):
        prefix = f"{idx + 1}. "
        if not line.startswith(prefix):
            ordered = False
            break
    if ordered:
        return BlockType.ORDERED_LIST

    # Default: paragraph
    return BlockType.PARAGRAPH
