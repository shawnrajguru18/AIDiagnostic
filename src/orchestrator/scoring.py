"""Scoring utilities for DXC AI Readiness Diagnostic V0.

Implements the six-dimension scoring model with configurable weights,
question-level weighted averages, tier classification, and overall
composite score computation.

All scores are on a 0-100 scale.
All question responses are expected as numeric values 0-100
(answer option scores from the questionnaire).
"""

from __future__ import annotations

from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# Dimension weights — must sum to 1.0
# ---------------------------------------------------------------------------

DIMENSION_WEIGHTS: Dict[str, float] = {
    "data_foundation": 0.20,
    "governance_posture": 0.20,
    "ai_investment_maturity": 0.18,
    "org_change_readiness": 0.15,
    "value_pocket_clarity": 0.17,
    "regulatory_complexity": 0.10,
}

# ---------------------------------------------------------------------------
# Question weights per dimension — weights within each dimension must sum to 1.0
# ---------------------------------------------------------------------------

DIMENSION_QUESTION_WEIGHTS: Dict[str, Dict[str, float]] = {
    "data_foundation": {
        "Q1.1": 0.30,
        "Q1.2": 0.25,
        "Q1.3": 0.25,
        "Q1.4": 0.20,
    },
    "governance_posture": {
        "Q2.1": 0.40,
        "Q2.2": 0.30,
        "Q2.3": 0.30,
    },
    "ai_investment_maturity": {
        "Q3.1": 0.30,
        "Q3.2": 0.30,
        "Q3.3": 0.25,
        "Q3.4": 0.15,
    },
    "org_change_readiness": {
        "Q4.1": 0.35,
        "Q4.2": 0.40,
        "Q4.3": 0.25,
    },
    "value_pocket_clarity": {
        "Q5.1": 0.40,
        "Q5.2": 0.30,
        "Q5.3": 0.30,
    },
    "regulatory_complexity": {
        "Q6.1": 0.50,  # informational weight
        "Q6.2": 0.30,
        "Q6.3": 0.20,
    },
}

# ---------------------------------------------------------------------------
# Tier thresholds (inclusive lower bound)
# ---------------------------------------------------------------------------

TIER_THRESHOLDS = [
    (80.0, "Leading"),
    (60.0, "Established"),
    (40.0, "Developing"),
    (0.0, "Emerging"),
]

# Tier colour mapping for rendering
TIER_COLOURS: Dict[str, Dict[str, str]] = {
    "Emerging": {"label": "Peach", "hex": "#FFC982"},
    "Developing": {"label": "Gold", "hex": "#FFAE41"},
    "Established": {"label": "Sky", "hex": "#A1E6FF"},
    "Leading": {"label": "True Blue", "hex": "#4995FF"},
}

# Human-readable dimension names
DIMENSION_DISPLAY_NAMES: Dict[str, str] = {
    "data_foundation": "Data Foundation",
    "governance_posture": "Governance Posture",
    "ai_investment_maturity": "AI Investment Maturity",
    "org_change_readiness": "Organisational Change Readiness",
    "value_pocket_clarity": "Value Pocket Clarity",
    "regulatory_complexity": "Regulatory Complexity",
}


# ---------------------------------------------------------------------------
# Core scoring functions
# ---------------------------------------------------------------------------


def get_tier(score: float) -> str:
    """Map a 0-100 score to a named readiness tier.

    Tiers:
        Leading:     80-100
        Established: 60-79
        Developing:  40-59
        Emerging:     0-39

    Args:
        score: Overall or dimension score on a 0-100 scale.

    Returns:
        Tier name string.
    """
    for threshold, tier_name in TIER_THRESHOLDS:
        if score >= threshold:
            return tier_name
    return "Emerging"


def _response_score(response: dict) -> Optional[float]:
    """Extract the numeric score from a single questionnaire response dict.

    A response dict is expected to have at minimum:
      - question_id: str  (e.g. "Q1.1")
      - score: int | float | None   (the pre-computed answer score 0-100)

    If score is None (informational question), returns None so callers can
    handle the skip-logic case.

    Args:
        response: A questionnaire response dict (see QuestionResponse schema).

    Returns:
        Float score 0-100, or None if the question is informational.
    """
    score = response.get("score")
    if score is None:
        return None
    return float(score)


def compute_dimension_score(dimension: str, responses: list) -> float:
    """Compute the weighted average score for a single dimension.

    Special case — AI Investment Maturity (ai_investment_maturity):
      If Q3.1 answer is option "A" (no current AI investment), Q3.2 and Q3.3
      are skipped and their weight is redistributed to Q3.1 and Q3.4
      proportionally.

    Args:
        dimension: Dimension key string (e.g. 'data_foundation').
        responses: List of response dicts for all questions.

    Returns:
        Weighted average score 0-100 for the dimension.
        Returns 0.0 if no scoreable responses found.
    """
    question_weights = DIMENSION_QUESTION_WEIGHTS.get(dimension, {})
    if not question_weights:
        return 0.0

    # Build a lookup: question_id -> score
    score_lookup: Dict[str, Optional[float]] = {}
    for response in responses:
        qid = response.get("question_id", "")
        if qid in question_weights:
            score_lookup[qid] = _response_score(response)

    # --- Special skip logic for ai_investment_maturity ---
    if dimension == "ai_investment_maturity":
        q3_1_response = next(
            (r for r in responses if r.get("question_id") == "Q3.1"), None
        )
        if q3_1_response is not None:
            # Detect "no investment" answer — option_id "A" or score == 0
            selected = q3_1_response.get("selected_option", "")
            raw_score = q3_1_response.get("score", -1)
            is_no_investment = selected == "A" or raw_score == 0

            if is_no_investment:
                # Remove Q3.2 and Q3.3 from scoring, redistribute weights
                active_weights = {
                    "Q3.1": question_weights["Q3.1"],
                    "Q3.4": question_weights["Q3.4"],
                }
                # Normalise to sum to 1.0
                total = sum(active_weights.values())
                active_weights = {k: v / total for k, v in active_weights.items()}

                weighted_sum = 0.0
                total_weight = 0.0
                for qid, w in active_weights.items():
                    s = score_lookup.get(qid)
                    if s is not None:
                        weighted_sum += s * w
                        total_weight += w

                return (weighted_sum / total_weight) if total_weight > 0 else 0.0

    # --- Standard weighted average ---
    weighted_sum = 0.0
    total_weight = 0.0

    for qid, weight in question_weights.items():
        score = score_lookup.get(qid)
        if score is not None:
            weighted_sum += score * weight
            total_weight += weight

    if total_weight == 0.0:
        return 0.0

    # Normalise in case some questions were skipped
    return weighted_sum / total_weight


def compute_overall_score(dimension_scores: Dict[str, float]) -> float:
    """Compute the overall AI readiness score as a weighted sum of dimension scores.

    Args:
        dimension_scores: Dict mapping dimension key to dimension score (0-100).

    Returns:
        Overall composite score 0-100.
    """
    total = 0.0
    weight_used = 0.0
    for dimension, weight in DIMENSION_WEIGHTS.items():
        score = dimension_scores.get(dimension)
        if score is not None:
            total += score * weight
            weight_used += weight

    if weight_used == 0.0:
        return 0.0

    # Normalise if some dimensions had no data
    return total / weight_used * 100.0 / 100.0  # already on 0-100 scale


def compute_all_scores(responses: list) -> dict:
    """Compute dimension scores, overall score, and tier from questionnaire responses.

    This is the top-level entry point used by C2 and the orchestrator.

    Args:
        responses: List of response dicts (QuestionResponse-compatible).

    Returns:
        dict with:
          - dimension_scores: {dimension_key: float} — each 0-100
          - overall_score: float — 0-100 composite
          - overall_tier: str — Emerging | Developing | Established | Leading
          - dimension_tiers: {dimension_key: str}
          - dimension_weights: {dimension_key: float}
          - questions_answered_per_dimension: {dimension_key: int}
          - questions_skipped_per_dimension: {dimension_key: int}
    """
    dimension_scores: Dict[str, float] = {}
    dimension_tiers: Dict[str, str] = {}
    answered_counts: Dict[str, int] = {}
    skipped_counts: Dict[str, int] = {}

    for dimension in DIMENSION_WEIGHTS:
        dim_weights = DIMENSION_QUESTION_WEIGHTS.get(dimension, {})
        answered = 0
        skipped = 0

        for response in responses:
            qid = response.get("question_id", "")
            if qid in dim_weights:
                if response.get("skipped") or _response_score(response) is None:
                    skipped += 1
                else:
                    answered += 1

        dim_score = compute_dimension_score(dimension, responses)
        dimension_scores[dimension] = dim_score
        dimension_tiers[dimension] = get_tier(dim_score)
        answered_counts[dimension] = answered
        skipped_counts[dimension] = skipped

    overall = compute_overall_score(dimension_scores)

    return {
        "dimension_scores": dimension_scores,
        "overall_score": round(overall, 1),
        "overall_tier": get_tier(overall),
        "dimension_tiers": dimension_tiers,
        "dimension_weights": dict(DIMENSION_WEIGHTS),
        "questions_answered_per_dimension": answered_counts,
        "questions_skipped_per_dimension": skipped_counts,
    }


def get_tier_colour(tier: str) -> Dict[str, str]:
    """Return the colour metadata for a given tier.

    Args:
        tier: Tier name string.

    Returns:
        dict with 'label' and 'hex' keys.
    """
    return TIER_COLOURS.get(tier, {"label": "Unknown", "hex": "#CCCCCC"})
