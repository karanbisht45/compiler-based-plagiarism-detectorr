# plagiarism/tree_hash.py

import hashlib

def hash_node(node):
    """
    Recursively compute hash of an IR node
    """
    hasher = hashlib.sha256()

    # Include node type
    hasher.update(node.node_type.encode())

    # Include value if exists
    if node.value is not None:
        hasher.update(str(node.value).encode())

    # Hash children
    for child in node.children:
        child_hash = hash_node(child)
        hasher.update(child_hash.encode())

    return hasher.hexdigest()
