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

        # -------------------------
        # CLASS NORMALIZATION
        # -------------------------
        if node.node_type == "CLASS":
            if node.value not in self.class_map:
                self.class_count += 1
                self.class_map[node.value] = f"C{self.class_count}"
            node.value = self.class_map[node.value]

        # -------------------------
        # FUNCTION NORMALIZATION
        # -------------------------
        elif node.node_type == "FUNCTION":
            if node.value not in self.func_map:
                self.func_count += 1
                self.func_map[node.value] = f"f{self.func_count}"
            node.value = self.func_map[node.value]

        # -------------------------
        # VARIABLE NORMALIZATION
        # -------------------------
        elif node.node_type in ("VAR", "POINTER_REF", "POINTER_DEREF"):
            if not isinstance(node.value, (int, float)):
                if node.value not in self.var_map:
                    self.var_count += 1
                    self.var_map[node.value] = f"v{self.var_count}"
                node.value = self.var_map[node.value]

        # -------------------------
        # RECURSIVE NORMALIZATION
        # -------------------------
        for child in node.children:
            self.normalize(child)

        return node

    # 🔥 NEW: Reset normalizer (important for consistency)
    def reset(self):
        self.var_map.clear()
        self.func_map.clear()
        self.class_map.clear()
        self.var_count = 0
        self.func_count = 0
        self.class_count = 0
