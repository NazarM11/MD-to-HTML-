class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html must be implemented by subclasses")
    
    def props_to_html(self):
        if not self.props:
            return ""
        
        return_string = ""
        for k, v in self.props.items(): 
            return_string += f' {k}="{v}"'

        return return_string 
    
    def __repr__(self):
        print(f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})")

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, props = None)
        self.tag = tag
        self.value = value
        self.props = props
    
    def to_html(self):
        if self.value is None:
            raise ValueError("This node has no value")
        if not self.tag:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        print(f"HTMLNode({self.tag}, {self.value}, {self.props})")

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, children, props = None)
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if not self.tag:
            raise ValueError("No tag")
        if not self.children:
            raise ValueError("No children found")
        return_string = f'<{self.tag}{self.props_to_html()}>' 
        for child in self.children:
            return_string += child.to_html()
        return return_string + f'</{self.tag}>'