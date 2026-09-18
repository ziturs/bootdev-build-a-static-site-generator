import os
import shutil

from textnode import TextNode, TextType


def copy_static(source, destination):
    if os.path.exists(source):

        if os.path.exists(destination):

            shutil.rmtree(destination)

        os.mkdir(destination)
        copies = os.listdir(source)

        for copy in copies:

            source_path = os.path.join(source, copy) 
            destination_path = os.path.join(destination, copy)

            if os.path.isfile(source_path):

                shutil.copy(source_path, destination_path)
                continue

            copy_static(source_path, destination_path)


def main():
    copy_static("static", "public")
    print(TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev"))
    #testing some stuff
    print(os.getcwd())
    print(os.listdir("static"))
    print(os.listdir("public"))
    #end of testing block

if __name__ == "__main__":
    main()