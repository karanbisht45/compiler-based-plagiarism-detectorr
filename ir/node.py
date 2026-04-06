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

    # 🔥 NEW: Structural equality
    def __eq__(self, other):
        if not isinstance(other, IRNode):
            return False

        if self.node_type != other.node_type:
            return False

        if self.value != other.value:
            return False

        if len(self.children) != len(other.children):
            return False

        for c1, c2 in zip(self.children, other.children):
            if c1 != c2:
                return False

        return True

    # 🔥 NEW: Hash (for sets / fast comparison)
    def __hash__(self):
        return hash((
            self.node_type,
            self.value,
            tuple(self.children)
        ))
