import os
from markdown_to_html import markdown_to_html_node
from extract_title import extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read markdown content
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Read template content
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    # Convert markdown to HTML string using your existing functions
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Extract title
    title = extract_title(markdown_content)

    # Replace placeholders in template
    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write output HTML
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                rel_path = os.path.relpath(root, dir_path_content)
                from_path = os.path.join(root, file)

                dest_dir = os.path.join(dest_dir_path, rel_path)
                os.makedirs(dest_dir, exist_ok=True)

                file_name = os.path.splitext(file)[0] + ".html"
                dest_path = os.path.join(dest_dir, file_name)

                print(f"Generating page from {from_path} to {dest_path} using {template_path}")
                generate_page(from_path, template_path, dest_path)
