def extract_title(markdown):
    for line in markdown.splitlines():
        line = line.strip()
        if line.startswith("# "):  # line starts with a single # and a space
            return line[2:].strip()  # return text after "# "
    raise ValueError("No H1 header found in the markdown")
