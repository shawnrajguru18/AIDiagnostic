"""
Demo fixture: NorthernCare Health — Healthcare & Life Sciences, Mid-Market.

NorthernCare is a regional health system with ~4,200 employees across
5 hospitals and 22 outpatient clinics. Heavy HIPAA exposure; nascent AI
investment; data remains highly siloed across clinical and administrative systems.

Expected scoring:
  - Overall: ~41 (±5) → Emerging (borderline Developing)
  - Data Foundation: ~35 (±8)
  - Governance Posture: ~38 (±8)
  - AI Investment Maturity: ~30 (±8)
  - Org Change Readiness: ~44 (±8)
  - Value-Pocket Clarity: ~55 (±8)
  - Regulatory Complexity: ~42 (±8)
"""

from typing import Any, Dict, List


# ---------------------------------------------------------------------------
# Prospect profile
# ---------------------------------------------------------------------------

NORTHERN_CARE_PROSPECT = {
    "prospect_name": "Dr. Marcus Webb",
    "prospect_role": "Chief Medical Information Officer",
    "prospect_email": "m.webb@northerncare.example.com",
    "company_name": "NorthernCare Health",
    "company_website": "https://www.northerncare.example.com",
    "industry": "Healthcare & Life Sciences",
    "size_band": "Mid-Market",
    "geography": "US",
    "persona": "P1",
}


# ---------------------------------------------------------------------------
# Questionnaire responses
# Scores: A=25, B=50, C=75, D=100 for single_select
# Scale: 1=20, 2=40, 3=60, 4=80, 5=100
# ---------------------------------------------------------------------------

NORTHERN_CARE_RESPONSES: List[Dict[str, Any]] = [
    # ---- Data Foundation ----
    {
        "question_id": "Q1.1",
        "dimension_id": "data_foundation",
        "answer_type": "single_select",
        "selected_option": "A",   # Siloed — data lives in departmental systems
        "score": 25,
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
        "selected_option": "A",   # No data lineage tracking
        "score": 25,
        "skipped": False,
    },
    {
        "question_id": "Q1.4",
        "dimension_id": "data_foundation",
        "answer_type": "single_select",
        "selected_option": "B",   # Ad hoc quality discovery, some dimensions measured
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
        "selected_option": "A",   # Primarily manual review by legal/compliance
        "score": 25,
        "skipped": False,
    },
    {
        "question_id": "Q2.3",
        "dimension_id": "governance_posture",
        "answer_type": "single_select",
        "selected_option": "B",   # Responsibility distributed across CIO/Legal
        "score": 50,
        "skipped": False,
    },
    # ---- AI Investment Maturity ----
    {
        "question_id": "Q3.1",
        "dimension_id": "ai_investment_maturity",
        "answer_type": "single_select",
        "selected_option": "A",   # Exploration — proofs-of-concept only
        "score": 25,
        "skipped": False,
    },
    {
        "question_id": "Q3.2",
        "dimension_id": "ai_investment_maturity",
        "answer_type": "single_select",
        "selected_option": "A",   # Less than 2% of tech budget
        "score": 25,
        "skipped": False,
    },
    {
        "question_id": "Q3.3",
        "dimension_id": "ai_investment_maturity",
        "answer_type": "single_select",
        "selected_option": "A",   # No MLOps team
        "score": 25,
        "skipped": False,
    },
    # ---- Org Change Readiness ----
    {
        "question_id": "Q4.1",
        "dimension_id": "org_change_readiness",
        "answer_type": "scale_1_5",
        "scale_value": 3,          # Moderate change management
        "score": 60,
        "skipped": False,
    },
    {
        "question_id": "Q4.2",
        "dimension_id": "org_change_readiness",
        "answer_type": "single_select",
        "selected_option": "A",   # Very low — most employees have no AI exposure
        "score": 25,
        "skipped": False,
    },
    {
        "question_id": "Q4.3",
        "dimension_id": "org_change_readiness",
        "answer_type": "single_select",
        "selected_option": "B",   # Informal executive mentions but no coordinated message
        "score": 50,
        "skipped": False,
    },
    # ---- Value-Pocket Clarity ----
    {
        "question_id": "Q5.1",
        "dimension_id": "value_pocket_clarity",
        "answer_type": "single_select",
        "selected_option": "A",   # No — have not yet mapped AI to specific business outcomes
        "score": 25,
        "skipped": False,
    },
    {
        "question_id": "Q5.2",
        "dimension_id": "value_pocket_clarity",
        "answer_type": "multi_select",
        "selected_options": ["A", "E"],   # Cost, Risk
        "score": 25,
        "skipped": False,
    },
    {
        "question_id": "Q5.3",
        "dimension_id": "value_pocket_clarity",
        "answer_type": "open_short",
        "open_text": (
            "Prior authorisation management is our biggest pain point — our team processes over "
            "3,200 prior auths per month manually. It's a significant administrative burden that "
            "delays patient care and requires 12 FTEs in our revenue cycle team to manage."
        ),
        "score": 75,
        "skipped": False,
    },
    # ---- Regulatory Complexity ----
    {
        "question_id": "Q6.1",
        "dimension_id": "regulatory_complexity",
        "answer_type": "multi_select",
        "selected_options": ["B", "C"],   # GDPR/CCPA, HIPAA/FDA
        "score": None,              # Informational
        "skipped": False,
    },
    {
        "question_id": "Q6.2",
        "dimension_id": "regulatory_complexity",
        "answer_type": "single_select",
        "selected_option": "B",   # Assessment in progress
        "score": 50,
        "skipped": False,
    },
    {
        "question_id": "Q6.3",
        "dimension_id": "regulatory_complexity",
        "answer_type": "single_select",
        "selected_option": "B",   # 2–3 jurisdictions (US + some state-level variation)
        "score": 75,
        "skipped": False,
    },
]


# ---------------------------------------------------------------------------
# Expected scoring outcomes (for test assertions)
# ---------------------------------------------------------------------------

NORTHERN_CARE_EXPECTED = {
    "overall_score_range": (33, 43),      # ~38 ±5
    "overall_tier": "Emerging",
    "dimension_expected": {
        "data_foundation":       (22, 38),   # ~30
        "governance_posture":    (34, 51),   # ~43
        "ai_investment_maturity": (17, 33),  # ~25
        "org_change_readiness":  (35, 52),   # ~44
        "value_pocket_clarity":  (32, 48),   # ~40
        "regulatory_complexity": (52, 68),   # ~60
    },
    "recommended_quick_wins": ["QW-HLS-001", "QW-HLS-002", "QW-002"],
}


# ---------------------------------------------------------------------------
# Combined fixture dict
# ---------------------------------------------------------------------------

NORTHERN_CARE_FIXTURE: Dict[str, Any] = {
    "prospect": NORTHERN_CARE_PROSPECT,
    "responses": NORTHERN_CARE_RESPONSES,
    "expected": NORTHERN_CARE_EXPECTED,
}
