# plagiarism/cfg_similarity.py

def extract_cfg_features(entry_node, visited=None, features=None):
    """
    Extract structural features from CFG
    """
    if visited is None:
        visited = set()
    if features is None:
        features = []

    if entry_node in visited:
        return features

    visited.add(entry_node)

    # 🔥 Node feature: label + outgoing degree
    node_feature = (entry_node.label, len(entry_node.next))
    features.append(node_feature)

    # 🔥 Edge features (IMPORTANT improvement)
    for nxt in entry_node.next:
        edge_feature = (entry_node.label, nxt.label)
        features.append(edge_feature)

    # Recurse
    for nxt in entry_node.next:
        extract_cfg_features(nxt, visited, features)

    return features


def cfg_similarity(cfg1_entry, cfg2_entry):
    """
    Compute similarity between two CFGs
    """

    features1 = extract_cfg_features(cfg1_entry)
    features2 = extract_cfg_features(cfg2_entry)

    set1 = set(features1)
    set2 = set(features2)

    if not set1 or not set2:
        return 0.0

    common = set1.intersection(set2)

    # 🔥 Slight smoothing (avoid extreme values)
    similarity = (2 * len(common)) / (len(set1) + len(set2))

    return similarity
