# ir/node.py

class IRNode:
    def __init__(self, node_type, value=None):
        """
        node_type: string (e.g., IF, ASSIGN, CLASS)
        value: operator, name, literal, etc.
        """
        self.node_type = node_type
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"{self.node_type}({self.value})"
