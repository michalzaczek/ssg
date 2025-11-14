import sys

from utilities import (
    copy_files,
    delete_from_folder,
    generate_pages_recursive,
)


def main():
    # Get basepath from CLI argument, default to "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    delete_from_folder("public")
    copy_files("static", "public")
    generate_pages_recursive("content", "template.html", "public", basepath)


if __name__ == "__main__":
    main()
