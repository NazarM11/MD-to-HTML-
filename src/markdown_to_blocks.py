def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return_list = []
    for block in blocks:
        if block == "":
            continue
        return_list.append(block.strip())
    return return_list