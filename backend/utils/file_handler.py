import os
import shutil

def move_file_to_category(file_path: str, label: str, upload_root: str) -> str:
    category_dir = os.path.join(upload_root, label)
    os.makedirs(category_dir, exist_ok=True)

    final_path = os.path.join(category_dir, os.path.basename(file_path))
    shutil.move(file_path, final_path)
    return final_path
