import sys

from utilities import (
    copy_files,
    delete_from_folder,
    generate_pages_recursive,
)

PUBLIC_DIR = "docs"
CONTENT_DIR = "content"
STATIC_DIR = "static"
TEMPLATE_FILE = "template.html"


def main():
    # Get basepath from CLI argument, default to "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    delete_from_folder(PUBLIC_DIR)
    copy_files(STATIC_DIR, PUBLIC_DIR)
    generate_pages_recursive(CONTENT_DIR, TEMPLATE_FILE, PUBLIC_DIR, basepath)


if __name__ == "__main__":
    main()
