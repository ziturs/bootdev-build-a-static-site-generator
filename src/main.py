import os
import shutil
import sys

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

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as file:
        markdown = file.read()

    with open(template_path, "r") as file:
        template = file.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html)

    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')
    directory = os.path.dirname(dest_path)

    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    with open(dest_path, "w") as file:
        file.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if os.path.exists(dir_path_content):
         content_directory = os.listdir(dir_path_content)
         for content_entry in content_directory:
            content_path = os.path.join(dir_path_content, content_entry)
            docs_path = os.path.join(dest_dir_path, content_entry)
            if os.path.isdir(content_path):
                generate_pages_recursive(content_path, template_path, docs_path, basepath)
            elif content_entry.endswith(".md"):
                path_with_no_ending, _ = os.path.splitext(docs_path)
                html_path = path_with_no_ending + ".html"
                generate_page(content_path, template_path, html_path, basepath)


def main():
    basepath = "/"

    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    copy_static("static", "docs")
    print(TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev"))
    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()