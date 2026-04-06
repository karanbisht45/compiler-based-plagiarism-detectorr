# plagiarism/pdg.py

def collect_vars(node, vars_set=None):
    if vars_set is None:
        vars_set = set()

    if node.node_type in ("VAR", "POINTER_DEREF"):
        vars_set.add(node.value)

    for child in node.children:
        collect_vars(child, vars_set)

    return vars_set


def extract_data_dependencies(ir_node, deps=None, last_def=None, alias=None):
    """
    Pointer-aware data-flow extraction
    """
    if deps is None:
        deps = set()
    if last_def is None:
        last_def = {}
    if alias is None:
        alias = {}

    if ir_node.node_type == "ASSIGN":
        lhs = ir_node.children[0]
        rhs = ir_node.children[1]

        # -------------------------
        # Case 1: p = &a
        # -------------------------
        if rhs.node_type == "POINTER_REF":
            alias[lhs.value] = rhs.value
            deps.add((rhs.value, lhs.value))
            last_def[lhs.value] = lhs.value

        # -------------------------
        # Case 2: x = *p
        # -------------------------
        elif rhs.node_type == "POINTER_DEREF":
            ptr = rhs.value

            # If alias exists → use actual variable
            if ptr in alias:
                deps.add((alias[ptr], lhs.value))

            # fallback: direct dependency
            elif ptr in last_def:
                deps.add((last_def[ptr], lhs.value))

            last_def[lhs.value] = lhs.value

        # -------------------------
        # Case 3: normal assignment
        # -------------------------
        else:
            used = collect_vars(rhs)

            for u in used:
                if u in alias:
                    deps.add((alias[u], lhs.value))
                elif u in last_def:
                    deps.add((last_def[u], lhs.value))

            last_def[lhs.value] = lhs.value

    # recurse
    for child in ir_node.children:
        extract_data_dependencies(child, deps, last_def, alias)

    return deps


def normalize_deps(deps):
    """
    Normalize dependency pairs (order independent)
    """
    return set(tuple(sorted(d)) for d in deps)


def pdg_similarity(ir1, ir2):
    deps1 = normalize_deps(extract_data_dependencies(ir1))
    deps2 = normalize_deps(extract_data_dependencies(ir2))

    # 🔥 Removed debug prints (important for clean output)

    if not deps1 or not deps2:
        return 0.0

    common = deps1.intersection(deps2)

    return (2 * len(common)) / (len(deps1) + len(deps2))
