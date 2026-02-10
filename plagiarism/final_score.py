# plagiarism/final_score.py

def clamp(x, low=0.0, high=1.0):
    return max(low, min(high, x))


def compute_plagiarism_score(subtree_sim, cfg_sim, pdg_sim):
    """
    Weighted plagiarism score
    """
    # Weights (defendable in viva)
    w_subtree = 0.4
    w_cfg = 0.35
    w_pdg = 0.25

    score = (
        w_subtree * subtree_sim +
        w_cfg * cfg_sim +
        w_pdg * pdg_sim
    )

    return clamp(score) * 100


def compute_ai_probability(plagiarism_score, cfg_sim, pdg_sim):
    """
    Heuristic AI-written probability (code)
    """
    ai_score = 0.0

    # High structure + low semantic diversity → AI-like
    if cfg_sim > 0.85:
        ai_score += 0.4

    if pdg_sim > 0.7:
        ai_score += 0.3

    if plagiarism_score > 80:
        ai_score += 0.3

    return clamp(ai_score) * 100


def final_verdict(plagiarism_score, ai_probability):
    """
    Human-readable verdict
    """
    if ai_probability > 70:
        return "Likely AI-generated"

    if plagiarism_score > 75:
        return "Highly Plagiarized"

    if plagiarism_score > 40:
        return "Possibly Plagiarized"

    return "Likely Human-written"
