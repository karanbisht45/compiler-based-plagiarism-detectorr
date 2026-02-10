# plagiarism/subtree_match.py

from plagiarism.tree_hash import hash_node

def collect_subtree_hashes(node, hashes=None):
    """
    Collect hashes of all subtrees rooted at every node
    """
    if hashes is None:
        hashes = []

    # Hash current subtree
    hashes.append(hash_node(node))

    # Recurse
    for child in node.children:
        collect_subtree_hashes(child, hashes)

    return hashes

def subtree_similarity(tree1, tree2):
    """
    Compute subtree similarity between two IR trees
    """
    hashes1 = collect_subtree_hashes(tree1)
    hashes2 = collect_subtree_hashes(tree2)

    set1 = set(hashes1)
    set2 = set(hashes2)

    if not set1 or not set2:
        return 0.0

    common = set1.intersection(set2)
    similarity = (2 * len(common)) / (len(set1) + len(set2))

    return similarity
