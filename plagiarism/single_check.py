# plagiarism/single_check.py

from plagiarism.subtree_match import subtree_similarity
from ir.cfg import build_cfg
from plagiarism.cfg_similarity import cfg_similarity
from plagiarism.pdg import pdg_similarity
from plagiarism.final_score import (
    compute_plagiarism_score,
    compute_ai_probability,
    final_verdict
)


def check_single_program(ir_tree, repository_programs):
    """
    Compare one program against repository
    """

    best_score = 0
    best_match = None
    scores = []

    for item in repository_programs:
        ref_ir = item["ir"]

        subtree_sim = subtree_similarity(ir_tree, ref_ir)

        cfg1, _ = build_cfg(ir_tree)
        cfg2, _ = build_cfg(ref_ir)
        cfg_sim = cfg_similarity(cfg1, cfg2)

        pdg_sim = pdg_similarity(ir_tree, ref_ir)

        plag_score = compute_plagiarism_score(
            subtree_sim, cfg_sim, pdg_sim
        )

        scores.append(plag_score)

        if plag_score > best_score:
            best_score = plag_score
            best_match = {
                "plagiarism": plag_score,
                "cfg": cfg_sim,
                "pdg": pdg_sim
            }

    # 🔥 SAFETY: no repository
    if best_match is None:
        return {
            "plagiarism": 0.0,
            "ai_prob": 0.0,
            "verdict": "No reference data"
        }

    # 🔥 NEW: average similarity (reduces false positives)
    avg_score = sum(scores) / len(scores) if scores else 0

    # 🔥 FINAL PLAG SCORE ADJUSTMENT
    if best_score < 30 and avg_score < 25:
        final_plag = best_score * 0.6   # dampen noise
    else:
        final_plag = best_score

    # 🔥 AI probability
    ai_prob = compute_ai_probability(
        final_plag,
        best_match["cfg"],
        best_match["pdg"]
    )

    # 🔥 Verdict
    verdict = final_verdict(final_plag, ai_prob)

    return {
        "plagiarism": final_plag,
        "ai_prob": ai_prob,
        "verdict": verdict
    }
