# plagiarism/subtree_match.py

from collections import Counter
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
    Compute subtree similarity using frequency-aware comparison
    """

    hashes1 = collect_subtree_hashes(tree1)
    hashes2 = collect_subtree_hashes(tree2)

    if not hashes1 or not hashes2:
        return 0.0

    # 🔥 Use frequency counts instead of sets
    counter1 = Counter(hashes1)
    counter2 = Counter(hashes2)

    # 🔥 Compute overlap (min frequency match)
    common = 0
    for h in counter1:
        if h in counter2:
            common += min(counter1[h], counter2[h])

    total = sum(counter1.values()) + sum(counter2.values())

    similarity = (2 * common) / total if total > 0 else 0.0

    return similarity
