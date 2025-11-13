from utilities import copy_files, delete_from_folder


def main():
    delete_from_folder("public")
    copy_files("static", "public")


if __name__ == "__main__":
    main()
