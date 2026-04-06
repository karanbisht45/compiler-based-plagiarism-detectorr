# ir/cfg.py

class CFGNode:
    def __init__(self, label):
        self.label = label
        self.next = []

    def add_edge(self, node):
        # 🔥 Prevent duplicate edges
        if node not in self.next:
            self.next.append(node)

    def __repr__(self):
        return f"CFGNode({self.label})"


def build_cfg(ir_node):
    """
    Build CFG from IR tree.
    Returns (entry_node, exit_nodes)
    """

    # 🔥 Use more informative label
    label = ir_node.node_type
    if ir_node.value:
        label += f"({ir_node.value})"

    entry = CFGNode(label)

    # -------------------------
    # PROGRAM / BLOCK / FUNCTION / CLASS
    # -------------------------
    if ir_node.node_type in ("PROGRAM", "BLOCK", "FUNCTION", "CLASS"):
        prev_exits = [entry]

        for child in ir_node.children:
            child_entry, child_exits = build_cfg(child)
            for pe in prev_exits:
                pe.add_edge(child_entry)
            prev_exits = child_exits

        return entry, prev_exits

    # -------------------------
    # IF STATEMENT
    # -------------------------
    if ir_node.node_type == "IF":
        cond_node = CFGNode("IF_COND")
        entry.add_edge(cond_node)

        then_entry, then_exits = build_cfg(ir_node.children[1])
        cond_node.add_edge(then_entry)

        exit_nodes = []

        if len(ir_node.children) > 2:
            else_entry, else_exits = build_cfg(ir_node.children[2])
            cond_node.add_edge(else_entry)
            exit_nodes.extend(then_exits + else_exits)
        else:
            exit_nodes.extend(then_exits)
            exit_nodes.append(cond_node)

        return entry, exit_nodes

    # -------------------------
    # WHILE / FOR LOOP
    # -------------------------
    if ir_node.node_type in ("WHILE", "FOR"):
        loop_cond = CFGNode("LOOP_COND")
        entry.add_edge(loop_cond)

        body_entry, body_exits = build_cfg(ir_node.children[1])
        loop_cond.add_edge(body_entry)

        for be in body_exits:
            be.add_edge(loop_cond)  # loop back

        return entry, [loop_cond]

    # -------------------------
    # SIMPLE STATEMENT
    # -------------------------
    return entry, [entry]
