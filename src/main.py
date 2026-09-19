import os
import shutil

from textnode import TextNode, TextType
from text_block import markdown_to_html_node

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


def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("no first header found!")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as file:
        markdown = file.read()

    with open(template_path, "r") as file:
        template = file.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html)
    directory = os.path.dirname(dest_path)

    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    with open(dest_path, "w") as file:
        file.write(full_html)


def main():
    copy_static("static", "public")
    print(TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev"))
    #testing some stuff
    generate_page("content/index.md", "template.html", "public/index.html")
    #end of testing block

if __name__ == "__main__":
    main()