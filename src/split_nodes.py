from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
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