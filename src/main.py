from utilities import (
    copy_files,
    delete_from_folder,
    generate_pages_recursive,
)


def main():
    delete_from_folder("public")
    copy_files("static", "public")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
