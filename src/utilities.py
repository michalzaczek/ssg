import os
import shutil


def delete_from_folder(folder_path):
    # Delete the public directory if it exists
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    # Recreate the public directory
    os.makedirs(folder_path)
