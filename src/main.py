import os, shutil
from copystatic import copy_source_to_dest
from markdown_html_node import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"



def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    print("Copying static files to public directory...")
    copy_source_to_dest(dir_path_static, dir_path_public)

    generate_pages_recursive("./content", "./template.html", "./public")


if __name__ == "__main__":
    main()

