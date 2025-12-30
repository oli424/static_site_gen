from textnode import TextType

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        attribute_string = f""
        if self.props is None:
            return None
        for key in self.props:
            attribute_string += f' {key}="{self.props[key]}"'
        return attribute_string
    
    def __repr__(self):
        return HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})


class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        
        tag = f"<{self.tag}>"
        closing = f"</{self.tag}>"
        if self.props == None:
            #print("None")
            return f"{tag}{self.value}{closing}"
        elif self.props != None:
            #print("Not None")
            props = self.props_to_html()
            return f"<{self.tag}{props}>{self.value}{closing}"
        

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("missing tag")
        if self.children == None:
            raise ValueError("missing children")
        
        children = ""
        for child in self.children:
            children += child.to_html()
        tag = f"<{self.tag}>"
        closing = f"</{self.tag}>"
        return f"{tag}{children}{closing}"
        

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("`", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception