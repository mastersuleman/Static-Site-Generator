import os
import sys
from file_utils import copy_recursive, clear_directory
from page_generator import generate_pages_recursive

def main():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    static_dir = os.path.join(BASE_DIR, "static")
    output_dir = os.path.join(BASE_DIR, "docs")
    content_dir = os.path.join(BASE_DIR, "content")
    template_html = os.path.join(BASE_DIR, "template.html")
    
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"

    print(f"Cleaning output directory: {output_dir}")
    clear_directory(output_dir)
    
    print(f"Copying static files from {static_dir} to {output_dir}")
    copy_recursive(static_dir, output_dir)
    
    print(f"Generating pages from {content_dir} using template {template_html} with basepath {base_path}")
    generate_pages_recursive(content_dir, template_html, output_dir, base_path)

if __name__ == "__main__":
    main()
