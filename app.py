import streamlit as st
from ir.node import IRNode
from ir.normalize import IRNormalizer
from plagiarism.subtree_match import subtree_similarity
from ir.cfg import build_cfg
from plagiarism.cfg_similarity import cfg_similarity
from plagiarism.pdg import pdg_similarity
from plagiarism.final_score import (
    compute_plagiarism_score,
    compute_ai_probability,
    final_verdict
)

def dummy_ir_from_code(code):
    """
    TEMPORARY:
    Replace this with real compiler frontend later
    """
    program = IRNode("PROGRAM")
    block = IRNode("BLOCK")

    # very rough structure simulation
    for line in code.splitlines():
        if "=" in line:
            assign = IRNode("ASSIGN")
            assign.add_child(IRNode("VAR", "x"))
            assign.add_child(IRNode("VAR", "y"))
            block.add_child(assign)

    program.add_child(block)

    normalizer = IRNormalizer()
    return normalizer.normalize(program)



st.set_page_config(
    page_title="Plagiarism & AI Detection Compiler",
    layout="wide"
)

st.title("🧠 Compiler-Based Plagiarism & AI Detection System")

st.markdown("""
This system detects:
- 🔍 **Code plagiarism** using compiler techniques
- 🤖 **AI-written probability** for code
- 📄 (Coming soon) AI detection for text & PDFs
""")


st.header("📂 Upload Code Files")

uploaded_files = st.file_uploader(
    "Upload 2 or more code files",
    type=["c", "cpp", "java", "py", "js"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} files uploaded")


def detect_language(filename, content):
    if filename.endswith(".py"):
        return "Python"
    if filename.endswith(".java"):
        return "Java"
    if filename.endswith(".js"):
        return "JavaScript"
    if filename.endswith(".c"):
        return "C"
    if filename.endswith(".cpp"):
        return "C++"
    return "Unknown"


if uploaded_files:
    st.subheader("📌 Detected Languages")

    for f in uploaded_files:
        code = f.read().decode("utf-8", errors="ignore")
        lang = detect_language(f.name, code)
        st.write(f"**{f.name}** → {lang}")


if uploaded_files and len(uploaded_files) >= 2:
    if st.button("🔍 Analyze Plagiarism"):
        ir_trees = []

        for f in uploaded_files:
            code = f.read().decode("utf-8", errors="ignore")
            ir = dummy_ir_from_code(code)
            ir_trees.append(ir)

        # Compare first two files (extend later)
        ir1, ir2 = ir_trees[0], ir_trees[1]

        subtree_sim = subtree_similarity(ir1, ir2)

        cfg1, _ = build_cfg(ir1)
        cfg2, _ = build_cfg(ir2)
        cfg_sim = cfg_similarity(cfg1, cfg2)

        pdg_sim = pdg_similarity(ir1, ir2)

        plag_score = compute_plagiarism_score(
            subtree_sim, cfg_sim, pdg_sim
        )

        ai_prob = compute_ai_probability(
            plag_score, cfg_sim, pdg_sim
        )

        verdict = final_verdict(plag_score, ai_prob)

        st.subheader("📊 Results")
        st.metric("Plagiarism Score (%)", f"{plag_score:.2f}")
        st.metric("AI-Written Probability (%)", f"{ai_prob:.2f}")
        st.success(f"Verdict: **{verdict}**")
