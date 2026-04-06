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
from repository.ir_store import add_program, get_all_programs
from plagiarism.single_check import check_single_program


def dummy_ir_from_code(code):
    """
    TEMPORARY:
    Replace this with real compiler frontend later
    """
    program = IRNode("PROGRAM")
    block = IRNode("BLOCK")

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

# 🔥 TEXT INPUT INSTEAD OF FILE UPLOAD
st.header("📝 Enter Code")

code_input = st.text_area("Paste your code here", height=300)

# 🔥 ANALYZE BUTTON
if st.button("Analyze Code"):

    if not code_input.strip():
        st.warning("Please enter some code")
        st.stop()

    # Convert code → IR
    ir = dummy_ir_from_code(code_input)

    repo = get_all_programs()

    # 🔹 FIRST CODE (NO COMPARISON)
    if len(repo) == 0:
        add_program(ir)
        st.info("First submission stored. No comparison available yet.")

    # 🔹 COMPARE WITH PAST
    else:
        result = check_single_program(ir, repo)

        st.subheader("📊 Result")
        st.metric("Plagiarism (%)", f"{result['plagiarism']:.2f}")
        st.metric("AI Probability (%)", f"{result['ai_prob']:.2f}")
        st.success(f"Verdict: {result['verdict']}")

        add_program(ir)

    # 🔥 LEARNING FEEDBACK
    st.write(f"📚 Repository size: {len(repo)} programs")
    st.info("System improves as more programs are analyzed.")
