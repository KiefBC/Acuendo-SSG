from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def __eq__(self, other):
        return super().__eq__(other)

    def to_html(self):
        if self.value is None:
            raise ValueError("Value cannot be None")

        if self.tag is None:
            return f"{self.value}"

        return f"<{self.tag}>{self.value}</{self.tag}>"
