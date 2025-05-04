from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def __eq__(self, other):
        return super().__eq__(other)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag cannot be None")

        if self.children is None:
            raise ValueError("Children cannot be None")

        children_html = ''.join(child.to_html() if isinstance(child, HTMLNode) else str(child)
                                for child in self.children)

        props_html = self.props_to_html()
        props_str = f" {props_html}" if props_html else ""

        return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"
