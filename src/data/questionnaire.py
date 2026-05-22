"""
Default question pool for the DXC AI Readiness Diagnostic V0.

Each entry conforms to the QuestionPoolEntry schema from src.models.schemas.
The pool covers all six diagnostic dimensions across three persona types.
"""

from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Question pool — list of raw dicts (schema-validated by A3 at runtime)
# ---------------------------------------------------------------------------

QUESTION_POOL: List[Dict[str, Any]] = [
    # -----------------------------------------------------------------------
    # D1: Data Foundation
    # -----------------------------------------------------------------------
    {
        "question_id": "Q1.1",
        "dimension_id": "data_foundation",
        "question_text": "How would you describe your organisation's current state of enterprise data management?",
        "question_type": "single_select",
        "weight": 0.20,
        "options": [
            {"option_id": "A", "label": "Siloed — data lives in departmental systems with no central catalogue", "score": 1},
            {"option_id": "B", "label": "Partially integrated — some shared data platforms exist but coverage is incomplete", "score": 2},
            {"option_id": "C", "label": "Managed — enterprise data platform with defined ownership and governance", "score": 3},
            {"option_id": "D", "label": "Advanced — real-time data mesh or lakehouse with broad organisational adoption", "score": 4},
        ],
        "persona_tags": None,
        "industry_tags": None,
        "helper_text": "Consider the state across all major business functions, not just IT.",
        "persona_variant_text": {
            "P1": "How would you describe your organisation's current ability to act on enterprise-wide data?",
            "P3": "How would you describe your organisation's current data infrastructure maturity, from a cost and investment standpoint?",
        },
        "skip_logic": None,
    },
    {
        "question_id": "Q1.2",
        "dimension_id": "data_foundation",
        "question_text": "What percentage of your business-critical datasets are labelled, versioned, and accessible for AI model training?",
        "question_type": "single_select",
        "weight": 0.18,
        "options": [
            {"option_id": "A", "label": "Less than 10%", "score": 1},
            {"option_id": "B", "label": "10–40%", "score": 2},
            {"option_id": "C", "label": "40–70%", "score": 3},
            {"option_id": "D", "label": "More than 70%", "score": 4},
        ],
        "persona_tags": ["P2"],
        "industry_tags": None,
        "helper_text": None,
        "skip_logic": None,
    },
    {
        "question_id": "Q1.3",
        "dimension_id": "data_foundation",
        "question_text": "Does your organisation have a documented data lineage and provenance capability?",
        "question_type": "single_select",
        "weight": 0.15,
        "options": [
            {"option_id": "A", "label": "No — data origins and transformations are not tracked", "score": 1},
            {"option_id": "B", "label": "Partial — some critical pipelines have lineage documentation", "score": 2},
            {"option_id": "C", "label": "Yes — end-to-end lineage tooling is deployed for key domains", "score": 3},
            {"option_id": "D", "label": "Yes, automated — lineage is captured automatically across all domains", "score": 4},
        ],
        "persona_tags": None,
        "industry_tags": None,
        "helper_text": "Data lineage enables traceability required for AI explainability and compliance.",
        "skip_logic": None,
    },
    {
        "question_id": "Q1.4",
        "dimension_id": "data_foundation",
        "question_text": "How does your organisation currently handle data quality measurement and remediation?",
        "question_type": "single_select",
        "weight": 0.15,
        "options": [
            {"option_id": "A", "label": "Ad hoc — issues are discovered reactively by end users", "score": 1},
            {"option_id": "B", "label": "Defined — some dimensions are measured but not systematically", "score": 2},
            {"option_id": "C", "label": "Managed — automated profiling with SLAs and escalation paths", "score": 3},
            {"option_id": "D", "label": "Optimised — continuous data quality monitoring with AI-assisted remediation", "score": 4},
        ],
        "persona_tags": None,
        "industry_tags": None,
        "helper_text": None,
        "skip_logic": None,
    },
    # -----------------------------------------------------------------------
    # D2: Governance Posture
    # -----------------------------------------------------------------------
    {
        "question_id": "Q2.1",
        "dimension_id": "governance_posture",
        "question_text": "Does your organisation have a formal AI governance framework or policy in place?",
        "question_type": "single_select",
        "weight": 0.20,
        "options": [
            {"option_id": "A", "label": "No formal framework — decisions are made case by case", "score": 1},
            {"option_id": "B", "label": "Draft / in progress — a framework is being developed", "score": 2},
            {"option_id": "C", "label": "Adopted — published policy, but limited enforcement mechanisms", "score": 3},
            {"option_id": "D", "label": "Embedded — policy with automated controls, audit trails, and regular review", "score": 4},
        ],
        "persona_tags": None,
        "industry_tags": None,
        "helper_text": "Consider policies covering bias, explainability, model monitoring, and human oversight.",
        "persona_variant_text": {
            "P1": "Has your board or executive team formally approved an AI governance framework?",
        },
        "skip_logic": None,
    },
    {
        "question_id": "Q2.2",
        "dimension_id": "governance_posture",
        "question_text": "How does your organisation ensure compliance with applicable data privacy regulations (e.g., GDPR, CCPA, PDPA)?",
        "question_type": "single_select",
        "weight": 0.18,
        "options": [
            {"option_id": "A", "label": "Primarily manual review by legal/compliance team", "score": 1},
            {"option_id": "B", "label": "Policy-driven with some automated controls", "score": 2},
            {"option_id": "C", "label": "Technology-enabled — privacy engineering integrated into data pipelines", "score": 3},
            {"option_id": "D", "label": "Privacy-by-design — embedded at the architecture and product level", "score": 4},
        ],
        "persona_tags": None,
        "industry_tags": None,
        "helper_text": None,
        "skip_logic": None,
    },
    {
        "question_id": "Q2.3",
        "dimension_id": "governance_posture",
        "question_text": "Does your organisation have a named Chief AI Officer (CAIO), Chief Data & AI Officer, or equivalent executive responsible for AI governance?",
        "question_type": "single_select",
        "weight": 0.15,
        "options": [
            {"option_id": "A", "label": "No designated role", "score": 1},
            {"option_id": "B", "label": "Responsibility is distributed across CIO/CTO/Legal", "score": 2},
            {"option_id": "C", "label": "Named individual with AI governance as part of their remit", "score": 3},
            {"option_id": "D", "label": "Dedicated CAIO or Chief Data & AI Officer with board-level visibility", "score": 4},
        ],
        "persona_tags": ["P1", "P2"],
        "industry_tags": None,
        "helper_text": None,
        "skip_logic": None,
    },
    # -----------------------------------------------------------------------
    # D3: AI Investment Maturity
    # -----------------------------------------------------------------------
    {
        "question_id": "Q3.1",
        "dimension_id": "ai_investment_maturity",
        "question_text": "How would you characterise your organisation's current level of AI deployment?",
        "question_type": "single_select",
        "weight": 0.22,
        "options": [
            {"option_id": "A", "label": "Exploration — we are running proofs-of-concept or internal pilots only", "score": 1},
            {"option_id": "B", "label": "Developing — we have one or two AI systems in production", "score": 2},
            {"option_id": "C", "label": "Scaling — multiple AI systems in production across several business units", "score": 3},
            {"option_id": "D", "label": "Embedded — AI is a core component of our operating model and value chain", "score": 4},
        ],
        "persona_tags": None,
        "industry_tags": None,
        "helper_text": None,
        "persona_variant_text": {
            "P3": "How would you characterise your organisation's current level of AI deployment relative to its committed technology budget?",
        },
        "skip_logic": None,
    },
    {
        "question_id": "Q3.2",
        "dimension_id": "ai_investment_maturity",
        "question_text": "What is your organisation's planned AI/GenAI investment level over the next 12 months relative to current technology spend?",
        "question_type": "single_select",
        "weight": 0.18,
        "options": [
            {"option_id": "A", "label": "Less than 2% of tech budget", "score": 1},
            {"option_id": "B", "label": "2–5% of tech budget", "score": 2},
            {"option_id": "C", "label": "5–15% of tech budget", "score": 3},
            {"option_id": "D", "label": "Greater than 15% of tech budget", "score": 4},
        ],
        "persona_tags": ["P1", "P3"],
        "industry_tags": None,
        "helper_text": "Include both CapEx (infrastructure, platform licences) and OpEx (talent, training, third-party models).",
        "skip_logic": None,
    },
    {
        "question_id": "Q3.3",
        "dimension_id": "ai_investment_maturity",
        "question_text": "Does your organisation have a dedicated MLOps or AI engineering team responsible for production model lifecycle management?",
        "question_type": "single_select",
        "weight": 0.15,
        "options": [
            {"option_id": "A", "label": "No — data scientists manage models informally", "score": 1},
            {"option_id": "B", "label": "Emerging — a small team is being assembled", "score": 2},
            {"option_id": "C", "label": "Established — dedicated MLOps team with defined processes", "score": 3},
            {"option_id": "D", "label": "Mature — platform engineering team with automated CI/CD for models", "score": 4},
        ],
        "persona_tags": ["P2"],
        "industry_tags": None,
        "helper_text": None,
        "skip_logic": None,
    },
    # -----------------------------------------------------------------------
    # D4: Org Change Readiness
    # -----------------------------------------------------------------------
    {
        "question_id": "Q4.1",
        "dimension_id": "org_change_readiness",
        "question_text": "How would you rate your organisation's change management capability for large-scale technology transformations?",
        "question_type": "scale_1_5",
        "weight": 0.20,
        "scale_anchors": [
            {"value": 1, "label": "Very weak — we struggle to sustain change adoption", "score": 1},
            {"value": 3, "label": "Moderate — we manage change with significant effort", "score": 3},
            {"value": 5, "label": "Very strong — structured change capability with measurable adoption outcomes", "score": 5},
        ],
        "persona_tags": None,
        "industry_tags": None,
        "helper_text": None,
        "persona_variant_text": {
            "P1": "How confident are you in your organisation's ability to adopt AI-driven working practices at scale?",
        },
        "skip_logic": None,
    },
    {
        "question_id": "Q4.2",
        "dimension_id": "org_change_readiness",
        "question_text": "What is the current state of AI literacy across your workforce (beyond the IT/data function)?",
        "question_type": "single_select",
        "weight": 0.18,
        "options": [
            {"option_id": "A", "label": "Very low — most employees have no exposure to AI concepts or tools", "score": 1},
            {"option_id": "B", "label": "Low — awareness exists in pockets but no structured programme", "score": 2},
            {"option_id": "C", "label": "Moderate — company-wide AI literacy programme launched", "score": 3},
            {"option_id": "D", "label": "High — role-specific AI upskilling is embedded in talent strategy", "score": 4},
        ],
        "persona_tags": None,
        "industry_tags": None,
        "helper_text": None,
        "skip_logic": None,
    },
    {
        "question_id": "Q4.3",
        "dimension_id": "org_change_readiness",
        "question_text": "Does your executive team actively champion AI adoption, and is this visible to the broader workforce?",
        "question_type": "single_select",
        "weight": 0.15,
        "options": [
            {"option_id": "A", "label": "No visible executive sponsorship", "score": 1},
            {"option_id": "B", "label": "Informal — individual executives mention AI but no coordinated message", "score": 2},
            {"option_id": "C", "label": "Active — executive sponsor with regular internal communications", "score": 3},
            {"option_id": "D", "label": "Embedded — AI is a stated strategic priority with board-level accountability", "score": 4},
        ],
        "persona_tags": ["P1"],
        "industry_tags": None,
        "helper_text": None,
        "skip_logic": None,
    },
    # -----------------------------------------------------------------------
    # D5: Value Pocket Clarity
    # -----------------------------------------------------------------------
    {
        "question_id": "Q5.1",
        "dimension_id": "value_pocket_clarity",
        "question_text": "Has your organisation identified and prioritised the top 3–5 business processes where AI could deliver measurable value?",
        "question_type": "single_select",
        "weight": 0.22,
        "options": [
            {"option_id": "A", "label": "No — we have not yet mapped AI to specific business outcomes", "score": 1},
            {"option_id": "B", "label": "Partially — some opportunities identified but not formally prioritised", "score": 2},
            {"option_id": "C", "label": "Yes — a prioritised AI opportunity map exists", "score": 3},
            {"option_id": "D", "label": "Yes, with business cases — each priority has a quantified ROI estimate", "score": 4},
        ],
        "persona_tags": None,
        "industry_tags": None,
        "helper_text": "Consider both revenue-generating and cost-reduction opportunities.",
        "persona_variant_text": {
            "P1": "Can you name the top three areas in your business where AI investment would create the greatest competitive advantage?",
            "P3": "Has your organisation produced business cases with quantified ROI for your top AI investment priorities?",
        },
        "skip_logic": None,
    },
    {
        "question_id": "Q5.2",
        "dimension_id": "value_pocket_clarity",
        "question_text": "How does your organisation typically measure the success of a technology investment?",
        "question_type": "multi_select",
        "weight": 0.15,
        "options": [
            {"option_id": "A", "label": "Cost reduction / efficiency metrics", "score": 1},
            {"option_id": "B", "label": "Revenue growth or new revenue streams", "score": 1},
            {"option_id": "C", "label": "Customer satisfaction or NPS improvement", "score": 1},
            {"option_id": "D", "label": "Employee productivity or engagement", "score": 1},
            {"option_id": "E", "label": "Risk reduction or compliance improvement", "score": 1},
            {"option_id": "F", "label": "Strategic positioning / market share", "score": 1},
        ],
        "persona_tags": ["P1", "P3"],
        "industry_tags": None,
        "helper_text": "Select all that apply.",
        "skip_logic": None,
    },
    {
        "question_id": "Q5.3",
        "dimension_id": "value_pocket_clarity",
        "question_text": "Describe your organisation's most significant unrealised process inefficiency that you believe AI could address.",
        "question_type": "open_short",
        "weight": 0.12,
        "max_chars": 500,
        "persona_tags": None,
        "industry_tags": None,
        "helper_text": "Be as specific as possible — for example, 'manual invoice matching across 12 ERP instances'.",
        "skip_logic": None,
    },
    # -----------------------------------------------------------------------
    # D6: Regulatory Complexity
    # -----------------------------------------------------------------------
    {
        "question_id": "Q6.1",
        "dimension_id": "regulatory_complexity",
        "question_text": "Which regulatory frameworks are directly applicable to your organisation's planned AI use cases?",
        "question_type": "multi_select",
        "weight": 0.20,
        "options": [
            {"option_id": "A", "label": "EU AI Act", "score": None},
            {"option_id": "B", "label": "GDPR / CCPA / other data privacy regulation", "score": None},
            {"option_id": "C", "label": "HIPAA / FDA (healthcare)", "score": None},
            {"option_id": "D", "label": "Financial services regulation (Basel, MiFID II, DORA, SR 11-7)", "score": None},
            {"option_id": "E", "label": "US Executive Order on AI / NIST AI RMF", "score": None},
            {"option_id": "F", "label": "Sector-specific (aerospace, defence, energy, telco)", "score": None},
            {"option_id": "G", "label": "None currently identified", "score": None},
        ],
        "persona_tags": None,
        "industry_tags": None,
        "helper_text": "Select all that apply. This information is used to calibrate risk and governance recommendations.",
        "skip_logic": {
            "G": {"skip_to": "Q6.3", "reason": "No regulatory frameworks identified"}
        },
    },
    {
        "question_id": "Q6.2",
        "dimension_id": "regulatory_complexity",
        "question_text": "How mature is your organisation's current compliance programme for AI-specific obligations?",
        "question_type": "single_select",
        "weight": 0.18,
        "options": [
            {"option_id": "A", "label": "Not started — we have not assessed AI-specific regulatory requirements", "score": 1},
            {"option_id": "B", "label": "Assessment in progress — we are mapping requirements", "score": 2},
            {"option_id": "C", "label": "Partial controls — some requirements addressed but gaps remain", "score": 3},
            {"option_id": "D", "label": "Compliant — controls in place, evidenced, and audited", "score": 4},
        ],
        "persona_tags": None,
        "industry_tags": None,
        "helper_text": None,
        "skip_logic": None,
    },
    {
        "question_id": "Q6.3",
        "dimension_id": "regulatory_complexity",
        "question_text": "Does your organisation operate across multiple jurisdictions with differing AI or data sovereignty requirements?",
        "question_type": "single_select",
        "weight": 0.12,
        "options": [
            {"option_id": "A", "label": "No — single jurisdiction", "score": 4},
            {"option_id": "B", "label": "Yes — 2–3 jurisdictions", "score": 3},
            {"option_id": "C", "label": "Yes — 4–10 jurisdictions", "score": 2},
            {"option_id": "D", "label": "Yes — more than 10 jurisdictions", "score": 1},
        ],
        "persona_tags": None,
        "industry_tags": None,
        "helper_text": "Higher cross-jurisdictional complexity reduces AI deployment velocity.",
        "skip_logic": None,
    },
]


def get_question_pool() -> List[Dict[str, Any]]:
    """Return the full question pool as a list of raw dicts."""
    return list(QUESTION_POOL)


def get_questions_by_dimension(dimension_id: str) -> List[Dict[str, Any]]:
    """Return questions filtered by dimension_id."""
    return [q for q in QUESTION_POOL if q["dimension_id"] == dimension_id]


def get_questions_by_persona(persona: str) -> List[Dict[str, Any]]:
    """Return questions applicable to the given persona (including universal questions)."""
    return [
        q for q in QUESTION_POOL
        if q.get("persona_tags") is None or persona in (q.get("persona_tags") or [])
    ]
