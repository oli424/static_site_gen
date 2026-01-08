import os, shutil
from copystatic import copy_source_to_dest
from markdown_html_node import generate_page

dir_path_static = "./static"
dir_path_public = "./public"



def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    print("Copying static files to public directory...")
    copy_source_to_dest(dir_path_static, dir_path_public)

    generate_page("./content/index.md", "./template.html", "public/index.html")


if __name__ == "__main__":
    main()

