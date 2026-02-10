# ir/printer.py

def print_ir(node, indent=0):
    print("  " * indent + f"{node.node_type}: {node.value}")
    for child in node.children:
        print_ir(child, indent + 1)
