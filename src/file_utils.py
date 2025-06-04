import os
import shutil

def clear_directory(path):
    """Delete all contents inside the directory at path."""
    if not os.path.exists(path):
        return
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            shutil.rmtree(full_path)
        else:
            os.remove(full_path)

def copy_recursive(src, dst):
    """Copy all contents from src directory to dst directory recursively."""
    # First clear destination directory
    if os.path.exists(dst):
        clear_directory(dst)
    else:
        os.makedirs(dst)

    def copy_dir(src_dir, dst_dir):
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for item in os.listdir(src_dir):
            s = os.path.join(src_dir, item)
            d = os.path.join(dst_dir, item)
            if os.path.isdir(s):
                copy_dir(s, d)
            else:
                shutil.copy2(s, d)
                print(f"Copied file: {d}")

    copy_dir(src, dst)
