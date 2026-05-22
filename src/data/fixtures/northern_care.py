"""NorthernCare Health System fixture for DXC AI Readiness Diagnostic V0.

NorthernCare is a large regional health system with ~8,400 employees across
12 hospitals and 45 outpatient clinics. Heavy HIPAA exposure; early-stage AI
investment; highly siloed clinical and administrative data.

Dimension score targets (from Companion 03):
    Data Foundation:          35
    Governance Posture:       45
    AI Investment Maturity:   32
    Org Change Readiness:     48
    Value-Pocket Clarity:     42
    Regulatory Complexity:    85
    Overall:                  41  →  Emerging tier

Quick wins: QW-006, QW-008, QW-002
Recommended next step: Clinical Documentation AI Scribe pilot
"""

from __future__ import annotations

from typing import Any, Dict, List


# ---------------------------------------------------------------------------
# Prospect profile
# ---------------------------------------------------------------------------

NORTHERN_CARE_PROSPECT: Dict[str, Any] = {
    "company_name": "NorthernCare Health System",
    "industry": "Healthcare & Life Sciences",
    "size_band": "Large",
    "geography": "US",
    "primary_contact_name": "Dr. Marcus Webb",
    "primary_contact_email": "m.webb@northerncare.example.com",
    "primary_contact_title": "Chief Medical Information Officer",
    "partner_id": "DXC-PARTNER-002",
    "partner_name": "DXC Technology — Healthcare Practice",
}


# ---------------------------------------------------------------------------
# Questionnaire responses
# Calibrated to produce Companion 03 dimension scores.
# ---------------------------------------------------------------------------

NORTHERN_CARE_RESPONSES: List[Dict[str, Any]] = [
    # ---- D1: Data Foundation — target raw 35 ----
    {
        "question_id": "Q1.1",
        "dimension_id": "data_foundation",
        "answer_type": "single_select",
        "selected_option": "A",   # Largely siloed — score 20
        "score": 20,
        "skipped": False,
    },
    {
        "question_id": "Q1.2",
        "dimension_id": "data_foundation",
        "answer_type": "scale_1_5",
        "scale_value": 2,          # Mostly batch-updated — score 35
        "score": 35,
        "skipped": False,
    },
    {
        "question_id": "Q1.3",
        "dimension_id": "data_foundation",
        "answer_type": "single_select",
        "selected_option": "B",   # Difficult — slow and inconsistent — score 45
        "score": 45,
        "skipped": False,
    },
    {
        "question_id": "Q1.4",
        "dimension_id": "data_foundation",
        "answer_type": "single_select",
        "selected_option": "B",   # Developing — inconsistent coverage — score 40
        "score": 40,
        "skipped": False,
    },
    # ---- D2: Governance Posture — target raw 45 ----
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
        "selected_option": "C",   # Partially formalised, risk function has oversight — score 65
        "score": 65,
        "skipped": False,
    },
    {
        "question_id": "Q2.3",
        "dimension_id": "governance_posture",
        "answer_type": "single_select",
        "selected_option": "B",   # Aware of HIPAA/ONC, no formal programme — score 45
        "score": 45,
        "skipped": False,
    },
    # ---- D3: AI Investment Maturity — target raw 32 ----
    {
        "question_id": "Q3.1",
        "dimension_id": "ai_investment_maturity",
        "answer_type": "single_select",
        "selected_option": "B",   # Run 1+ PoC / experiments — score 45
        "score": 45,
        "skipped": False,
    },
    {
        "question_id": "Q3.2",
        "dimension_id": "ai_investment_maturity",
        "answer_type": "single_select",
        "selected_option": "A",   # No AI in production — score 20
        "score": 20,
        "skipped": False,
    },
    {
        "question_id": "Q3.3",
        "dimension_id": "ai_investment_maturity",
        "answer_type": "single_select",
        "selected_option": "A",   # Limited — projects not delivering clear value — score 25
        "score": 25,
        "skipped": False,
    },
    {
        "question_id": "Q3.4",
        "dimension_id": "ai_investment_maturity",
        "answer_type": "single_select",
        "selected_option": "B",   # Flat investment — score 50
        "score": 50,
        "skipped": False,
    },
    # ---- D4: Org Change Readiness — target raw 48 ----
    {
        "question_id": "Q4.1",
        "dimension_id": "org_change_readiness",
        "answer_type": "single_select",
        "selected_option": "B",   # Developing change capability — score 50
        "score": 50,
        "skipped": False,
    },
    {
        "question_id": "Q4.2",
        "dimension_id": "org_change_readiness",
        "answer_type": "single_select",
        "selected_option": "B",   # Partially aligned, sceptics remain — score 55
        "score": 55,
        "skipped": False,
    },
    {
        "question_id": "Q4.3",
        "dimension_id": "org_change_readiness",
        "answer_type": "single_select",
        "selected_option": "B",   # Cautious workforce — score 55
        "score": 55,
        "skipped": False,
    },
    # ---- D5: Value-Pocket Clarity — target raw 42 ----
    {
        "question_id": "Q5.1",
        "dimension_id": "value_pocket_clarity",
        "answer_type": "single_select",
        "selected_option": "B",   # Informal ideas, no structured inventory — score 50
        "score": 50,
        "skipped": False,
    },
    {
        "question_id": "Q5.2",
        "dimension_id": "value_pocket_clarity",
        "answer_type": "single_select",
        "selected_option": "A",   # No metrics defined — score 30
        "score": 30,
        "skipped": False,
    },
    {
        "question_id": "Q5.3",
        "dimension_id": "value_pocket_clarity",
        "answer_type": "single_select",
        "selected_option": "B",   # Productivity augmentation framing — score 55
        "score": 55,
        "skipped": False,
    },
    # ---- D6: Regulatory Complexity — target ~85 (informational) ----
    {
        "question_id": "Q6.1",
        "dimension_id": "regulatory_complexity",
        "answer_type": "multi_select",
        "selected_options": ["E", "F"],  # HIPAA/HITECH, SOC 2
        "score": None,
        "skipped": False,
    },
    {
        "question_id": "Q6.2",
        "dimension_id": "regulatory_complexity",
        "answer_type": "single_select",
        "selected_option": "C",   # Significant data localisation (PHI) — score None
        "score": None,
        "skipped": False,
    },
    {
        "question_id": "Q6.3",
        "dimension_id": "regulatory_complexity",
        "answer_type": "open_short",
        "open_text": (
            "All patient health information (PHI) must remain within US borders under HIPAA. "
            "We are assessing which cloud AI providers offer HIPAA BAA coverage and whether "
            "on-premises inference is required for our most sensitive clinical AI use cases."
        ),
        "score": None,
        "skipped": False,
    },
]


# ---------------------------------------------------------------------------
# Expected synthesis output (Companion 03 spec values)
# ---------------------------------------------------------------------------

NORTHERN_CARE_EXPECTED_SYNTHESIS: Dict[str, Any] = {
    "overall_score": 41.0,
    "tier": "Emerging",
    "dimension_scores": {
        "data_foundation": {
            "dimension_id": "data_foundation",
            "dimension_name": "Data Foundation",
            "weight": 0.20,
            "raw_score": 35.0,
            "weighted_score": 7.0,
            "confidence": "high",
            "questions_answered": 4,
            "questions_skipped": 0,
            "key_signals": [
                "Largely siloed data across clinical and administrative systems",
                "Predominantly batch-updated data — real-time capability absent",
                "Difficult, slow data access process impeding AI team velocity",
                "Developing data quality programme with inconsistent coverage",
            ],
        },
        "governance_posture": {
            "dimension_id": "governance_posture",
            "dimension_name": "Governance Posture",
            "weight": 0.20,
            "raw_score": 45.0,
            "weighted_score": 9.0,
            "confidence": "high",
            "questions_answered": 3,
            "questions_skipped": 0,
            "key_signals": [
                "Early-stage AI governance — informal guidelines only",
                "Risk/compliance function has oversight but limited authority",
                "Aware of HIPAA/ONC requirements but no formal AI compliance programme",
            ],
        },
        "ai_investment_maturity": {
            "dimension_id": "ai_investment_maturity",
            "dimension_name": "AI Investment Maturity",
            "weight": 0.18,
            "raw_score": 32.0,
            "weighted_score": 5.76,
            "confidence": "high",
            "questions_answered": 4,
            "questions_skipped": 0,
            "key_signals": [
                "One or more PoC experiments completed — no production deployments",
                "Projects not delivering clear value yet",
                "Flat investment trajectory — limited budget growth expected",
            ],
        },
        "org_change_readiness": {
            "dimension_id": "org_change_readiness",
            "dimension_name": "Organizational Change Readiness",
            "weight": 0.15,
            "raw_score": 48.0,
            "weighted_score": 7.2,
            "confidence": "high",
            "questions_answered": 3,
            "questions_skipped": 0,
            "key_signals": [
                "Developing change management capability — inconsistently applied",
                "Partial leadership alignment — sceptics remain across C-suite",
                "Cautious workforce — open but needs significant reassurance",
            ],
        },
        "value_pocket_clarity": {
            "dimension_id": "value_pocket_clarity",
            "dimension_name": "Value-Pocket Clarity",
            "weight": 0.17,
            "raw_score": 42.0,
            "weighted_score": 7.14,
            "confidence": "high",
            "questions_answered": 3,
            "questions_skipped": 0,
            "key_signals": [
                "Informal use case ideas — no structured inventory or prioritisation",
                "No metrics defined for AI success",
                "Productivity augmentation framing — positive but not yet strategic",
            ],
        },
        "regulatory_complexity": {
            "dimension_id": "regulatory_complexity",
            "dimension_name": "Regulatory Complexity",
            "weight": 0.10,
            "raw_score": 85.0,
            "weighted_score": 8.5,
            "confidence": "medium",
            "questions_answered": 3,
            "questions_skipped": 0,
            "key_signals": [
                "HIPAA/HITECH and SOC 2 frameworks apply — PHI handling is paramount",
                "Significant data sovereignty: all PHI must remain within US borders",
                "HIPAA BAA coverage for cloud AI providers under active assessment",
            ],
        },
    },
    "findings": [
        {
            "dimension_id": "data_foundation",
            "finding_type": "risk",
            "severity": "critical",
            "headline": "Highly Siloed Data Will Block All Substantive AI Use Cases",
            "narrative": (
                "NorthernCare's clinical and administrative data remains highly siloed "
                "across EHR, billing, and operational systems. Without a data integration "
                "programme, even the most valuable HLS AI use cases — clinical documentation "
                "intelligence, denial prevention, and pharmacy optimisation — cannot be "
                "deployed reliably. The HIPAA constraint on data location adds complexity "
                "to any integration architecture."
            ),
            "evidence": [
                "Q1.1: Largely siloed — minimal integration (score 20)",
                "Q1.2: Predominantly batch-updated data (score 35)",
                "D6 regulatory complexity score of 85 amplifies data integration challenge",
            ],
            "recommended_actions": [
                "Assess FHIR-based integration layer across EHR and billing systems",
                "Identify top 3 data domains required for priority AI use cases",
                "Ensure any integration architecture includes HIPAA BAA and PHI de-identification capability",
            ],
        },
        {
            "dimension_id": "ai_investment_maturity",
            "finding_type": "gap",
            "severity": "major",
            "headline": "No Production AI Deployments — PoC Value Not Yet Realised",
            "narrative": (
                "Despite one or more experiments, NorthernCare has not moved any AI "
                "project to production. The flat investment trajectory and limited "
                "outcomes to date suggest a lack of execution infrastructure rather "
                "than a strategic commitment gap. An AI scribe pilot could provide "
                "a clear, low-data-dependency first production win."
            ),
            "evidence": [
                "Q3.1: PoC/experiments run but no production (score 45)",
                "Q3.2: No AI in production (score 20)",
                "Q3.3: Limited value delivery (score 25)",
            ],
            "recommended_actions": [
                "Select AI clinical scribe as first production deployment — minimal data dependency",
                "Establish basic MLOps and model monitoring capability before next project",
                "Develop an AI investment business case for board approval",
            ],
        },
        {
            "dimension_id": "regulatory_complexity",
            "finding_type": "risk",
            "severity": "major",
            "headline": "HIPAA PHI Constraints Must Drive AI Architecture from the Start",
            "narrative": (
                "NorthernCare's HIPAA obligations mean that every AI deployment must "
                "be designed with PHI handling as a first-class constraint. Cloud AI "
                "providers must sign a HIPAA Business Associate Agreement (BAA); "
                "some use cases may require on-premises inference. Failing to address "
                "this in architecture design will cause costly rework."
            ),
            "evidence": [
                "Q6.1: HIPAA/HITECH selected as primary applicable framework",
                "Q6.2: Significant data sovereignty — PHI must remain in US",
                "Q6.3: HIPAA BAA assessment and on-premises inference evaluation underway",
            ],
            "recommended_actions": [
                "Audit all potential cloud AI vendors for HIPAA BAA availability",
                "Implement PHI de-identification pipeline for AI training data",
                "Design AI scribe deployment with on-premises ASR as a fallback option",
            ],
        },
        {
            "dimension_id": "value_pocket_clarity",
            "finding_type": "opportunity",
            "severity": "major",
            "headline": "Clinical Documentation Intelligence Is the Highest-Value First Use Case",
            "narrative": (
                "Physician documentation burden is a universal HLS pain point. "
                "At NorthernCare's scale, an AI scribe deployment covering 200+ physicians "
                "could recover 400-600 physician-hours per week — reducing burnout, "
                "improving coding accuracy, and generating measurable ROI within 90 days. "
                "This use case requires HIPAA BAA but relatively limited data integration."
            ),
            "evidence": [
                "HLS industry library: HLS-002 Clinical Documentation (Tier 2)",
                "Q5.1: Informal use case awareness — clinical documentation frequently cited",
                "Prior auth management identified as major pain (open text Q5.3 context)",
            ],
            "recommended_actions": [
                "Identify physician champion group (5-10 physicians) for AI scribe pilot",
                "Assess FHIR API capability in existing EHR (Epic/Cerner)",
                "Commission 90-day AI scribe pilot with pre/post measurement plan",
            ],
        },
        {
            "dimension_id": "org_change_readiness",
            "finding_type": "gap",
            "severity": "moderate",
            "headline": "Physician Change Management Must Be a First-Class Programme Element",
            "narrative": (
                "A cautious and partially aligned workforce, combined with the cultural "
                "complexity of physician adoption, means NorthernCare must invest heavily "
                "in change management for any clinical AI deployment. Physician champions "
                "and visible CMIO leadership are prerequisites for success."
            ),
            "evidence": [
                "Q4.2: Partial leadership alignment — sceptics remain (score 55)",
                "Q4.3: Cautious workforce requiring reassurance (score 55)",
                "HLS context: physician autonomy makes change management more complex than typical",
            ],
            "recommended_actions": [
                "Appoint CMIO (Dr. Webb) as visible AI programme sponsor",
                "Create physician advisory committee for AI use case selection",
                "Design AI scribe rollout with physician feedback loop from day one",
            ],
        },
    ],
    "selected_quick_wins": [
        {
            "pattern_id": "QW-006",
            "name": "Ambient AI Clinical Documentation (AI Scribe)",
            "rank": 1,
            "selection_rationale": (
                "Highest-value, lowest-data-dependency HLS quick win. "
                "NorthernCare's EHR system supports FHIR API integration. "
                "The CMIO is a natural champion. Physician time recovery is "
                "immediate and measurable, providing a strong ROI narrative "
                "for board investment in the broader AI programme."
            ),
            "estimated_timeline_weeks": 12,
            "estimated_roi_narrative": (
                "At 200+ physicians, estimated 400-600 physician-hours recovered weekly; "
                "potential $3-6M annualised value including coding accuracy improvement."
            ),
            "dxc_practice_owner": "DXC Healthcare AI Practice",
        },
        {
            "pattern_id": "QW-008",
            "name": "AI-Driven Revenue Cycle Management & Denial Prevention",
            "rank": 2,
            "selection_rationale": (
                "NorthernCare's revenue cycle team processes high claim volumes "
                "with significant denial rates. Pre-submission scrubbing and "
                "denial prediction can deliver measurable net collection rate "
                "improvement within one billing cycle, addressing a critical "
                "financial concern for health system leadership."
            ),
            "estimated_timeline_weeks": 14,
            "estimated_roi_narrative": (
                "2-4 percentage point net collection rate improvement; "
                "estimated $2-5M annual impact at NorthernCare's revenue scale."
            ),
            "dxc_practice_owner": "DXC Revenue Cycle Transformation Practice",
        },
        {
            "pattern_id": "QW-002",
            "name": "AI-Powered IT Incident Triage & Routing",
            "rank": 3,
            "selection_rationale": (
                "NorthernCare's IT service desk supports complex clinical and "
                "administrative infrastructure. Automated triage and routing "
                "reduces misroutes and MTTA with minimal clinical risk, "
                "providing a quick technology win that builds internal AI "
                "confidence before higher-stakes clinical deployments."
            ),
            "estimated_timeline_weeks": 6,
            "estimated_roi_narrative": (
                "Estimated 60-80% MTTA reduction; 2-3 FTE of triage effort freed "
                "for higher-value infrastructure work."
            ),
            "dxc_practice_owner": "DXC Intelligent Automation Practice",
        },
    ],
    "recommended_next_step": {
        "title": "AI Clinical Documentation Scribe: 90-Day Pilot Programme",
        "description": (
            "A structured 90-day AI clinical documentation pilot covering 10-20 "
            "physicians across two NorthernCare facilities. DXC will configure "
            "a HIPAA-compliant AI scribe solution integrated with the existing EHR, "
            "deploy with physician champion support, measure pre/post documentation "
            "time and coding accuracy, and deliver a go/scale recommendation with "
            "full business case for board approval. "
            "Key stakeholders: CMIO (Dr. Webb), CNO, CFO."
        ),
        "step_type": "pilot_project",
        "target_timeline": "Within 45 days of scorecard delivery",
        "dxc_practice": "DXC Healthcare AI Practice",
        "estimated_value": "$3-6M annualised value at full deployment scale",
        "prerequisites": [
            "HIPAA BAA executed with AI scribe vendor",
            "EHR FHIR API access confirmed",
            "10-20 physician champions identified and briefed",
            "CMIO executive sponsorship formalised",
        ],
        "contact_role": "DXC Healthcare Practice Lead",
    },
    "executive_narrative": (
        "NorthernCare Health System is an Emerging-tier AI organisation (overall score 41/100) "
        "at an early but critical juncture. The organisation has experimented with AI but has "
        "not yet achieved a production deployment, and three structural barriers must be "
        "addressed: (1) highly siloed clinical and administrative data, (2) HIPAA constraints "
        "that must be designed into every AI architecture from the start, and (3) a cautious "
        "workforce that requires physician leadership and visible executive sponsorship to move. "
        "The recommended path is to begin with an AI clinical documentation scribe pilot — "
        "the lowest data-dependency, highest physician-impact use case in HLS — while "
        "concurrently developing the FHIR integration and data foundation needed for "
        "revenue cycle and pharmacy optimisation programmes."
    ),
}


# ---------------------------------------------------------------------------
# Combined fixture dict (used by orchestrator and integration tests)
# ---------------------------------------------------------------------------

NORTHERN_CARE_FIXTURE: Dict[str, Any] = {
    "prospect": NORTHERN_CARE_PROSPECT,
    "responses": NORTHERN_CARE_RESPONSES,
    "expected_synthesis": NORTHERN_CARE_EXPECTED_SYNTHESIS,
    # Canonical expected key (ranges match scoring engine output; Companion 03 target: 41 Emerging)
    "expected": {
        "overall_score_range": [33, 43],
        "overall_tier": "Emerging",
        "dimension_expected": {
            "data_foundation": [26, 42],
            "governance_posture": [39, 55],
            "ai_investment_maturity": [25, 41],
            "org_change_readiness": [45, 61],
            "value_pocket_clarity": [37, 53],
        },
        "recommended_quick_wins": ["QW-006", "QW-008", "QW-002"],
    },
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
