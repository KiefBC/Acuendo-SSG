from .htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def __eq__(self, other):
        return super().__eq__(other)

    def to_html(self, indent_level=0, format_output=False):
        indent = "  " * indent_level if format_output else ""

        if self.tag is None:
            if self.value is None:
                raise ValueError("Value cannot be None")
            return f"{self.value}"

        if self.tag == "img":
            props_html = self.props_to_html()
            props_str = f" {props_html}" if props_html else ""
            return f"{indent}<{self.tag}{props_str} />"  # self-closing tag

        props_html = self.props_to_html()
        props_str = f" {props_html}" if props_html else ""

        return f"{indent}<{self.tag}{props_str}>{self.value}</{self.tag}>"
