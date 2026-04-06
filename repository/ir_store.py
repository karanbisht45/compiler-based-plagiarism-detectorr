# repository/ir_store.py

stored_programs = []

def add_program(ir_tree, metadata=None):
    """
    Store IR of a program
    """
    stored_programs.append({
        "ir": ir_tree,
        "meta": metadata
    })

def get_all_programs():
    """
    Return all stored IRs
    """
    return stored_programs
