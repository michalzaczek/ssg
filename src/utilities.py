import os
import shutil

from textnode import markdown_to_html_node


def delete_from_folder(folder_path):
    # Delete the public directory if it exists
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    # Recreate the public directory
    os.makedirs(folder_path)


def copy_files(from_path, dest_path):
    dir = os.listdir(from_path)

    if not os.path.exists(dest_path):
        os.mkdir(dest_path)

    for item in dir:
        item_path = os.path.join(from_path, item)
        if os.path.isfile(item_path):
            print(f"Copying file: {item_path} -> {dest_path}")
            shutil.copy(item_path, dest_path)
        else:
            new_dest_path = os.path.join(dest_path, item)
            copy_files(item_path, new_dest_path)


def extract_title(markdown):
    """
    Extract the h1 header from markdown text.
    """
    lines = markdown.split("\n")
    for line in lines:
        stripped = line.strip()
        # Check if line starts with '#' but not '##' (h1 only, not h2+)
        if stripped.startswith("#") and not stripped.startswith("##"):
            # Remove the '#' and any whitespace after it
            title = stripped[1:].strip()
            return title
    raise Exception("Error: No h1 header found in markdown")


def generate_page(from_path, template_path, dest_path, basepath="/"):
    """
    Generate an HTML page from a markdown file using a template.
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        md = file.read()

    with open(template_path, "r") as file:
        template = file.read()

    html_node = markdown_to_html_node(md)
    html_str = html_node.to_html()
    title = extract_title(md)

    new_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_str)

    # Ensure basepath ends with / if it's not just "/"
    if basepath != "/" and not basepath.endswith("/"):
        basepath = basepath + "/"

    # Replace URL paths with basepath
    new_html = new_html.replace('href="/', f'href="{basepath}')
    new_html = new_html.replace('src="/', f'src="{basepath}')

    # Create necessary directories if they don't exist
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as file:
        file.write(new_html)


def generate_pages_recursive(
    dir_path_content, template_path, dest_dir_path, basepath="/"
):
    """
    Recursively generate HTML pages from markdown files in a directory.
    """
    dir = os.listdir(dir_path_content)

    for item in dir:
        item_path = os.path.join(dir_path_content, item)
        new_dest_dir_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(item_path) and item_path.endswith(".md"):
            # Replace the .md extension with .html
            html_path = os.path.splitext(new_dest_dir_path)[0] + ".html"
            generate_page(item_path, template_path, html_path, basepath)

        elif os.path.isdir(item_path):
            generate_pages_recursive(
                item_path, template_path, new_dest_dir_path, basepath
            )
