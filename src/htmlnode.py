class HTMLNode:
    def __init__(
        self, tag=None, value: str | None = None, children=None, props=None
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == None:
            return ""

        string = ""
        for key in self.props:
            string += f' {key}="{self.props[key]}"'

        return string

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("invalid HTML: no tag")

        if self.children == None:
            raise ValueError("invalid HTML: no tag")

        children_tags = ""
        for child in self.children:
            children_tags += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_tags}</{self.tag}>"
