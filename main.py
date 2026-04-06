# main.py

from ir.node import IRNode
from ir.printer import print_ir
from ir.normalize import IRNormalizer
from plagiarism.tree_hash import hash_node
from plagiarism.subtree_match import subtree_similarity
from ir.cfg import build_cfg
from plagiarism.cfg_similarity import cfg_similarity
from plagiarism.pdg import pdg_similarity
from plagiarism.final_score import (
    compute_plagiarism_score,
    compute_ai_probability,
    final_verdict
)

# -----------------------
# STEP 1: BUILD SAMPLE IR
# -----------------------

program = IRNode("PROGRAM")

# class MyClass
cls = IRNode("CLASS", "MyClass")

# function foo
func = IRNode("FUNCTION", "foo")
block = IRNode("BLOCK")

# ptr = &a
assign1 = IRNode("ASSIGN")
assign1.add_child(IRNode("VAR", "ptr"))
assign1.add_child(IRNode("POINTER_REF", "a"))

# x = *ptr
assign2 = IRNode("ASSIGN")
assign2.add_child(IRNode("VAR", "x"))
assign2.add_child(IRNode("POINTER_DEREF", "ptr"))

block.add_child(assign1)
block.add_child(assign2)

func.add_child(block)
cls.add_child(func)
program.add_child(cls)

# -----------------------------
# STEP 2: PRINT ORIGINAL IR
# -----------------------------

print("=== ORIGINAL IR ===")
print_ir(program)

# -----------------------------
# STEP 3: NORMALIZE IR
# -----------------------------

normalizer = IRNormalizer()
normalized_program = normalizer.normalize(program)

print("\n=== NORMALIZED IR ===")
print_ir(normalized_program)

# -----------------------------
# STEP 4: TREE HASHING
# -----------------------------

tree_hash = hash_node(normalized_program)

print("\n=== TREE HASH ===")
print(tree_hash)

# -----------------------------
# STEP 5: PARTIAL PLAGIARISM TEST
# -----------------------------

# Create second program with realistic similarity
program2 = IRNode("PROGRAM")
cls2 = IRNode("CLASS", "AnotherClass")
func2 = IRNode("FUNCTION", "bar")
block2 = IRNode("BLOCK")

# ptr2 = &a
assign_p = IRNode("ASSIGN")
assign_p.add_child(IRNode("VAR", "ptr2"))
assign_p.add_child(IRNode("POINTER_REF", "a"))

# y = *ptr2
assign_copy = IRNode("ASSIGN")
assign_copy.add_child(IRNode("VAR", "y"))
assign_copy.add_child(IRNode("POINTER_DEREF", "ptr2"))

block2.add_child(assign_p)
block2.add_child(assign_copy)

func2.add_child(block2)
cls2.add_child(func2)
program2.add_child(cls2)

# Normalize second program
normalizer2 = IRNormalizer()
program2 = normalizer2.normalize(program2)

# Compute subtree similarity
similarity = subtree_similarity(normalized_program, program2)

print("\n=== SUBTREE SIMILARITY ===")
print(f"Similarity Score: {similarity:.2f}")

# -----------------------------
# STEP 6: CFG BUILD
# -----------------------------

print("\n=== CFG BUILD ===")
cfg_entry, cfg_exits = build_cfg(normalized_program)

print("CFG Entry:", cfg_entry)
print("CFG Exit Nodes:", cfg_exits)
print("CFG Entry Next:", cfg_entry.next)

# -----------------------------
# STEP 7: CFG SIMILARITY
# -----------------------------

cfg_entry1, _ = build_cfg(normalized_program)
cfg_entry2, _ = build_cfg(program2)

cfg_sim = cfg_similarity(cfg_entry1, cfg_entry2)

print("\n=== CFG SIMILARITY ===")
print(f"CFG Similarity Score: {cfg_sim:.2f}")

# -----------------------------
# STEP 8: PDG SIMILARITY
# -----------------------------

pdg_sim = pdg_similarity(normalized_program, program2)

print("\n=== PDG SIMILARITY ===")
print(f"PDG Similarity Score: {pdg_sim:.2f}")

# -----------------------------
# STEP 9: FINAL SCORING
# -----------------------------

final_plag_score = compute_plagiarism_score(
    subtree_sim=similarity,
    cfg_sim=cfg_sim,
    pdg_sim=pdg_sim
)

ai_prob = compute_ai_probability(
    plagiarism_score=final_plag_score,
    cfg_sim=cfg_sim,
    pdg_sim=pdg_sim
)

verdict = final_verdict(final_plag_score, ai_prob)

print("\n=== FINAL REPORT ===")
print(f"Plagiarism Score : {final_plag_score:.2f}%")
print(f"AI Probability   : {ai_prob:.2f}%")
print(f"Verdict          : {verdict}")
