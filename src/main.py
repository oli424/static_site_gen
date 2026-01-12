import os, shutil, sys
from copystatic import copy_source_to_dest
from markdown_html_node import generate_pages_recursive

dir_path_static = "./static"
dir_path_docs = "./docs"



def main():
    print("Deleting docs directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)
    print("Copying static files to docs directory...")
    copy_source_to_dest(dir_path_static, dir_path_docs)

    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)

    


if __name__ == "__main__":
    main()

