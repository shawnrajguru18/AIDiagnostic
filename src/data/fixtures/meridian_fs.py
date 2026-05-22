"""
Demo fixture: MeridianFS — Financial Services, Large Enterprise.

MeridianFS is a regional financial services holding company with ~$8B AUM,
primary operations in the US and UK, with regulatory exposure across SR 11-7,
DORA, MiFID II, and initial EU AI Act obligations.

Expected scoring:
  - Overall: ~55 (±5) → Developing
  - Data Foundation: ~50 (±8)
  - Governance Posture: ~62 (±8)
  - AI Investment Maturity: ~48 (±8)
  - Org Change Readiness: ~55 (±8)
  - Value-Pocket Clarity: ~68 (±8)
  - Regulatory Complexity: ~44 (±8)

Recommended quick wins: QW-001, QW-005, QW-012
"""

from typing import Any, Dict, List


# ---------------------------------------------------------------------------
# Prospect profile
# ---------------------------------------------------------------------------

MERIDIAN_FS_PROSPECT = {
    "prospect_name": "Sarah Chen",
    "prospect_role": "Chief Digital Officer",
    "prospect_email": "s.chen@meridianfs.example.com",
    "company_name": "MeridianFS",
    "company_website": "https://www.meridianfs.example.com",
    "industry": "Financial Services",
    "size_band": "Large",
    "geography": "US",
    "persona": "P1",
}


# ---------------------------------------------------------------------------
# Questionnaire responses
# Each response dict maps to the scoring engine's QuestionResponse structure.
# Scores follow the questionnaire option mapping: A=1→25, B=2→50, C=3→75, D=4→100
# Scale questions (Q4.1) map 1=20, 2=40, 3=60, 4=80, 5=100
# ---------------------------------------------------------------------------

MERIDIAN_FS_RESPONSES: List[Dict[str, Any]] = [
    # ---- Data Foundation ----
    {
        "question_id": "Q1.1",
        "dimension_id": "data_foundation",
        "answer_type": "single_select",
        "selected_option": "B",   # Partially integrated — some shared data platforms
        "score": 50,
        "skipped": False,
    },
    {
        "question_id": "Q1.2",
        "dimension_id": "data_foundation",
        "answer_type": "single_select",
        "selected_option": "A",   # Less than 10% of datasets ML-ready
        "score": 25,
        "skipped": False,
    },
    {
        "question_id": "Q1.3",
        "dimension_id": "data_foundation",
        "answer_type": "single_select",
        "selected_option": "B",   # Partial lineage documentation
        "score": 50,
        "skipped": False,
    },
    {
        "question_id": "Q1.4",
        "dimension_id": "data_foundation",
        "answer_type": "single_select",
        "selected_option": "B",   # Some dimensions measured but not systematically
        "score": 50,
        "skipped": False,
    },
    # ---- Governance Posture ----
    {
        "question_id": "Q2.1",
        "dimension_id": "governance_posture",
        "answer_type": "single_select",
        "selected_option": "B",   # Draft / in progress — framework being developed
        "score": 50,
        "skipped": False,
    },
    {
        "question_id": "Q2.2",
        "dimension_id": "governance_posture",
        "answer_type": "single_select",
        "selected_option": "B",   # Policy-driven with some automated controls
        "score": 50,
        "skipped": False,
    },
    {
        "question_id": "Q2.3",
        "dimension_id": "governance_posture",
        "answer_type": "single_select",
        "selected_option": "C",   # Named individual with AI governance remit
        "score": 75,
        "skipped": False,
    },
    # ---- AI Investment Maturity ----
    {
        "question_id": "Q3.1",
        "dimension_id": "ai_investment_maturity",
        "answer_type": "single_select",
        "selected_option": "B",   # Developing — one or two AI systems in production
        "score": 50,
        "skipped": False,
    },
    {
        "question_id": "Q3.2",
        "dimension_id": "ai_investment_maturity",
        "answer_type": "single_select",
        "selected_option": "B",   # 2–5% of tech budget
        "score": 50,
        "skipped": False,
    },
    {
        "question_id": "Q3.3",
        "dimension_id": "ai_investment_maturity",
        "answer_type": "single_select",
        "selected_option": "A",   # No MLOps team — data scientists manage informally
        "score": 25,
        "skipped": False,
    },
    # ---- Org Change Readiness ----
    {
        "question_id": "Q4.1",
        "dimension_id": "org_change_readiness",
        "answer_type": "scale_1_5",
        "scale_value": 2,          # Below-moderate change management
        "score": 40,
        "skipped": False,
    },
    {
        "question_id": "Q4.2",
        "dimension_id": "org_change_readiness",
        "answer_type": "single_select",
        "selected_option": "C",   # Company-wide AI literacy programme launched
        "score": 75,
        "skipped": False,
    },
    {
        "question_id": "Q4.3",
        "dimension_id": "org_change_readiness",
        "answer_type": "single_select",
        "selected_option": "C",   # Active executive sponsor with communications
        "score": 75,
        "skipped": False,
    },
    # ---- Value-Pocket Clarity ----
    {
        "question_id": "Q5.1",
        "dimension_id": "value_pocket_clarity",
        "answer_type": "single_select",
        "selected_option": "C",   # Prioritised AI opportunity map exists
        "score": 75,
        "skipped": False,
    },
    {
        "question_id": "Q5.2",
        "dimension_id": "value_pocket_clarity",
        "answer_type": "multi_select",
        "selected_options": ["A", "B", "E"],   # Cost, Revenue, Risk
        "score": 50,
        "skipped": False,
    },
    {
        "question_id": "Q5.3",
        "dimension_id": "value_pocket_clarity",
        "answer_type": "open_short",
        "open_text": (
            "Our most significant unrealised inefficiency is manual contract review across our lending and "
            "advisory divisions. We process approximately 2,000 contracts per month across 6 ERP instances "
            "with manual extraction of key clauses — this creates a 5-7 day bottleneck in deal execution."
        ),
        "score": 50,
        "skipped": False,
    },
    # ---- Regulatory Complexity ----
    {
        "question_id": "Q6.1",
        "dimension_id": "regulatory_complexity",
        "answer_type": "multi_select",
        "selected_options": ["B", "D", "E"],   # GDPR, Financial Services, US EO/NIST
        "score": None,             # Informational question — no direct score
        "skipped": False,
    },
    {
        "question_id": "Q6.2",
        "dimension_id": "regulatory_complexity",
        "answer_type": "single_select",
        "selected_option": "A",   # Not started — no AI-specific compliance assessment
        "score": 25,
        "skipped": False,
    },
    {
        "question_id": "Q6.3",
        "dimension_id": "regulatory_complexity",
        "answer_type": "single_select",
        "selected_option": "B",   # 2–3 jurisdictions (US + UK)
        "score": 75,
        "skipped": False,
    },
]


# ---------------------------------------------------------------------------
# Expected scoring outcomes (for test assertions)
# ---------------------------------------------------------------------------

MERIDIAN_FS_EXPECTED = {
    "overall_score_range": (47, 57),      # ~52 ±5
    "overall_tier": "Developing",
    "dimension_expected": {
        "data_foundation":       (35, 52),   # ~44
        "governance_posture":    (49, 66),   # ~58
        "ai_investment_maturity": (34, 51),  # ~43
        "org_change_readiness":  (55, 71),   # ~63
        "value_pocket_clarity":  (52, 68),   # ~60
        "regulatory_complexity": (37, 53),   # ~45
    },
    "recommended_quick_wins": ["QW-001", "QW-005", "QW-012"],
}


# ---------------------------------------------------------------------------
# Combined fixture dict (used by orchestrator and tests)
# ---------------------------------------------------------------------------

MERIDIAN_FS_FIXTURE: Dict[str, Any] = {
    "prospect": MERIDIAN_FS_PROSPECT,
    "responses": MERIDIAN_FS_RESPONSES,
    "expected": MERIDIAN_FS_EXPECTED,
}
