import os
from file_utils import copy_recursive, clear_directory
from page_generator import generate_pages_recursive

def main():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # two levels up to root

    static_dir = os.path.join(BASE_DIR, "static")
    public_dir = os.path.join(BASE_DIR, "public")
    content_dir = os.path.join(BASE_DIR, "content")
    template_html = os.path.join(BASE_DIR, "template.html")

    print(f"Cleaning public directory: {public_dir}")
    clear_directory(public_dir)

    print(f"Copying static files from {static_dir} to {public_dir}")
    copy_recursive(static_dir, public_dir)

    print(f"Generating pages from {content_dir} to {public_dir} using {template_html}")
    generate_pages_recursive(content_dir, template_html, public_dir)

if __name__ == "__main__":
    main()
