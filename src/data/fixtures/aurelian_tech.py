"""
Demo fixture: Aurelian Technologies — Technology, Enterprise.

Aurelian is a publicly traded enterprise software company (~$2.1B ARR, 6,800 employees)
headquartered in the US with operations in EU and APAC. Strong data infrastructure,
active MLOps practice, multiple AI systems in production.

Expected scoring:
  - Overall: ~68 (±5) → Established
  - Data Foundation: ~72 (±8)
  - Governance Posture: ~70 (±8)
  - AI Investment Maturity: ~75 (±8)
  - Org Change Readiness: ~65 (±8)
  - Value-Pocket Clarity: ~73 (±8)
  - Regulatory Complexity: ~58 (±8)
"""

from typing import Any, Dict, List


# ---------------------------------------------------------------------------
# Prospect profile
# ---------------------------------------------------------------------------

AURELIAN_TECH_PROSPECT = {
    "prospect_name": "Priya Kapoor",
    "prospect_role": "VP of AI & Data Products",
    "prospect_email": "p.kapoor@aurelian.example.com",
    "company_name": "Aurelian Technologies",
    "company_website": "https://www.aurelian.example.com",
    "industry": "Technology",
    "size_band": "Enterprise",
    "geography": "US",
    "persona": "P2",
}


# ---------------------------------------------------------------------------
# Questionnaire responses
# Scores: A=25, B=50, C=75, D=100 for single_select
# Scale: 1=20, 2=40, 3=60, 4=80, 5=100
# ---------------------------------------------------------------------------

AURELIAN_TECH_RESPONSES: List[Dict[str, Any]] = [
    # ---- Data Foundation ----
    {
        "question_id": "Q1.1",
        "dimension_id": "data_foundation",
        "answer_type": "single_select",
        "selected_option": "C",   # Managed — enterprise data platform with defined ownership
        "score": 75,
        "skipped": False,
    },
    {
        "question_id": "Q1.2",
        "dimension_id": "data_foundation",
        "answer_type": "single_select",
        "selected_option": "C",   # 40–70% of datasets labelled/versioned
        "score": 75,
        "skipped": False,
    },
    {
        "question_id": "Q1.3",
        "dimension_id": "data_foundation",
        "answer_type": "single_select",
        "selected_option": "C",   # End-to-end lineage for key domains
        "score": 75,
        "skipped": False,
    },
    {
        "question_id": "Q1.4",
        "dimension_id": "data_foundation",
        "answer_type": "single_select",
        "selected_option": "B",   # Defined — some dimensions measured but not systematically
        "score": 50,
        "skipped": False,
    },
    # ---- Governance Posture ----
    {
        "question_id": "Q2.1",
        "dimension_id": "governance_posture",
        "answer_type": "single_select",
        "selected_option": "C",   # Adopted — published policy, limited enforcement
        "score": 75,
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
        "selected_option": "C",   # Scaling — multiple AI systems in production
        "score": 75,
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
        "selected_option": "C",   # Established dedicated MLOps team
        "score": 75,
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
        "selected_option": "C",   # Company-wide AI literacy programme launched
        "score": 75,
        "skipped": False,
    },
    {
        "question_id": "Q4.3",
        "dimension_id": "org_change_readiness",
        "answer_type": "single_select",
        "selected_option": "C",   # Active executive sponsor
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
        "selected_options": ["A", "B", "C", "D"],   # Cost, Revenue, CX, Employee
        "score": 75,
        "skipped": False,
    },
    {
        "question_id": "Q5.3",
        "dimension_id": "value_pocket_clarity",
        "answer_type": "open_short",
        "open_text": (
            "The most significant unrealised opportunity is in AI-augmented software development. "
            "We have 1,200 engineers but our code review and testing cycles still largely rely on "
            "manual peer review. We estimate we could improve developer throughput 25-35% with AI "
            "code generation and automated review, but we haven't formalised an enterprise rollout plan."
        ),
        "score": 75,
        "skipped": False,
    },
    # ---- Regulatory Complexity ----
    {
        "question_id": "Q6.1",
        "dimension_id": "regulatory_complexity",
        "answer_type": "multi_select",
        "selected_options": ["A", "B", "E"],   # EU AI Act, GDPR/CCPA, US EO/NIST
        "score": None,              # Informational
        "skipped": False,
    },
    {
        "question_id": "Q6.2",
        "dimension_id": "regulatory_complexity",
        "answer_type": "single_select",
        "selected_option": "B",   # Assessment in progress — requirements being mapped
        "score": 50,
        "skipped": False,
    },
    {
        "question_id": "Q6.3",
        "dimension_id": "regulatory_complexity",
        "answer_type": "single_select",
        "selected_option": "B",   # 2–3 jurisdictions (US, EU, APAC)
        "score": 75,
        "skipped": False,
    },
]


# ---------------------------------------------------------------------------
# Expected scoring outcomes (for test assertions)
# ---------------------------------------------------------------------------

AURELIAN_TECH_EXPECTED = {
    "overall_score_range": (63, 74),      # ~69 ±5
    "overall_tier": "Established",
    "dimension_expected": {
        "data_foundation":       (62, 78),   # ~70
        "governance_posture":    (59, 76),   # ~68
        "ai_investment_maturity": (58, 74),  # ~66
        "org_change_readiness":  (62, 78),   # ~70
        "value_pocket_clarity":  (67, 83),   # ~75
        "regulatory_complexity": (52, 68),   # ~60
    },
    "recommended_quick_wins": ["QW-006", "QW-002", "QW-005"],
}


# ---------------------------------------------------------------------------
# Combined fixture dict
# ---------------------------------------------------------------------------

AURELIAN_TECH_FIXTURE: Dict[str, Any] = {
    "prospect": AURELIAN_TECH_PROSPECT,
    "responses": AURELIAN_TECH_RESPONSES,
    "expected": AURELIAN_TECH_EXPECTED,
}
