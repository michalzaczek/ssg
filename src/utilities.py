import os
import shutil


def delete_from_folder(folder_path):
    # Delete the public directory if it exists
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    # Recreate the public directory
    os.makedirs(folder_path)


def copy_files(from_path, to_path):
    dir = os.listdir(from_path)

    if not os.path.exists(to_path):
        os.mkdir(to_path)

    for item in dir:
        item_path = os.path.join(from_path, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, to_path)
        else:
            new_to_path = os.path.join(to_path, item)
            copy_files(item_path, new_to_path)
