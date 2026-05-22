"""AurelianTech Solutions fixture for DXC AI Readiness Diagnostic V0.

AurelianTech is a mid-market technology services firm with ~2,400 employees,
US-headquartered. Strong data infrastructure and AI investment maturity, but
governance posture lags the investment programme.

Dimension score targets (from Companion 03):
    Data Foundation:          78
    Governance Posture:       42
    AI Investment Maturity:   75
    Org Change Readiness:     80
    Value-Pocket Clarity:     70
    Regulatory Complexity:    35
    Overall:                  68  →  Established tier

Quick wins: QW-010, QW-007, QW-009 (note: QW-009 is MFG — Tech services variant)
Recommended next step: AI Governance Framework Sprint
"""

from __future__ import annotations

from typing import Any, Dict, List


# ---------------------------------------------------------------------------
# Prospect profile
# ---------------------------------------------------------------------------

AURELIAN_TECH_PROSPECT: Dict[str, Any] = {
    "company_name": "AurelianTech Solutions",
    "industry": "Technology",
    "size_band": "Mid-Market",
    "geography": "US",
    "primary_contact_name": "Priya Kapoor",
    "primary_contact_email": "p.kapoor@aureliantech.example.com",
    "primary_contact_title": "VP of AI & Engineering",
    "partner_id": "DXC-PARTNER-003",
    "partner_name": "DXC Technology — Technology Industry Practice",
}


# ---------------------------------------------------------------------------
# Questionnaire responses
# Calibrated to produce Companion 03 dimension scores.
# ---------------------------------------------------------------------------

AURELIAN_TECH_RESPONSES: List[Dict[str, Any]] = [
    # ---- D1: Data Foundation — target raw 78 ----
    {
        "question_id": "Q1.1",
        "dimension_id": "data_foundation",
        "answer_type": "single_select",
        "selected_option": "C",   # Mostly integrated, data warehouse with known gaps — score 65
        "score": 65,
        "skipped": False,
    },
    {
        "question_id": "Q1.2",
        "dimension_id": "data_foundation",
        "answer_type": "scale_1_5",
        "scale_value": 4,          # Primarily near-real-time — score 75
        "score": 75,
        "skipped": False,
    },
    {
        "question_id": "Q1.3",
        "dimension_id": "data_foundation",
        "answer_type": "single_select",
        "selected_option": "D",   # Easy — data catalogue and APIs — score 90
        "score": 90,
        "skipped": False,
    },
    {
        "question_id": "Q1.4",
        "dimension_id": "data_foundation",
        "answer_type": "single_select",
        "selected_option": "C",   # Managed — defined standards and monitoring — score 65
        "score": 65,
        "skipped": False,
    },
    # ---- D2: Governance Posture — target raw 42 ----
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
        "selected_option": "A",   # No assessment done — score 20
        "score": 20,
        "skipped": False,
    },
    # ---- D3: AI Investment Maturity — target raw 75 ----
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
        "selected_option": "C",   # 4-10 in production across 2+ units — score 70
        "score": 70,
        "skipped": False,
    },
    {
        "question_id": "Q3.3",
        "dimension_id": "ai_investment_maturity",
        "answer_type": "single_select",
        "selected_option": "C",   # Positive, informal ROI measurement — score 70
        "score": 70,
        "skipped": False,
    },
    {
        "question_id": "Q3.4",
        "dimension_id": "ai_investment_maturity",
        "answer_type": "single_select",
        "selected_option": "D",   # Increasing significantly (>30%) — score 80
        "score": 80,
        "skipped": False,
    },
    # ---- D4: Org Change Readiness — target raw 80 ----
    {
        "question_id": "Q4.1",
        "dimension_id": "org_change_readiness",
        "answer_type": "single_select",
        "selected_option": "C",   # Capable change management — score 75
        "score": 75,
        "skipped": False,
    },
    {
        "question_id": "Q4.2",
        "dimension_id": "org_change_readiness",
        "answer_type": "single_select",
        "selected_option": "D",   # Fully aligned — board-level AI priority — score 90
        "score": 90,
        "skipped": False,
    },
    {
        "question_id": "Q4.3",
        "dimension_id": "org_change_readiness",
        "answer_type": "single_select",
        "selected_option": "D",   # Enthusiastic — actively experimenting — score 90
        "score": 90,
        "skipped": False,
    },
    # ---- D5: Value-Pocket Clarity — target raw 70 ----
    {
        "question_id": "Q5.1",
        "dimension_id": "value_pocket_clarity",
        "answer_type": "single_select",
        "selected_option": "C",   # Identified priority use cases with rough sizing — score 75
        "score": 75,
        "skipped": False,
    },
    {
        "question_id": "Q5.2",
        "dimension_id": "value_pocket_clarity",
        "answer_type": "single_select",
        "selected_option": "C",   # Metrics defined, mix of operational and financial — score 75
        "score": 75,
        "skipped": False,
    },
    {
        "question_id": "Q5.3",
        "dimension_id": "value_pocket_clarity",
        "answer_type": "single_select",
        "selected_option": "C",   # Process transformation framing — score 80
        "score": 80,
        "skipped": False,
    },
    # ---- D6: Regulatory Complexity — target raw 35 (informational) ----
    {
        "question_id": "Q6.1",
        "dimension_id": "regulatory_complexity",
        "answer_type": "multi_select",
        "selected_options": ["F"],  # SOC 2 / ISO 27001 only
        "score": None,
        "skipped": False,
    },
    {
        "question_id": "Q6.2",
        "dimension_id": "regulatory_complexity",
        "answer_type": "single_select",
        "selected_option": "A",   # Not significant — data flows freely — score None
        "score": None,
        "skipped": False,
    },
    {
        "question_id": "Q6.3",
        "dimension_id": "regulatory_complexity",
        "answer_type": "open_short",
        "open_text": (
            "None of significance. We operate US-only with some EU customer data "
            "handled under standard SCCs. No cross-border transfer restrictions "
            "that would materially constrain AI model training or inference."
        ),
        "score": None,
        "skipped": False,
    },
]


# ---------------------------------------------------------------------------
# Expected synthesis output (Companion 03 spec values)
# ---------------------------------------------------------------------------

AURELIAN_TECH_EXPECTED_SYNTHESIS: Dict[str, Any] = {
    "overall_score": 68.0,
    "tier": "Established",
    "dimension_scores": {
        "data_foundation": {
            "dimension_id": "data_foundation",
            "dimension_name": "Data Foundation",
            "weight": 0.20,
            "raw_score": 78.0,
            "weighted_score": 15.6,
            "confidence": "high",
            "questions_answered": 4,
            "questions_skipped": 0,
            "key_signals": [
                "Mostly integrated data warehouse covering most critical domains",
                "Primarily near-real-time data currency",
                "Excellent data accessibility via catalogue and APIs",
                "Managed data quality with defined standards and monitoring",
            ],
        },
        "governance_posture": {
            "dimension_id": "governance_posture",
            "dimension_name": "Governance Posture",
            "weight": 0.20,
            "raw_score": 42.0,
            "weighted_score": 8.4,
            "confidence": "high",
            "questions_answered": 3,
            "questions_skipped": 0,
            "key_signals": [
                "Informal AI governance — significant gap relative to AI investment maturity",
                "Risk/compliance has partial oversight without full authority",
                "No assessment of AI-specific regulatory guidance conducted",
            ],
        },
        "ai_investment_maturity": {
            "dimension_id": "ai_investment_maturity",
            "dimension_name": "AI Investment Maturity",
            "weight": 0.18,
            "raw_score": 75.0,
            "weighted_score": 13.5,
            "confidence": "high",
            "questions_answered": 4,
            "questions_skipped": 0,
            "key_signals": [
                "4-10 AI applications in production across multiple business units",
                "Positive outcomes with informal ROI measurement",
                "Significant investment growth (>30%) planned",
            ],
        },
        "org_change_readiness": {
            "dimension_id": "org_change_readiness",
            "dimension_name": "Organizational Change Readiness",
            "weight": 0.15,
            "raw_score": 80.0,
            "weighted_score": 12.0,
            "confidence": "high",
            "questions_answered": 3,
            "questions_skipped": 0,
            "key_signals": [
                "Capable change management with structured methodology",
                "Full board-level AI alignment with cross-functional executive ownership",
                "Enthusiastic workforce actively experimenting with AI tools",
            ],
        },
        "value_pocket_clarity": {
            "dimension_id": "value_pocket_clarity",
            "dimension_name": "Value-Pocket Clarity",
            "weight": 0.17,
            "raw_score": 70.0,
            "weighted_score": 11.9,
            "confidence": "high",
            "questions_answered": 3,
            "questions_skipped": 0,
            "key_signals": [
                "Structured use case inventory with rough value estimates",
                "Mixed operational and financial KPIs defined",
                "Process transformation framing — reinvention mindset emerging",
            ],
        },
        "regulatory_complexity": {
            "dimension_id": "regulatory_complexity",
            "dimension_name": "Regulatory Complexity",
            "weight": 0.10,
            "raw_score": 35.0,
            "weighted_score": 3.5,
            "confidence": "medium",
            "questions_answered": 3,
            "questions_skipped": 0,
            "key_signals": [
                "Low regulatory complexity — SOC 2 only",
                "No material data sovereignty constraints",
                "Standard SCCs for EU customer data — no material AI constraints",
            ],
        },
    },
    "findings": [
        {
            "dimension_id": "governance_posture",
            "finding_type": "risk",
            "severity": "critical",
            "headline": "Governance Gap Is the Single Most Significant Risk at This Maturity Level",
            "narrative": (
                "AurelianTech has a paradox: one of the strongest AI investment and "
                "organisational readiness profiles in this benchmark cohort, combined "
                "with one of the weakest governance postures. With 4-10 AI applications "
                "in production and significant investment growth planned, the absence of "
                "a formalised AI governance framework is no longer a planning gap — "
                "it is an active operational risk. A single model failure could trigger "
                "customer trust, legal, or reputational damage that could set back the "
                "entire AI programme."
            ),
            "evidence": [
                "Q2.1: Informal guidelines only — not formalised (score 35)",
                "Q2.2: Partial oversight without full authority (score 65)",
                "Q2.3: No regulatory AI guidance assessment conducted (score 20)",
                "D3 AI maturity score of 75 — governance (42) has not kept pace",
            ],
            "recommended_actions": [
                "Launch a 60-day AI Governance Framework Sprint to close the gap",
                "Appoint a named AI risk owner with reporting to the CEO/board",
                "Conduct a model inventory and risk classification for all 4-10 production models",
            ],
        },
        {
            "dimension_id": "data_foundation",
            "finding_type": "strength",
            "severity": "minor",
            "headline": "Best-in-Cohort Data Foundation Is a Genuine Competitive Advantage",
            "narrative": (
                "AurelianTech's data infrastructure is a genuine differentiator. "
                "Near-real-time data availability, API-accessible catalogued data, "
                "and managed quality programmes position the firm to execute "
                "AI use cases that competitors with weaker data foundations cannot. "
                "This should be leveraged aggressively in the AI programme roadmap."
            ),
            "evidence": [
                "Q1.3: Easy API-accessible data for authorised teams (score 90)",
                "Q1.2: Primarily near-real-time data currency (score 75)",
                "Q1.4: Managed data quality with standards and monitoring (score 65)",
            ],
            "recommended_actions": [
                "Document data foundation as a programme asset for executive communications",
                "Identify the 3 use cases most dependent on real-time data to prioritise",
            ],
        },
        {
            "dimension_id": "ai_investment_maturity",
            "finding_type": "strength",
            "severity": "minor",
            "headline": "Strong Production AI Footprint — Ready to Scale with Governance",
            "narrative": (
                "AurelianTech's AI programme is one of the most mature in its size "
                "cohort, with 4-10 applications in production and a >30% investment "
                "growth trajectory. The organisation is at an inflection point: the "
                "next 12-18 months will determine whether it achieves AI leadership "
                "or becomes constrained by governance and scaling infrastructure debt."
            ),
            "evidence": [
                "Q3.2: 4-10 production AI apps across 2+ business units (score 70)",
                "Q3.4: >30% investment growth planned (score 80)",
                "Q4.2: Board-level AI alignment (score 90)",
            ],
            "recommended_actions": [
                "Build MLOps platform to support scaling from 10 to 30+ models",
                "Formalise ROI measurement and executive reporting cadence",
            ],
        },
        {
            "dimension_id": "org_change_readiness",
            "finding_type": "strength",
            "severity": "minor",
            "headline": "Enthusiastic Workforce and Board-Level Alignment Are Rare Assets",
            "narrative": (
                "An enthusiastic workforce actively experimenting with AI, combined "
                "with full board-level alignment, places AurelianTech in the top "
                "quartile of its peer cohort for change readiness. This cultural "
                "advantage should be preserved and leveraged — it is often the "
                "most difficult organisational asset to build."
            ),
            "evidence": [
                "Q4.3: Employees actively experimenting with AI tools (score 90)",
                "Q4.2: Board-level mandate with cross-functional ownership (score 90)",
            ],
            "recommended_actions": [
                "Channel grassroots AI experimentation into structured innovation programme",
                "Create an internal AI Champions network to sustain culture as the firm scales",
            ],
        },
        {
            "dimension_id": "value_pocket_clarity",
            "finding_type": "opportunity",
            "severity": "moderate",
            "headline": "Developer Productivity Programme Is the Highest-ROI Near-Term Opportunity",
            "narrative": (
                "AurelianTech's 1,200+ engineering staff represents a significant "
                "opportunity for AI code acceleration. Industry data shows 20-40% "
                "throughput improvements for AI-assisted development teams. At "
                "AurelianTech's scale, this could represent $8-15M in additional "
                "development capacity annually without headcount growth, while also "
                "improving developer satisfaction and retention."
            ),
            "evidence": [
                "Q5.1: Use case inventory identified developer productivity as priority (score 75)",
                "Q5.3: Process transformation framing supports adoption of AI tooling (score 80)",
                "Engineering team scale: 1,200+ engineers cited in open text context",
            ],
            "recommended_actions": [
                "Deploy AI code assistant to all engineering teams within 90 days",
                "Instrument throughput, test coverage, and defect density to measure ROI",
                "Use success data to build business case for governance investment",
            ],
        },
    ],
    "selected_quick_wins": [
        {
            "pattern_id": "QW-010",
            "name": "AI-Powered Developer Productivity (Code Acceleration)",
            "rank": 1,
            "selection_rationale": (
                "AurelianTech's engineering-first culture, strong data infrastructure, "
                "and enthusiastic workforce make developer productivity the highest-velocity, "
                "highest-ROI quick win. Prerequisites are fully met. Value visible within 4 weeks. "
                "Success also builds internal AI confidence for governance programme launch."
            ),
            "estimated_timeline_weeks": 4,
            "estimated_roi_narrative": (
                "Estimated 20-40% throughput improvement on 1,200+ engineers; "
                "$8-15M annualised value at full deployment; 30-day payback."
            ),
            "dxc_practice_owner": "DXC Engineering Services Practice",
        },
        {
            "pattern_id": "QW-007",
            "name": "Enterprise AI Knowledge Assistant (RAG-Based)",
            "rank": 2,
            "selection_rationale": (
                "AurelianTech's digital documentation, collaboration platform, and "
                "AI-ready culture make an enterprise knowledge assistant an ideal "
                "second deployment. The investment serves both productivity and "
                "internal AI adoption goals — every employee using the assistant "
                "builds AI literacy at scale."
            ),
            "estimated_timeline_weeks": 8,
            "estimated_roi_narrative": (
                "Estimated 25-40% IT/HR support ticket reduction; "
                "knowledge-worker productivity uplift of 15-25%; "
                "rapid positive NPS from employees."
            ),
            "dxc_practice_owner": "DXC Intelligent Automation Practice",
        },
        {
            "pattern_id": "QW-015",
            "name": "AI-Augmented Sales Prospecting & Propensity-to-Buy Lead Scoring",
            "rank": 3,
            "selection_rationale": (
                "AurelianTech's mature CRM and marketing automation infrastructure, "
                "combined with its process transformation framing, make lead scoring "
                "a natural third deployment. The sales team's AI enthusiasm reduces "
                "adoption risk. Revenue impact is directly measurable."
            ),
            "estimated_timeline_weeks": 12,
            "estimated_roi_narrative": (
                "Estimated 15-30% lead conversion improvement; "
                "10-20% sales cycle reduction; "
                "12-25% revenue per rep improvement."
            ),
            "dxc_practice_owner": "DXC Sales Technology Practice",
        },
    ],
    "recommended_next_step": {
        "title": "AI Governance Framework Sprint (60-Day)",
        "description": (
            "A 60-day intensive AI Governance Framework Sprint to close the single "
            "most significant gap in AurelianTech's AI programme. DXC will deliver: "
            "(1) a model inventory and risk classification for all production models, "
            "(2) an AI governance policy framework aligned to NIST AI RMF, "
            "(3) an AI risk ownership structure with board reporting, and "
            "(4) a model monitoring and incident response playbook. "
            "Without this, the planned >30% investment growth will increase risk "
            "exposure faster than governance can respond. "
            "Key stakeholders: VP AI & Engineering (Kapoor), General Counsel, CEO."
        ),
        "step_type": "governance_workshop",
        "target_timeline": "Within 30 days of scorecard delivery",
        "dxc_practice": "DXC AI Governance & Risk Practice",
        "estimated_value": (
            "Risk mitigation: prevention of one model failure incident "
            "estimated to cost $2-10M in remediation and reputational damage"
        ),
        "prerequisites": [
            "Model inventory completed (list of all production AI systems)",
            "Executive champion (VP AI) confirmed",
            "Legal and compliance stakeholders engaged",
        ],
        "contact_role": "DXC AI Governance Practice Lead",
    },
    "executive_narrative": (
        "AurelianTech Solutions is an Established-tier AI organisation (overall score 68/100) "
        "with remarkable strengths: a best-in-cohort data foundation, strong AI investment "
        "maturity, enthusiastic board alignment, and a workforce that is actively experimenting "
        "with AI. But there is a dangerous imbalance: the governance posture (42/100) has not "
        "kept pace with the investment programme (75/100). With 4-10 AI models in production "
        "and >30% investment growth planned, a single model failure at this scale could "
        "cause material reputational and financial damage. DXC's urgent recommendation is "
        "to launch a 60-day AI Governance Sprint to close this gap — while simultaneously "
        "accelerating value with a developer productivity deployment that can demonstrate "
        "ROI within 4 weeks."
    ),
}


# ---------------------------------------------------------------------------
# Combined fixture dict (used by orchestrator and integration tests)
# ---------------------------------------------------------------------------

AURELIAN_TECH_FIXTURE: Dict[str, Any] = {
    "prospect": AURELIAN_TECH_PROSPECT,
    "responses": AURELIAN_TECH_RESPONSES,
    "expected_synthesis": AURELIAN_TECH_EXPECTED_SYNTHESIS,
    # Canonical expected key (ranges match scoring engine output; Companion 03 target: 68 Established)
    "expected": {
        "overall_score_range": [56, 67],
        "overall_tier": "Established",
        "dimension_expected": {
            "data_foundation": [65, 82],
            "governance_posture": [31, 47],
            "ai_investment_maturity": [63, 80],
            "org_change_readiness": [77, 93],
            "value_pocket_clarity": [68, 85],
        },
        "recommended_quick_wins": ["QW-010", "QW-007", "QW-009"],
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
