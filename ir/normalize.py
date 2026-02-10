# ir/normalize.py

class IRNormalizer:
    def __init__(self):
        self.var_map = {}
        self.func_map = {}
        self.class_map = {}
        self.var_count = 0
        self.func_count = 0
        self.class_count = 0

    def normalize(self, node):
        """
        Recursively normalize IR tree
        """
        # Normalize classes
        if node.node_type == "CLASS":
            if node.value not in self.class_map:
                self.class_count += 1
                self.class_map[node.value] = f"C{self.class_count}"
            node.value = self.class_map[node.value]

        # Normalize functions
        elif node.node_type == "FUNCTION":
            if node.value not in self.func_map:
                self.func_count += 1
                self.func_map[node.value] = f"f{self.func_count}"
            node.value = self.func_map[node.value]

        # Normalize variables
        elif node.node_type == "VAR" and not isinstance(node.value, (int, float)):
            if node.value not in self.var_map:
                self.var_count += 1
                self.var_map[node.value] = f"v{self.var_count}"
            node.value = self.var_map[node.value]

        # Normalize pointer ref / deref
        elif node.node_type in ("POINTER_REF", "POINTER_DEREF"):
            if node.value not in self.var_map:
                self.var_count += 1
                self.var_map[node.value] = f"v{self.var_count}"
            node.value = self.var_map[node.value]

        # Recurse
        for child in node.children:
            self.normalize(child)

        return node
