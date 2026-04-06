# plagiarism/tree_hash.py

import hashlib

def hash_node(node):
    """
    Recursively compute hash of an IR node
    (order-aware but stable)
    """

    hasher = hashlib.sha256()

    # Include node type
    hasher.update(node.node_type.encode())

    # Include value if exists
    if node.value is not None:
        hasher.update(str(node.value).encode())

    # 🔥 Collect child hashes first
    child_hashes = [hash_node(child) for child in node.children]

    # 🔥 Sort child hashes (important improvement)
    child_hashes.sort()

    for ch in child_hashes:
        hasher.update(ch.encode())

    return hasher.hexdigest()
