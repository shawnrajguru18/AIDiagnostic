"""
Complete 20-question pool for the DXC AI Readiness Diagnostic V0.
Source: Companion 01 — Question Pool Specification.

All questions, options, scores, skip/branching logic, persona tags, and
industry tags are encoded verbatim from the specification.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Question pool — raw dicts (validated by agents at runtime)
# Each entry maps to the QuestionPoolEntry schema in src.models.schemas.
# ---------------------------------------------------------------------------
#
# Dimension weights:
#   D1 Data Foundation          0.20  (4 questions)
#   D2 Governance Posture       0.20  (3 questions)
#   D3 AI Investment Maturity   0.18  (4 questions)
#   D4 Org Change Readiness     0.15  (3 questions)
#   D5 Value-Pocket Clarity     0.17  (3 questions)
#   D6 Regulatory Complexity    0.10  (3 questions)

QUESTION_POOL: List[Dict[str, Any]] = [

    # =========================================================================
    # DIMENSION 1: DATA FOUNDATION  (weight 0.20, questions Q1.1–Q1.4)
    # =========================================================================

    # Q1.1 — Data location / integration
    # single_select | question weight 0.30 | options A-D with scores 20/40/65/90
    {
        "question_id": "Q1.1",
        "dimension_id": "data_foundation",
        "question_text": (
            "Where does the data that drives your most important business decisions "
            "currently live, and how integrated is it?"
        ),
        "question_type": "single_select",
        "weight": 0.30,
        "options": [
            {
                "option_id": "A",
                "label": "Largely siloed in separate systems / departments with minimal integration",
                "score": 20,
                "description": "Data exists in disconnected silos with little cross-system visibility.",
            },
            {
                "option_id": "B",
                "label": "Partially integrated — some data pipelines exist but gaps remain",
                "score": 40,
                "description": "Some integration has been achieved but material gaps persist.",
            },
            {
                "option_id": "C",
                "label": "Mostly integrated through a data warehouse or data lake with known gaps",
                "score": 65,
                "description": "A central store exists and covers most critical domains.",
            },
            {
                "option_id": "D",
                "label": "Highly integrated — unified data platform with real-time or near-real-time access",
                "score": 90,
                "description": "Unified platform with broad coverage and fast access.",
            },
        ],
        "scale_anchors": None,
        "max_chars": None,
        "persona_tags": None,
        "industry_tags": None,
        "skip_logic": None,
        "branching_logic": None,
        "helper_text": (
            "Think about the data used for decisions in finance, operations, "
            "customer management, and supply chain."
        ),
        "persona_variant_text": None,
    },

    # Q1.2 — Decision data currency (scale 1-5)
    # scale_1_5 | question weight 0.25 | scores 15/35/55/75/95
    {
        "question_id": "Q1.2",
        "dimension_id": "data_foundation",
        "question_text": (
            "How current is the data that feeds your key business decisions? "
            "Rate on a scale of 1 (mostly stale / batch) to 5 (real-time or near-real-time)."
        ),
        "question_type": "scale_1_5",
        "weight": 0.25,
        "options": None,
        "scale_anchors": [
            {"value": 1, "label": "Data is predominantly stale (days or weeks old)", "score": 15},
            {"value": 2, "label": "Mostly batch-updated; some near-real-time feeds", "score": 35},
            {"value": 3, "label": "Mix of batch and near-real-time; adequate for most decisions", "score": 55},
            {"value": 4, "label": "Primarily near-real-time with limited batch lag", "score": 75},
            {"value": 5, "label": "Real-time or near-real-time across all critical domains", "score": 95},
        ],
        "max_chars": None,
        "persona_tags": None,
        "industry_tags": None,
        "skip_logic": None,
        "branching_logic": None,
        "helper_text": (
            "Consider the latency between an event occurring and when it is reflected "
            "in your reports."
        ),
        "persona_variant_text": None,
    },

    # Q1.3 — Data accessibility for AI
    # single_select | weight 0.25 | scores 25/45/70/90
    {
        "question_id": "Q1.3",
        "dimension_id": "data_foundation",
        "question_text": (
            "When your teams need data to build or run an AI model or analytics use case, "
            "how easy is it to access the right data?"
        ),
        "question_type": "single_select",
        "weight": 0.25,
        "options": [
            {
                "option_id": "A",
                "label": "Very difficult — data access requires lengthy approval chains and manual extraction",
                "score": 25,
                "description": "High friction; access takes weeks and requires significant manual effort.",
            },
            {
                "option_id": "B",
                "label": "Difficult — there is a process but it is slow and inconsistent",
                "score": 45,
                "description": "Process exists but delays and inconsistency impede velocity.",
            },
            {
                "option_id": "C",
                "label": "Moderate — self-service for some domains, gated access for sensitive data",
                "score": 70,
                "description": "Self-service available for many domains; sensitive data is governed.",
            },
            {
                "option_id": "D",
                "label": "Easy — data catalogue and APIs make data readily available to authorised teams",
                "score": 90,
                "description": "Catalogued, API-accessible data; minimal friction for authorised users.",
            },
        ],
        "scale_anchors": None,
        "max_chars": None,
        "persona_tags": None,
        "industry_tags": None,
        "skip_logic": None,
        "branching_logic": None,
        "helper_text": "Consider both technical accessibility and governance/approval processes.",
        "persona_variant_text": None,
    },

    # Q1.4 — Data quality posture
    # single_select | weight 0.20 | scores 20/40/65/85
    {
        "question_id": "Q1.4",
        "dimension_id": "data_foundation",
        "question_text": (
            "How would you characterise your organisation's current approach "
            "to data quality management?"
        ),
        "question_type": "single_select",
        "weight": 0.20,
        "options": [
            {
                "option_id": "A",
                "label": "Reactive — data quality issues are fixed ad hoc when they cause problems",
                "score": 20,
                "description": "No systematic programme; issues addressed only when they surface.",
            },
            {
                "option_id": "B",
                "label": "Developing — some data quality rules exist but coverage is inconsistent",
                "score": 40,
                "description": "Partial rules and monitoring in place; gaps remain.",
            },
            {
                "option_id": "C",
                "label": "Managed — defined data quality standards and monitoring for critical domains",
                "score": 65,
                "description": "Standards exist and are actively monitored for key data domains.",
            },
            {
                "option_id": "D",
                "label": "Optimised — continuous data quality monitoring, SLAs, and automated remediation",
                "score": 85,
                "description": "Mature programme with automation, SLAs, and continuous improvement.",
            },
        ],
        "scale_anchors": None,
        "max_chars": None,
        "persona_tags": None,
        "industry_tags": None,
        "skip_logic": None,
        "branching_logic": None,
        "helper_text": "Think about whether data quality is actively measured and who owns it.",
        "persona_variant_text": None,
    },

    # =========================================================================
    # DIMENSION 2: GOVERNANCE POSTURE  (weight 0.20, questions Q2.1–Q2.3)
    # =========================================================================

    # Q2.1 — Defined AI governance framework
    # single_select | weight 0.40 | scores 15/35/65/90
    {
        "question_id": "Q2.1",
        "dimension_id": "governance_posture",
        "question_text": (
            "Does your organisation have a defined AI governance framework "
            "— policies, standards, or guardrails for how AI is built and deployed?"
        ),
        "question_type": "single_select",
        "weight": 0.40,
        "options": [
            {
                "option_id": "A",
                "label": "No — we have no formal AI governance policies or standards",
                "score": 15,
                "description": "No formal framework exists.",
            },
            {
                "option_id": "B",
                "label": "Early stages — we have some informal guidelines but nothing formalised",
                "score": 35,
                "description": "Informal guidance only; not codified or enforced.",
            },
            {
                "option_id": "C",
                "label": "In progress — formal policies are being developed or partially rolled out",
                "score": 65,
                "description": "Policy work underway; partial rollout across the organisation.",
            },
            {
                "option_id": "D",
                "label": "Yes — we have a comprehensive AI governance framework that is actively enforced",
                "score": 90,
                "description": "Comprehensive framework in place, actively enforced and maintained.",
            },
        ],
        "scale_anchors": None,
        "max_chars": None,
        "persona_tags": None,
        "industry_tags": None,
        "skip_logic": None,
        "branching_logic": None,
        "helper_text": (
            "This includes AI ethics policies, model risk management, explainability "
            "requirements, and bias testing."
        ),
        "persona_variant_text": None,
    },

    # Q2.2 — AI risk accountability
    # single_select | weight 0.30 | scores 15/35/65/90
    {
        "question_id": "Q2.2",
        "dimension_id": "governance_posture",
        "question_text": "Who is accountable for AI-related risks in your organisation?",
        "question_type": "single_select",
        "weight": 0.30,
        "options": [
            {
                "option_id": "A",
                "label": "Unclear — no single owner; accountability is diffuse or absent",
                "score": 15,
                "description": "Risk ownership is not defined.",
            },
            {
                "option_id": "B",
                "label": "Informal — individual project teams manage their own AI risk",
                "score": 35,
                "description": "Risk managed at project level without enterprise coordination.",
            },
            {
                "option_id": "C",
                "label": "Partially formalised — a risk or compliance function has oversight but limited authority",
                "score": 65,
                "description": "Oversight exists but lacks full authority or cross-functional reach.",
            },
            {
                "option_id": "D",
                "label": "Clearly defined — a named executive or committee owns AI risk with board visibility",
                "score": 90,
                "description": "Named executive or committee; board-level reporting cadence.",
            },
        ],
        "scale_anchors": None,
        "max_chars": None,
        "persona_tags": None,
        "industry_tags": None,
        "skip_logic": None,
        "branching_logic": None,
        "helper_text": (
            "Consider who would be accountable if an AI model produced a harmful "
            "or incorrect output."
        ),
        "persona_variant_text": None,
    },

    # Q2.3 — Industry-specific AI guidance (FS/HLS primary)
    # single_select | weight 0.30 | scores 20/45/70/90
    {
        "question_id": "Q2.3",
        "dimension_id": "governance_posture",
        "question_text": (
            "Has your organisation assessed the AI-specific regulatory guidance "
            "or requirements from your industry regulators (e.g., SR 11-7 for banks, "
            "ONC rules for health IT, EU AI Act for EU-operating firms)?"
        ),
        "question_type": "single_select",
        "weight": 0.30,
        "options": [
            {
                "option_id": "A",
                "label": "No assessment has been done",
                "score": 20,
                "description": "No review of regulatory AI guidance undertaken.",
            },
            {
                "option_id": "B",
                "label": "Aware of requirements but no formal compliance programme",
                "score": 45,
                "description": "Team is aware but has not launched a compliance programme.",
            },
            {
                "option_id": "C",
                "label": "Compliance programme in progress — gap assessment underway",
                "score": 70,
                "description": "Formal gap assessment and remediation in progress.",
            },
            {
                "option_id": "D",
                "label": "Compliant — regulatory guidance is embedded in our AI governance framework",
                "score": 90,
                "description": "Regulatory requirements fully embedded; regularly reviewed.",
            },
        ],
        "scale_anchors": None,
        "max_chars": None,
        "persona_tags": None,
        # Primary for FS and HLS; shown to all but weighted more in those verticals
        "industry_tags": ["Financial Services", "Healthcare & Life Sciences"],
        "skip_logic": None,
        "branching_logic": None,
        "helper_text": (
            "If your industry does not have specific AI regulations, answer based on "
            "how well you track emerging guidance."
        ),
        "persona_variant_text": None,
    },

    # =========================================================================
    # DIMENSION 3: AI INVESTMENT MATURITY  (weight 0.18, questions Q3.1–Q3.4)
    # =========================================================================

    # Q3.1 — AI initiatives launched
    # single_select | weight 0.30 | scores 25/45/70/85
    # skip_logic: if A → skip Q3.2 and Q3.3
    {
        "question_id": "Q3.1",
        "dimension_id": "ai_investment_maturity",
        "question_text": (
            "How would you describe your organisation's AI initiative history to date?"
        ),
        "question_type": "single_select",
        "weight": 0.30,
        "options": [
            {
                "option_id": "A",
                "label": "We have not launched any AI initiatives",
                "score": 25,
                "description": "No AI projects started.",
            },
            {
                "option_id": "B",
                "label": "We have run one or more AI experiments or proof-of-concept projects",
                "score": 45,
                "description": "Exploration underway; PoC or pilot phase.",
            },
            {
                "option_id": "C",
                "label": "We have multiple AI projects in flight, including some in production",
                "score": 70,
                "description": "Portfolio of projects; production deployments exist.",
            },
            {
                "option_id": "D",
                "label": "AI is embedded across multiple business functions and product lines",
                "score": 85,
                "description": "Mature, multi-function AI programme driving business outcomes.",
            },
        ],
        "scale_anchors": None,
        "max_chars": None,
        "persona_tags": None,
        "industry_tags": None,
        # If Q3.1 = A, skip Q3.2 and Q3.3
        "skip_logic": {"A": ["Q3.2", "Q3.3"]},
        "branching_logic": None,
        "helper_text": (
            "Include internal tools, automation, analytics models, and generative AI projects."
        ),
        "persona_variant_text": None,
    },

    # Q3.2 — Production AI today (skip if Q3.1 = A)
    # single_select | weight 0.30 | scores 20/45/70/90
    {
        "question_id": "Q3.2",
        "dimension_id": "ai_investment_maturity",
        "question_text": (
            "Which of the following best describes your current production AI footprint?"
        ),
        "question_type": "single_select",
        "weight": 0.30,
        "options": [
            {
                "option_id": "A",
                "label": "No AI in production — all work is in pilot or experiment phase",
                "score": 20,
                "description": "Nothing in production yet.",
            },
            {
                "option_id": "B",
                "label": "1–3 AI models or applications in production in a single business unit",
                "score": 45,
                "description": "Limited production footprint; single business unit.",
            },
            {
                "option_id": "C",
                "label": "4–10 AI models or applications in production across 2+ business units",
                "score": 70,
                "description": "Meaningful production portfolio across multiple units.",
            },
            {
                "option_id": "D",
                "label": "10+ AI models or applications in production across the enterprise",
                "score": 90,
                "description": "Scaled enterprise AI programme in production.",
            },
        ],
        "scale_anchors": None,
        "max_chars": None,
        "persona_tags": None,
        "industry_tags": None,
        "skip_logic": None,
        # Show only if Q3.1 != A
        "branching_logic": {"show_if": {"Q3.1": {"not": "A"}}},
        "helper_text": (
            "Count distinct deployed models or AI-powered applications, not experiments."
        ),
        "persona_variant_text": None,
    },

    # Q3.3 — AI programme outcomes (skip if Q3.1 = A)
    # single_select | weight 0.25 | scores 25/45/70/90
    {
        "question_id": "Q3.3",
        "dimension_id": "ai_investment_maturity",
        "question_text": (
            "How well have your AI investments delivered measurable business outcomes?"
        ),
        "question_type": "single_select",
        "weight": 0.25,
        "options": [
            {
                "option_id": "A",
                "label": "Limited — most AI projects have not reached production or delivered clear value",
                "score": 25,
                "description": "Projects not completing or not generating clear business value.",
            },
            {
                "option_id": "B",
                "label": "Mixed — some successes but also notable failures or stalled projects",
                "score": 45,
                "description": "Inconsistent track record; learning from failures.",
            },
            {
                "option_id": "C",
                "label": "Positive — most projects deliver value but ROI measurement is informal",
                "score": 70,
                "description": "Good success rate; value delivered but not rigorously measured.",
            },
            {
                "option_id": "D",
                "label": "Strong — AI investments are tracked against KPIs and consistently deliver ROI",
                "score": 90,
                "description": "Disciplined measurement; consistent, documented ROI.",
            },
        ],
        "scale_anchors": None,
        "max_chars": None,
        "persona_tags": None,
        "industry_tags": None,
        "skip_logic": None,
        "branching_logic": {"show_if": {"Q3.1": {"not": "A"}}},
        "helper_text": (
            "Consider both financial outcomes (cost savings, revenue) and operational outcomes."
        ),
        "persona_variant_text": None,
    },

    # Q3.4 — AI investment trajectory
    # single_select | weight 0.15 | scores 30/50/70/80
    {
        "question_id": "Q3.4",
        "dimension_id": "ai_investment_maturity",
        "question_text": (
            "How is your AI investment level expected to change over the next 12–18 months?"
        ),
        "question_type": "single_select",
        "weight": 0.15,
        "options": [
            {
                "option_id": "A",
                "label": "Decreasing or paused — budgets are being cut or frozen",
                "score": 30,
                "description": "Investment reducing or halted.",
            },
            {
                "option_id": "B",
                "label": "Flat — maintaining current spending levels",
                "score": 50,
                "description": "Steady-state investment.",
            },
            {
                "option_id": "C",
                "label": "Increasing moderately (10–30% growth)",
                "score": 70,
                "description": "Moderate growth in AI budgets.",
            },
            {
                "option_id": "D",
                "label": "Increasing significantly (>30% growth) or a major new programme is launching",
                "score": 80,
                "description": "Significant step-up in investment or a major new initiative.",
            },
        ],
        "scale_anchors": None,
        "max_chars": None,
        "persona_tags": None,
        "industry_tags": None,
        "skip_logic": None,
        "branching_logic": None,
        "helper_text": "Include technology, talent, and external services spend.",
        "persona_variant_text": None,
    },

    # =========================================================================
    # DIMENSION 4: ORGANISATIONAL CHANGE READINESS  (weight 0.15, Q4.1–Q4.3)
    # =========================================================================

    # Q4.1 — Change management capacity
    # single_select | weight 0.35 | scores 25/50/75/90
    {
        "question_id": "Q4.1",
        "dimension_id": "org_change_readiness",
        "question_text": (
            "How would you rate your organisation's track record and capacity "
            "for large-scale change management programmes?"
        ),
        "question_type": "single_select",
        "weight": 0.35,
        "options": [
            {
                "option_id": "A",
                "label": "Weak — change programmes regularly stall; low organisational change appetite",
                "score": 25,
                "description": "Poor track record; change fatigue or resistance is common.",
            },
            {
                "option_id": "B",
                "label": "Developing — some change management capability but inconsistently applied",
                "score": 50,
                "description": "Capability exists but application is uneven.",
            },
            {
                "option_id": "C",
                "label": "Capable — structured change management exists and usually succeeds",
                "score": 75,
                "description": "Established methodology and reasonable success rate.",
            },
            {
                "option_id": "D",
                "label": "Strong — proven track record of delivering complex transformation programmes",
                "score": 90,
                "description": "Demonstrated excellence in complex, multi-year transformation.",
            },
        ],
        "scale_anchors": None,
        "max_chars": None,
        "persona_tags": None,
        "industry_tags": None,
        "skip_logic": None,
        "branching_logic": None,
        "helper_text": (
            "Think about recent ERP implementations, digital transformation programmes, "
            "or restructuring."
        ),
        "persona_variant_text": None,
    },

    # Q4.2 — Leadership alignment on AI
    # single_select | weight 0.40 | scores 30/55/75/90
    {
        "question_id": "Q4.2",
        "dimension_id": "org_change_readiness",
        "question_text": (
            "How aligned is your senior leadership team on the strategic priority of AI?"
        ),
        "question_type": "single_select",
        "weight": 0.40,
        "options": [
            {
                "option_id": "A",
                "label": "Not aligned — AI is not a shared strategic priority; no executive sponsorship",
                "score": 30,
                "description": "No executive sponsor; AI not on the leadership agenda.",
            },
            {
                "option_id": "B",
                "label": "Partially aligned — some leaders champion AI but others are sceptical or disengaged",
                "score": 55,
                "description": "Mixed signals from leadership; limited cross-functional commitment.",
            },
            {
                "option_id": "C",
                "label": "Mostly aligned — leadership broadly supports AI but priorities still being defined",
                "score": 75,
                "description": "Broad support; strategic priorities being finalised.",
            },
            {
                "option_id": "D",
                "label": "Fully aligned — AI is a board-level priority with cross-functional executive commitment",
                "score": 90,
                "description": "Board-level mandate; cross-functional executive ownership.",
            },
        ],
        "scale_anchors": None,
        "max_chars": None,
        "persona_tags": None,
        "industry_tags": None,
        "skip_logic": None,
        "branching_logic": None,
        "helper_text": "Alignment means more than agreement in principle — it includes budget commitment.",
        "persona_variant_text": {
            "P3": (
                "How aligned is your C-suite and board on AI as a core driver of "
                "financial performance and competitive differentiation?"
            ),
        },
    },

    # Q4.3 — Workforce posture toward AI
    # single_select | weight 0.25 | scores 30/55/75/90
    {
        "question_id": "Q4.3",
        "dimension_id": "org_change_readiness",
        "question_text": (
            "How would you characterise your workforce's general attitude toward AI adoption?"
        ),
        "question_type": "single_select",
        "weight": 0.25,
        "options": [
            {
                "option_id": "A",
                "label": "Resistant — significant anxiety or active pushback from employees",
                "score": 30,
                "description": "Broad workforce resistance; AI seen as a threat to jobs.",
            },
            {
                "option_id": "B",
                "label": "Cautious — employees are willing to try AI but expect reassurance and training",
                "score": 55,
                "description": "Open-minded but needing support; change management investment required.",
            },
            {
                "option_id": "C",
                "label": "Receptive — most employees see AI as a useful tool and are willing adopters",
                "score": 75,
                "description": "Positive disposition; employees seeking AI augmentation.",
            },
            {
                "option_id": "D",
                "label": "Enthusiastic — employees are actively experimenting with AI tools",
                "score": 90,
                "description": "Bottom-up enthusiasm; grassroots AI experimentation common.",
            },
        ],
        "scale_anchors": None,
        "max_chars": None,
        "persona_tags": None,
        "industry_tags": None,
        "skip_logic": None,
        "branching_logic": None,
        "helper_text": (
            "Base this on what you observe, not what you hope. Consider frontline workers, "
            "not just knowledge workers."
        ),
        "persona_variant_text": None,
    },

    # =========================================================================
    # DIMENSION 5: VALUE-POCKET CLARITY  (weight 0.17, questions Q5.1–Q5.3)
    # =========================================================================

    # Q5.1 — Identified processes for AI
    # single_select | weight 0.40 | scores 25/50/75/90
    {
        "question_id": "Q5.1",
        "dimension_id": "value_pocket_clarity",
        "question_text": (
            "Has your organisation identified specific business processes or "
            "workflows where AI could deliver meaningful value?"
        ),
        "question_type": "single_select",
        "weight": 0.40,
        "options": [
            {
                "option_id": "A",
                "label": "No — we have not yet conducted a structured value identification exercise",
                "score": 25,
                "description": "No formal exercise; AI use cases are not mapped.",
            },
            {
                "option_id": "B",
                "label": "Informally — teams have ideas but there is no structured inventory",
                "score": 50,
                "description": "Individual ideas exist but not aggregated or prioritised.",
            },
            {
                "option_id": "C",
                "label": "Yes — we have an identified list of priority use cases with rough sizing",
                "score": 75,
                "description": "Structured use case inventory with rough value estimates.",
            },
            {
                "option_id": "D",
                "label": "Yes — we have a validated, prioritised roadmap with business case approval",
                "score": 90,
                "description": "Fully validated roadmap; business cases approved and funded.",
            },
        ],
        "scale_anchors": None,
        "max_chars": None,
        "persona_tags": None,
        "industry_tags": None,
        "skip_logic": None,
        "branching_logic": None,
        "helper_text": (
            "Think about whether there is a shared, documented list that leadership "
            "has reviewed."
        ),
        "persona_variant_text": None,
    },

    # Q5.2 — Success metrics defined (CFO framing for P3)
    # single_select | weight 0.30 | scores 30/50/75/90
    {
        "question_id": "Q5.2",
        "dimension_id": "value_pocket_clarity",
        "question_text": (
            "For your priority AI use cases, have you defined measurable success metrics?"
        ),
        "question_type": "single_select",
        "weight": 0.30,
        "options": [
            {
                "option_id": "A",
                "label": "No metrics defined — success is loosely described",
                "score": 30,
                "description": "No quantitative targets set.",
            },
            {
                "option_id": "B",
                "label": "High-level metrics exist but are not tied to financial outcomes",
                "score": 50,
                "description": "Operational metrics defined; financial linkage not established.",
            },
            {
                "option_id": "C",
                "label": "Metrics defined for most use cases with a mix of operational and financial KPIs",
                "score": 75,
                "description": "Good coverage; mix of operational and financial measures.",
            },
            {
                "option_id": "D",
                "label": "Rigorous metrics — business cases with NPV, payback period, and KPI dashboards",
                "score": 90,
                "description": "Full financial rigour; NPV, payback, live dashboards.",
            },
        ],
        "scale_anchors": None,
        "max_chars": None,
        "persona_tags": None,
        "industry_tags": None,
        "skip_logic": None,
        "branching_logic": None,
        "helper_text": "Metrics should be measurable before and after AI deployment.",
        "persona_variant_text": {
            "P3": (
                "For your priority AI investments, have you defined financial success "
                "metrics such as NPV, IRR, cost-per-unit reduction, or revenue impact?"
            ),
        },
    },

    # Q5.3 — Process reinvention framing
    # single_select | weight 0.30 | scores 35/55/80/95
    {
        "question_id": "Q5.3",
        "dimension_id": "value_pocket_clarity",
        "question_text": (
            "When your organisation thinks about AI, which framing best describes "
            "the typical conversation?"
        ),
        "question_type": "single_select",
        "weight": 0.30,
        "options": [
            {
                "option_id": "A",
                "label": "Automation of tasks — replacing manual steps with AI to reduce cost",
                "score": 35,
                "description": "Task-level automation mindset; primarily cost-reduction focused.",
            },
            {
                "option_id": "B",
                "label": "Productivity augmentation — helping workers do their jobs faster and better",
                "score": 55,
                "description": "Human-in-the-loop augmentation; productivity focus.",
            },
            {
                "option_id": "C",
                "label": "Process transformation — redesigning end-to-end processes around AI capabilities",
                "score": 80,
                "description": "Process-level redesign; AI at the core of new operating models.",
            },
            {
                "option_id": "D",
                "label": "Business model reinvention — AI enables new products, services, or revenue streams",
                "score": 95,
                "description": "Strategic reinvention; AI creates new business value not previously possible.",
            },
        ],
        "scale_anchors": None,
        "max_chars": None,
        "persona_tags": None,
        "industry_tags": None,
        "skip_logic": None,
        "branching_logic": None,
        "helper_text": (
            "This reflects your organisation's ambition level, not its current maturity."
        ),
        "persona_variant_text": None,
    },

    # =========================================================================
    # DIMENSION 6: REGULATORY COMPLEXITY  (weight 0.10, questions Q6.1–Q6.3)
    # =========================================================================

    # Q6.1 — Regulatory frameworks (multi_select, informational / complexity scoring)
    # 7 options | weight 0.50
    # branching: show Q6.2 if A (EU AI Act), C (FCA/PRA), or E (HIPAA) selected
    {
        "question_id": "Q6.1",
        "dimension_id": "regulatory_complexity",
        "question_text": (
            "Which of the following regulatory frameworks apply to your organisation's "
            "AI or data activities? Select all that apply."
        ),
        "question_type": "multi_select",
        "weight": 0.50,
        "options": [
            {
                "option_id": "A",
                "label": "EU AI Act",
                "score": None,
                "description": "European Union Artificial Intelligence Act (risk-based framework).",
            },
            {
                "option_id": "B",
                "label": "GDPR / EU data protection",
                "score": None,
                "description": "General Data Protection Regulation (EU/EEA).",
            },
            {
                "option_id": "C",
                "label": "FCA / PRA guidance (UK financial services AI)",
                "score": None,
                "description": "UK Financial Conduct Authority and Prudential Regulation Authority.",
            },
            {
                "option_id": "D",
                "label": "SR 11-7 / OCC model risk management (US banking)",
                "score": None,
                "description": "US Federal Reserve / OCC model risk management guidance.",
            },
            {
                "option_id": "E",
                "label": "HIPAA / HITECH (US healthcare)",
                "score": None,
                "description": "US Health Insurance Portability and Accountability Act.",
            },
            {
                "option_id": "F",
                "label": "SOC 2 / ISO 27001 (security and privacy)",
                "score": None,
                "description": "Trust service criteria / international information security standard.",
            },
            {
                "option_id": "G",
                "label": "None of the above / not yet assessed",
                "score": None,
                "description": "No specific AI/data regulatory frameworks identified.",
            },
        ],
        "scale_anchors": None,
        "max_chars": None,
        "persona_tags": None,
        "industry_tags": None,
        "skip_logic": None,
        # Show Q6.2 only when EU AI Act (A), FCA/PRA (C), or HIPAA (E) selected
        "branching_logic": {
            "show_Q6.2_if_selected": ["A", "C", "E"],
        },
        "helper_text": (
            "Select all frameworks your legal or compliance team has confirmed apply. "
            "If unsure, select 'not yet assessed'."
        ),
        "persona_variant_text": None,
    },

    # Q6.2 — Data sovereignty constraints
    # single_select | weight 0.30 | informational scoring
    # Shown only if Q6.1 includes EU AI Act (A), FCA/PRA (C), or HIPAA (E)
    {
        "question_id": "Q6.2",
        "dimension_id": "regulatory_complexity",
        "question_text": (
            "Given the regulatory frameworks you operate under, how significant "
            "are data sovereignty or data residency constraints on your AI programme?"
        ),
        "question_type": "single_select",
        "weight": 0.30,
        "options": [
            {
                "option_id": "A",
                "label": "Not significant — our data can flow freely within our operating regions",
                "score": None,
                "description": "No material data residency constraints.",
            },
            {
                "option_id": "B",
                "label": "Moderate — some data must stay in specific jurisdictions but workarounds exist",
                "score": None,
                "description": "Constraints exist but are manageable with current architecture.",
            },
            {
                "option_id": "C",
                "label": "Significant — data localisation requirements constrain our AI model options",
                "score": None,
                "description": "Material constraints limiting cloud provider or model choices.",
            },
            {
                "option_id": "D",
                "label": "Very significant — air-gapped or on-premises requirements limit cloud AI use",
                "score": None,
                "description": "Severe constraints; on-premises or air-gapped requirements.",
            },
        ],
        "scale_anchors": None,
        "max_chars": None,
        "persona_tags": None,
        "industry_tags": None,
        "skip_logic": None,
        "branching_logic": {
            "show_if_Q6.1_includes": ["A", "C", "E"],
        },
        "helper_text": (
            "Consider where training data, inference infrastructure, and outputs must reside."
        ),
        "persona_variant_text": None,
    },

    # Q6.3 — Cross-border data implications (open_short)
    # open_short | weight 0.20 | max 500 chars
    {
        "question_id": "Q6.3",
        "dimension_id": "regulatory_complexity",
        "question_text": (
            "Are there any cross-border data transfer restrictions or international "
            "compliance obligations that you believe could constrain your AI strategy? "
            "Please describe briefly."
        ),
        "question_type": "open_short",
        "weight": 0.20,
        "options": None,
        "scale_anchors": None,
        "max_chars": 500,
        "persona_tags": None,
        "industry_tags": None,
        "skip_logic": None,
        "branching_logic": None,
        "helper_text": (
            "If none, you may write 'None'. Examples include SCCs under GDPR, "
            "Schrems II concerns, or China PIPL requirements."
        ),
        "persona_variant_text": None,
    },
]


# ---------------------------------------------------------------------------
# Accessor functions
# ---------------------------------------------------------------------------


def get_question_pool() -> List[Dict[str, Any]]:
    """Return the complete 20-question pool as raw dicts."""
    return list(QUESTION_POOL)


def get_question_by_id(qid: str) -> Optional[Dict[str, Any]]:
    """Return a single question dict by question_id, or None if not found."""
    for q in QUESTION_POOL:
        if q["question_id"] == qid:
            return q
    return None


def get_questions_by_dimension(dimension_id: str) -> List[Dict[str, Any]]:
    """Return all questions for a given dimension_id."""
    return [q for q in QUESTION_POOL if q["dimension_id"] == dimension_id]


def get_questions_for_persona(persona: str) -> List[Dict[str, Any]]:
    """Return questions applicable to the given persona (includes universal questions)."""
    return [
        q for q in QUESTION_POOL
        if q.get("persona_tags") is None or persona in (q.get("persona_tags") or [])
    ]
