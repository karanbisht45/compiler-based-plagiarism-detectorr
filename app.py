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

uploaded_file = st.file_uploader(
    "Upload a code file",
    type=["c", "cpp", "java", "py", "js"],
    accept_multiple_files=False
)


if uploaded_file:
    st.success(f"{len(uploaded_file)} files uploaded")


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


if uploaded_file:
    st.subheader("📌 Detected Languages")

    for f in uploaded_file:
        code = f.read().decode("utf-8", errors="ignore")
        lang = detect_language(f.name, code)
        st.write(f"**{f.name}** → {lang}")


if uploaded_file:
    code = uploaded_file.read().decode("utf-8", errors="ignore")
    ir = dummy_ir_from_code(code)

    repo = get_all_programs()

    if len(repo) == 0:
        add_program(ir, {"filename": uploaded_file.name})
        st.info("First program stored as reference.")
    else:
        result = check_single_program(ir, repo)

        st.subheader("📊 Result")
        st.metric("Plagiarism (%)", f"{result['plagiarism']:.2f}")
        st.metric("AI Probability (%)", f"{result['ai_prob']:.2f}")
        st.success(f"Verdict: {result['verdict']}")

        add_program(ir, {"filename": uploaded_file.name})
