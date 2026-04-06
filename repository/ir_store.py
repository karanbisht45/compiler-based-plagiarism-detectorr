# repository/ir_store.py

stored_programs = []

def add_program(ir_tree, metadata=None):
    """
    Store IR of a program
    Avoid duplicate storage
    """

    # 🔹 Prevent duplicates (basic check)
    for item in stored_programs:
        if item["ir"] == ir_tree:
            return  # already stored

    stored_programs.append({
        "ir": ir_tree,
        "meta": metadata or {}
    })


def get_all_programs():
    """
    Return all stored IRs
    """
    return stored_programs


def get_repository_size():
    """
    Return number of stored programs
    """
    return len(stored_programs)
