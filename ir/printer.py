# ir/printer.py

def print_ir(node, indent=0):
    """
    Pretty-print IR tree for debugging and demo
    """
    prefix = "  " * indent

    # Show node type and value clearly
    if node.value is not None:
        print(f"{prefix}{node.node_type} -> {node.value}")
    else:
        print(f"{prefix}{node.node_type}")

    for child in node.children:
        print_ir(child, indent + 1)
