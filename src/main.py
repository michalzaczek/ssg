from utilities import copy_files, delete_from_folder, generate_page


def main():
    delete_from_folder("public")
    copy_files("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
