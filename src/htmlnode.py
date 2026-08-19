class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list | None = None, props: dict | None = None): 
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self) -> str:
        raise NotImplementedError("to_html must be implemented by subclasses")


    def props_to_html(self):
        if self.props is None:
            return ""

        html_string = ''

        for prop_key, prop_value in self.props.items():
            html_string += (' ' + prop_key + '="' + prop_value + '"')

        return html_string

    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict | None = None): 
        super().__init__(
            tag = tag, 
            value = value, 
            children = None, 
            props = props,
            )

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value!")
        if not self.tag:
            return self.value
        
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
