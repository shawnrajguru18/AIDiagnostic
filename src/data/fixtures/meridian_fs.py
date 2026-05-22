"""MeridianFS Holdings demo fixture for DXC AI Readiness Diagnostic V0.

This is the PRIMARY V0 investor-day demo scenario. All data is synthetic
and constructed to validate end-to-end pipeline behaviour and serve as
integration-test expected output.

Usage:
    from src.data.fixtures.meridian_fs import MERIDIAN_FS_FIXTURE
    prospect = MERIDIAN_FS_FIXTURE["prospect"]
    expected_synthesis = MERIDIAN_FS_FIXTURE["expected_synthesis"]

Dimension score targets (from Companion 03):
    Data Foundation:          ~52
    Governance Posture:       ~38
    AI Investment Maturity:   ~62
    Org Change Readiness:     ~55
    Value-Pocket Clarity:     ~48
    Regulatory Complexity:    ~72
    Overall:                  ~53  →  Developing tier

Quick wins: QW-001, QW-005, QW-012
Recommended next step: APR Discovery on claims adjudication
"""

from __future__ import annotations

from typing import Any, Dict, List


# ---------------------------------------------------------------------------
# Prospect profile
# ---------------------------------------------------------------------------

MERIDIAN_FS_PROSPECT: Dict[str, Any] = {
    "company_name": "MeridianFS Holdings, Inc.",
    "industry": "Financial Services",
    "size_band": "Large",
    "geography": "US",
    "primary_contact_name": "James Whitfield",
    "primary_contact_email": "j.whitfield@meridianfs.example.com",
    "primary_contact_title": "Chief Operating Officer",
    "partner_id": "DXC-PARTNER-001",
    "partner_name": "DXC Technology — US Financial Services Practice",
}


# ---------------------------------------------------------------------------
# Questionnaire responses
# Scores calibrated to produce the target dimension scores from Companion 03.
# ---------------------------------------------------------------------------

MERIDIAN_FS_RESPONSES: List[Dict[str, Any]] = [
    # ---- D1: Data Foundation — target raw ~52 ----
    {
        "question_id": "Q1.1",
        "dimension_id": "data_foundation",
        "answer_type": "single_select",
        "selected_option": "B",   # Partially integrated — score 40
        "score": 40,
        "skipped": False,
    },
    {
        "question_id": "Q1.2",
        "dimension_id": "data_foundation",
        "answer_type": "scale_1_5",
        "scale_value": 3,          # Mix of batch and near-RT — score 55
        "score": 55,
        "skipped": False,
    },
    {
        "question_id": "Q1.3",
        "dimension_id": "data_foundation",
        "answer_type": "single_select",
        "selected_option": "C",   # Moderate self-service — score 70
        "score": 70,
        "skipped": False,
    },
    {
        "question_id": "Q1.4",
        "dimension_id": "data_foundation",
        "answer_type": "single_select",
        "selected_option": "B",   # Developing quality programme — score 40
        "score": 40,
        "skipped": False,
    },
    # ---- D2: Governance Posture — target raw ~38 ----
    {
        "question_id": "Q2.1",
        "dimension_id": "governance_posture",
        "answer_type": "single_select",
        "selected_option": "B",   # Early stages, informal guidelines — score 35
        "score": 35,
        "skipped": False,
    },
    {
        "question_id": "Q2.2",
        "dimension_id": "governance_posture",
        "answer_type": "single_select",
        "selected_option": "B",   # Informal, project-level risk management — score 35
        "score": 35,
        "skipped": False,
    },
    {
        "question_id": "Q2.3",
        "dimension_id": "governance_posture",
        "answer_type": "single_select",
        "selected_option": "B",   # Aware of FCA/PRA, SR 11-7 but no programme — score 45
        "score": 45,
        "skipped": False,
    },
    # ---- D3: AI Investment Maturity — target raw ~62 ----
    {
        "question_id": "Q3.1",
        "dimension_id": "ai_investment_maturity",
        "answer_type": "single_select",
        "selected_option": "C",   # Multiple projects, some in production — score 70
        "score": 70,
        "skipped": False,
    },
    {
        "question_id": "Q3.2",
        "dimension_id": "ai_investment_maturity",
        "answer_type": "single_select",
        "selected_option": "B",   # 1-3 AI apps in production — score 45
        "score": 45,
        "skipped": False,
    },
    {
        "question_id": "Q3.3",
        "dimension_id": "ai_investment_maturity",
        "answer_type": "single_select",
        "selected_option": "C",   # Positive outcomes, informal ROI — score 70
        "score": 70,
        "skipped": False,
    },
    {
        "question_id": "Q3.4",
        "dimension_id": "ai_investment_maturity",
        "answer_type": "single_select",
        "selected_option": "C",   # Increasing moderately (10-30%) — score 70
        "score": 70,
        "skipped": False,
    },
    # ---- D4: Org Change Readiness — target raw ~55 ----
    {
        "question_id": "Q4.1",
        "dimension_id": "org_change_readiness",
        "answer_type": "single_select",
        "selected_option": "B",   # Developing change management — score 50
        "score": 50,
        "skipped": False,
    },
    {
        "question_id": "Q4.2",
        "dimension_id": "org_change_readiness",
        "answer_type": "single_select",
        "selected_option": "C",   # Mostly aligned, priorities being defined — score 75
        "score": 75,
        "skipped": False,
    },
    {
        "question_id": "Q4.3",
        "dimension_id": "org_change_readiness",
        "answer_type": "single_select",
        "selected_option": "B",   # Cautious — willing but needs support — score 55
        "score": 55,
        "skipped": False,
    },
    # ---- D5: Value-Pocket Clarity — target raw ~48 ----
    {
        "question_id": "Q5.1",
        "dimension_id": "value_pocket_clarity",
        "answer_type": "single_select",
        "selected_option": "B",   # Informal — teams have ideas, no inventory — score 50
        "score": 50,
        "skipped": False,
    },
    {
        "question_id": "Q5.2",
        "dimension_id": "value_pocket_clarity",
        "answer_type": "single_select",
        "selected_option": "B",   # High-level metrics, not financial — score 50
        "score": 50,
        "skipped": False,
    },
    {
        "question_id": "Q5.3",
        "dimension_id": "value_pocket_clarity",
        "answer_type": "single_select",
        "selected_option": "A",   # Automation of tasks framing — score 35
        "score": 35,
        "skipped": False,
    },
    # ---- D6: Regulatory Complexity — target ~72 (informational) ----
    {
        "question_id": "Q6.1",
        "dimension_id": "regulatory_complexity",
        "answer_type": "multi_select",
        "selected_options": ["C", "D", "F"],  # FCA/PRA, SR 11-7, SOC 2
        # Complexity score derived from number of applicable frameworks (3 = high = 75)
        "score": 75,
        "skipped": False,
    },
    {
        "question_id": "Q6.2",
        "dimension_id": "regulatory_complexity",
        "answer_type": "single_select",
        "selected_option": "C",   # Required in-region data residency; cloud restrictions apply
        "score": 65,
        "skipped": False,
    },
    {
        "question_id": "Q6.3",
        "dimension_id": "regulatory_complexity",
        "answer_type": "open_short",
        "open_text": (
            "We operate across US and UK. UK FCA Consumer Duty and cross-border "
            "data transfer requirements under UK GDPR create constraints on "
            "cloud-based AI model training for customer-facing applications. "
            "We are assessing whether UK SCCs are sufficient or whether a "
            "UK-sovereign cloud deployment is required."
        ),
        # Open-ended: moderate-high complexity score (70) reflecting substantive constraints
        "score": 70,
        "skipped": False,
    },
]


# ---------------------------------------------------------------------------
# Expected synthesis output (Companion 03 spec values)
# Used by integration tests to validate end-to-end pipeline output.
# ---------------------------------------------------------------------------

MERIDIAN_FS_EXPECTED_SYNTHESIS: Dict[str, Any] = {
    "overall_score": 53.0,
    "tier": "Developing",
    "dimension_scores": {
        "data_foundation": {
            "dimension_id": "data_foundation",
            "dimension_name": "Data Foundation",
            "weight": 0.20,
            "raw_score": 52.0,
            "weighted_score": 10.4,
            "confidence": "high",
            "questions_answered": 4,
            "questions_skipped": 0,
            "key_signals": [
                "Partially integrated data landscape with known gaps",
                "Mix of batch and near-real-time data currency",
                "Moderate self-service data accessibility",
                "Developing data quality programme with inconsistent coverage",
            ],
        },
        "governance_posture": {
            "dimension_id": "governance_posture",
            "dimension_name": "Governance Posture",
            "weight": 0.20,
            "raw_score": 38.0,
            "weighted_score": 7.6,
            "confidence": "high",
            "questions_answered": 3,
            "questions_skipped": 0,
            "key_signals": [
                "Informal AI governance guidelines only — nothing formalised",
                "AI risk managed at project level without enterprise coordination",
                "Aware of FCA/PRA and SR 11-7 requirements but no compliance programme",
            ],
        },
        "ai_investment_maturity": {
            "dimension_id": "ai_investment_maturity",
            "dimension_name": "AI Investment Maturity",
            "weight": 0.18,
            "raw_score": 62.0,
            "weighted_score": 11.16,
            "confidence": "high",
            "questions_answered": 4,
            "questions_skipped": 0,
            "key_signals": [
                "Multiple AI projects in flight with 1-3 in production",
                "Positive outcomes delivered, though ROI measurement is informal",
                "Moderate investment growth expected (10-30%)",
            ],
        },
        "org_change_readiness": {
            "dimension_id": "org_change_readiness",
            "dimension_name": "Organizational Change Readiness",
            "weight": 0.15,
            "raw_score": 55.0,
            "weighted_score": 8.25,
            "confidence": "high",
            "questions_answered": 3,
            "questions_skipped": 0,
            "key_signals": [
                "Developing change management capability — inconsistently applied",
                "Leadership broadly supports AI but priorities still being defined",
                "Workforce is cautious — willing to try but needs reassurance",
            ],
        },
        "value_pocket_clarity": {
            "dimension_id": "value_pocket_clarity",
            "dimension_name": "Value-Pocket Clarity",
            "weight": 0.17,
            "raw_score": 48.0,
            "weighted_score": 8.16,
            "confidence": "high",
            "questions_answered": 3,
            "questions_skipped": 0,
            "key_signals": [
                "Informal AI use case identification — no structured inventory",
                "High-level metrics not tied to financial outcomes",
                "Task-automation framing — process reinvention mindset not yet present",
            ],
        },
        "regulatory_complexity": {
            "dimension_id": "regulatory_complexity",
            "dimension_name": "Regulatory Complexity",
            "weight": 0.10,
            "raw_score": 72.0,
            "weighted_score": 7.2,
            "confidence": "medium",
            "questions_answered": 3,
            "questions_skipped": 0,
            "key_signals": [
                "Operates under FCA/PRA, SR 11-7, and SOC 2 frameworks",
                "Significant data sovereignty constraints for UK operations",
                "UK GDPR cross-border transfer restrictions on cloud AI training",
            ],
        },
    },
    "findings": [
        {
            "dimension_id": "governance_posture",
            "finding_type": "risk",
            "severity": "critical",
            "headline": "AI Governance Gap Creates Regulatory Exposure",
            "narrative": (
                "MeridianFS operates under SR 11-7 model risk management guidance "
                "and FCA/PRA AI principles, yet has only informal AI guidelines with "
                "no formalised framework. As AI deployments scale, this gap creates "
                "material regulatory and model-risk exposure. The lack of defined AI "
                "risk ownership at the enterprise level amplifies this risk."
            ),
            "evidence": [
                "Q2.1: Early-stage governance — informal guidelines only (score 35)",
                "Q2.2: AI risk managed at project level, no enterprise coordination (score 35)",
                "Q2.3: FCA/PRA and SR 11-7 requirements known but no compliance programme (score 45)",
            ],
            "recommended_actions": [
                "Commission an AI governance framework aligned to SR 11-7 and FCA/PRA within 90 days",
                "Appoint a named AI risk owner with executive committee visibility",
                "Conduct a model inventory and risk classification exercise",
            ],
        },
        {
            "dimension_id": "data_foundation",
            "finding_type": "gap",
            "severity": "major",
            "headline": "Fragmented Data Foundation Will Constrain AI Scaling",
            "narrative": (
                "MeridianFS has partially integrated data across its business lines "
                "but material gaps remain. The inconsistent data quality programme "
                "will create reliability issues for AI models as the portfolio scales "
                "from 1-3 to 10+ production deployments. Claims adjudication and "
                "fraud detection — the highest-value FS AI use cases — require "
                "high-quality, low-latency data that the current infrastructure "
                "cannot reliably provide at scale."
            ),
            "evidence": [
                "Q1.1: Partial integration — some pipelines but gaps remain (score 40)",
                "Q1.4: Developing quality programme — inconsistent coverage (score 40)",
                "High regulatory complexity (D6: 72) amplifies data quality risk for SR 11-7 compliance",
            ],
            "recommended_actions": [
                "Prioritise a data quality SLA programme for claims and transaction data domains",
                "Assess near-real-time pipeline capability for fraud detection use case",
                "Map data lineage for top 5 AI use cases as prerequisite for SR 11-7 compliance",
            ],
        },
        {
            "dimension_id": "ai_investment_maturity",
            "finding_type": "strength",
            "severity": "minor",
            "headline": "Established AI Programme Provides a Strong Foundation for Acceleration",
            "narrative": (
                "With multiple AI projects in flight and 1-3 in production, "
                "MeridianFS has moved beyond experimentation. Positive outcomes "
                "have been delivered and investment is growing moderately. This "
                "maturity positions the firm well to accelerate — provided governance "
                "and data foundation gaps are resolved concurrently."
            ),
            "evidence": [
                "Q3.1: Multiple projects in flight including some in production (score 70)",
                "Q3.3: Positive outcomes, though ROI measurement is informal (score 70)",
                "Q3.4: 10-30% investment growth planned over 12-18 months (score 70)",
            ],
            "recommended_actions": [
                "Formalise ROI measurement framework aligned to finance KPIs",
                "Establish MLOps capability to support scaling from 3 to 10+ models",
            ],
        },
        {
            "dimension_id": "value_pocket_clarity",
            "finding_type": "opportunity",
            "severity": "major",
            "headline": "Claims Adjudication Is the Highest Near-Term Value Pocket",
            "narrative": (
                "Industry benchmarks indicate that FS firms of MeridianFS's scale "
                "can achieve 55-70% straight-through processing on routine claims, "
                "yielding 30-45% cost reduction. MeridianFS's informal use case "
                "inventory has not yet surfaced this opportunity with a business case. "
                "An APR Discovery engagement focused on claims adjudication could "
                "unlock $4-9M in annual savings based on peer benchmarks at comparable firms."
            ),
            "evidence": [
                "Q5.1: Informal use case identification — no structured inventory (score 50)",
                "Q5.2: High-level metrics not tied to financial outcomes (score 50)",
                "Industry library: FS-001 Claims Adjudication (Tier 2 process) confirmed applicable",
            ],
            "recommended_actions": [
                "Commission a Claims Adjudication Value Assessment within 60 days",
                "Quantify current STP rate and manual processing cost as baseline",
                "Model ROI on 55-70% STP target using DXC benchmark data",
            ],
        },
        {
            "dimension_id": "regulatory_complexity",
            "finding_type": "risk",
            "severity": "major",
            "headline": "UK Cross-Border Data Constraints Require Architecture Decision",
            "narrative": (
                "The combination of FCA/PRA oversight and UK GDPR cross-border "
                "transfer restrictions means MeridianFS cannot freely use "
                "US-based cloud AI training infrastructure for customer-facing "
                "UK applications. This requires either a UK-sovereign cloud "
                "deployment or federated learning architecture — decisions that "
                "must be made before scaling the AI programme to avoid costly rework."
            ),
            "evidence": [
                "Q6.1: FCA/PRA framework selected as applicable",
                "Q6.2: Significant data localisation constraints identified",
                "Q6.3: UK GDPR SCCs and cross-border transfer concerns explicitly raised",
            ],
            "recommended_actions": [
                "Engage DXC Cloud Practice to assess UK-sovereign AI infrastructure options",
                "Obtain legal opinion on UK GDPR adequacy for specific AI training data flows",
                "Design AI architecture with data residency as a first-class constraint",
            ],
        },
    ],
    "selected_quick_wins": [
        {
            "pattern_id": "QW-001",
            "name": "Intelligent Invoice & Accounts-Payable Automation",
            "rank": 1,
            "selection_rationale": (
                "MeridianFS operates across multiple legal entities with high invoice "
                "volumes. Existing ERP infrastructure and partial data integration "
                "make this a low-risk, high-ROI entry point. Prerequisites are met "
                "and value can be demonstrated within 8 weeks — ideal as a first "
                "AI win to build organisational confidence."
            ),
            "estimated_timeline_weeks": 8,
            "estimated_roi_narrative": (
                "Estimated $1.2-2.8M annual savings based on assumed invoice volume "
                "for a Large FS firm; payback typically 6-9 months."
            ),
            "dxc_practice_owner": "DXC Intelligent Process Automation",
        },
        {
            "pattern_id": "QW-005",
            "name": "AI-Assisted Claims Adjudication & Straight-Through Processing",
            "rank": 2,
            "selection_rationale": (
                "Claims adjudication is the highest-value FS-specific opportunity "
                "for MeridianFS. The 3+ year claims history and digital intake channel "
                "meet prerequisites. Achieving 55-70% STP would deliver transformational "
                "unit economics and demonstrate AI ROI at board level."
            ),
            "estimated_timeline_weeks": 14,
            "estimated_roi_narrative": (
                "Peer benchmarks: $4-9M annual savings at MeridianFS scale; "
                "30-45% processing cost reduction; 18-month payback at mid-range."
            ),
            "dxc_practice_owner": "DXC Financial Services AI Practice",
        },
        {
            "pattern_id": "QW-012",
            "name": "AI-Assisted Regulatory Report Generation & Validation",
            "rank": 3,
            "selection_rationale": (
                "Given MeridianFS's significant regulatory burden (SR 11-7, FCA/PRA) "
                "and the need to build compliance confidence with regulators, automated "
                "regulatory reporting delivers cost savings while strengthening the "
                "governance narrative for supervisory engagement."
            ),
            "estimated_timeline_weeks": 16,
            "estimated_roi_narrative": (
                "Estimated $600K-1.4M annual savings on report preparation; "
                "improved governance story for FCA/PRA supervisory engagement."
            ),
            "dxc_practice_owner": "DXC Regulatory Technology Practice",
        },
    ],
    "recommended_next_step": {
        "title": "APR Discovery: Claims Adjudication Transformation",
        "description": (
            "A 4-week Accelerated Proof of Results (APR) Discovery engagement "
            "focused on MeridianFS's claims adjudication process. DXC will "
            "baseline the current straight-through processing rate, quantify "
            "the financial opportunity, design the target AI architecture "
            "(including SR 11-7 model governance requirements), and deliver "
            "a go/no-go recommendation with a signed business case. "
            "Key stakeholders: COO (Whitfield), CFO, and Chief Risk Officer."
        ),
        "step_type": "apr_discovery",
        "target_timeline": "Within 30 days of scorecard delivery",
        "dxc_practice": "DXC Financial Services AI Practice",
        "estimated_value": "$4-9M annual savings opportunity on claims adjudication alone",
        "prerequisites": [
            "Access to claims management system and 24 months of adjudication history",
            "Stakeholder alignment from COO, CFO, and CRO",
            "Data governance approval for AI access to claims data",
        ],
        "contact_role": "DXC Financial Services Practice Lead",
    },
    "executive_narrative": (
        "MeridianFS is a Developing-tier AI organisation (overall score 53/100) "
        "with a meaningful AI programme underway but facing three structural gaps "
        "that must be resolved before the firm can scale with confidence: "
        "(1) an AI governance framework that satisfies FCA/PRA and SR 11-7 obligations, "
        "(2) a data foundation that can support production-grade AI at scale, and "
        "(3) a structured approach to identifying and measuring AI value. "
        "The good news: MeridianFS has an active leadership mandate, growing investment, "
        "and a high-value near-term opportunity in claims adjudication that can generate "
        "$4-9M in annual savings while building the governance muscle the firm needs. "
        "DXC recommends beginning with an APR Discovery on claims adjudication within "
        "the next 30 days."
    ),
}


# ---------------------------------------------------------------------------
# Combined fixture dict (used by orchestrator and integration tests)
# ---------------------------------------------------------------------------

MERIDIAN_FS_FIXTURE: Dict[str, Any] = {
    "prospect": MERIDIAN_FS_PROSPECT,
    "responses": MERIDIAN_FS_RESPONSES,
    "expected_synthesis": MERIDIAN_FS_EXPECTED_SYNTHESIS,
    # Canonical "expected" key matching NorthernCare/AurelianTech fixture structure
    "expected": {
        "overall_score_range": [50, 60],
        "overall_tier": "Developing",
        "dimension_expected": {
            "data_foundation": [44, 60],
            "governance_posture": [30, 46],
            "ai_investment_maturity": [54, 70],
            "org_change_readiness": [47, 63],
            "value_pocket_clarity": [40, 56],
            "regulatory_complexity": [64, 80],
        },
        "recommended_quick_wins": ["QW-001", "QW-005", "QW-012"],
    },
    # Tolerances for integration test assertions (±8 points on each dimension)
    "score_tolerances": {
        "overall": 5,
        "data_foundation": 8,
        "governance_posture": 8,
        "ai_investment_maturity": 8,
        "org_change_readiness": 8,
        "value_pocket_clarity": 8,
        "regulatory_complexity": 8,
    },
}
