class BlockType:
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown: str):
    return [
        block.strip()
        for block in markdown.strip().split("\n\n")
        if block.strip()
    ]


def block_to_block_type(block: str) -> str:
    lines = block.split("\n")
    if block.startswith(("#", "##", "###", "####", "#####", "######")):
        return BlockType.HEADING

    code_block = block.split("```")
    if code_block[0] == "" and code_block[-1] == "":
        return BlockType.CODE

    if block.startswith("1."):
        for index, line in enumerate(lines):
            if not line.startswith(f"{index + 1}."):
                return BlockType.PARAGRAPH
        return BlockType.OLIST

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    return BlockType.PARAGRAPH
