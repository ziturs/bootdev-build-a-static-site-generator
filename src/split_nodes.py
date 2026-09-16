import re

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_text = old_node.text.split(delimiter)

        if len(split_text) % 2 == 0:
            raise Exception(f"Unclosed delimiter: {delimiter}")

        for index, text in enumerate(split_text):
            if index % 2 == 0:
                new_node = TextNode(text, TextType.TEXT)
            else:
                new_node = TextNode(text, text_type)
            new_nodes.append(new_node)
    return new_nodes


def extract_markdown_images(markdown: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", markdown)
    return matches


def extract_markdown_links(markdown: str) -> list[tuple[str, str]]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", markdown)
    return matches


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)
        remaining_text = old_node.text

        for alt, url in images:
            image = f"![{alt}]({url})"
            parts = remaining_text.split(image, 1)

            if parts[0]:
                parts_node = TextNode(parts[0], TextType.TEXT)
                new_nodes.append(parts_node)

            image_node = TextNode(alt, TextType.IMAGE, url)
            new_nodes.append(image_node)
            remaining_text = parts[1]

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)
        remaining_text = old_node.text

        for text, url in links:
            links = f"[{text}]({url})"
            parts = remaining_text.split(links, 1)

            if parts[0]:
                parts_node = TextNode(parts[0], TextType.TEXT)
                new_nodes.append(parts_node)

            link_node = TextNode(text, TextType.LINK, url)
            new_nodes.append(link_node)
            remaining_text = parts[1]

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
