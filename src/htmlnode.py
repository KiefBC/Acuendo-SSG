class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self, indent_level=0, format_output=False):
        raise NotImplementedError("to_html() must be implemented by subclasses")

    def props_to_html(self):
        if self.props is None:
            return ""
        else:
            return " ".join([f"{key}={value}" for key, value in self.props.items()])
