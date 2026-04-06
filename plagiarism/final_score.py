# plagiarism/final_score.py

def clamp(x, low=0.0, high=1.0):
    return max(low, min(high, x))


def compute_plagiarism_score(subtree_sim, cfg_sim, pdg_sim):
    """
    Weighted plagiarism score (balanced)
    """

    # 🔥 Slightly safer weights (reduce false positives)
    w_subtree = 0.4
    w_cfg = 0.35
    w_pdg = 0.25

    raw_score = (
        w_subtree * subtree_sim +
        w_cfg * cfg_sim +
        w_pdg * pdg_sim
    )

    # 🔥 Soft penalty for weak similarity
    if raw_score < 0.3:
        raw_score *= 0.7

    return clamp(raw_score) * 100


def compute_ai_probability(plagiarism_score, cfg_sim, pdg_sim):
    """
    Improved heuristic AI-written probability
    """

    ai_score = 0.0

    # 🔹 Very structured flow → AI-like
    if cfg_sim > 0.9:
        ai_score += 0.4

    # 🔹 Strong semantic similarity
    if pdg_sim > 0.75:
        ai_score += 0.3

    # 🔹 High plagiarism → suspicious
    if plagiarism_score > 70:
        ai_score += 0.2

    # 🔹 Low variation between structure & semantics
    if abs(cfg_sim - pdg_sim) < 0.1:
        ai_score += 0.1

    return clamp(ai_score) * 100


def final_verdict(plagiarism_score, ai_probability):
    """
    Improved verdict logic (demo-safe)
    """

    # 🔥 Strong AI signal first
    if ai_probability > 75:
        return "Likely AI-generated"

    # 🔹 Safe zone
    if plagiarism_score < 25:
        return "Likely Human-written"

    # 🔹 Low similarity
    if plagiarism_score < 50:
        return "Low similarity (Safe)"

    # 🔹 Moderate plagiarism
    if plagiarism_score < 75:
        return "Possibly Plagiarized"

    # 🔹 High plagiarism
    return "Highly Plagiarized"
