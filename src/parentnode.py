from .htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def __eq__(self, other):
        return super().__eq__(other)

    def to_html(self, indent_level=0, format_output=False):
        if self.tag is None:
            raise ValueError("Tag cannot be None")

        if self.children is None:
            raise ValueError("Children cannot be None")

        indent = "  " * indent_level if format_output else ""
        next_indent = "  " * (indent_level + 1) if format_output else ""
        line_break = "\n" if format_output else ""

        if format_output:
            children_html = line_break.join(
                next_indent + (child.to_html(indent_level + 1, format_output) if isinstance(child, HTMLNode) else str(child))
                for child in self.children
            )
        else:
            children_html = "".join(
                child.to_html(indent_level + 1, format_output) if isinstance(child, HTMLNode) else str(child)
                for child in self.children
            )

        props_html = self.props_to_html()
        props_str = f" {props_html}" if props_html else ""

        if children_html:
            if format_output:
                return f"{indent}<{self.tag}{props_str}>{line_break}{children_html}{line_break}{indent}</{self.tag}>"
            else:
                return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"
        else:
            return f"{indent}<{self.tag}{props_str}></{self.tag}>"
