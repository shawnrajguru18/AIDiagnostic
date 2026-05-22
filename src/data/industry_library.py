"""Industry Process Library for DXC AI Readiness Diagnostic V0.

V0 coverage:
  - Tier 1 (universal): 5 entries applicable to all industries
  - Financial Services (FS):  6 Tier 2/3 entries
  - Healthcare & Life Sciences (HLS): 4 Tier 2/3 entries
  - Manufacturing (MFG): 4 Tier 2/3 entries

Other industries receive Tier 1 entries only (V0.5 gap flagged).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Tier 1 — Universal processes (apply to all industries)
# ---------------------------------------------------------------------------

TIER1_UNIVERSAL: List[Dict[str, Any]] = [

    # T1-001  AP / Invoice Processing
    {
        "process_id": "T1-001",
        "process_name": "Accounts Payable & Invoice Processing",
        "tier": 1,
        "industries_applicable": ["All"],
        "sub_processes": [
            {
                "sub_process_id": "T1-001-A",
                "sub_process_name": "Intelligent invoice capture & extraction",
                "value_pocket_sizing": "High — $0.8–3M/yr per 10 000 invoices/month",
                "reinvention_archetype": "Automation",
                "ai_pattern_description": (
                    "LLM-based document understanding reads invoices in any format, "
                    "extracts header and line-item fields, and pushes to ERP — "
                    "eliminating manual keying."
                ),
                "applicable_ai_patterns": [
                    "document_understanding",
                    "extraction",
                    "ocr",
                ],
            },
            {
                "sub_process_id": "T1-001-B",
                "sub_process_name": "PO matching, exception routing & approval",
                "value_pocket_sizing": "Medium — cycle-time and discount-capture value",
                "reinvention_archetype": "Augmentation",
                "ai_pattern_description": (
                    "Automated three-way match with rule-based exception handling "
                    "and intelligent approval routing based on amount, category, "
                    "and vendor risk."
                ),
                "applicable_ai_patterns": [
                    "classification",
                    "routing",
                    "anomaly_detection",
                ],
            },
            {
                "sub_process_id": "T1-001-C",
                "sub_process_name": "Supplier self-service & query resolution",
                "value_pocket_sizing": "Medium",
                "reinvention_archetype": "Augmentation",
                "ai_pattern_description": (
                    "RAG-based chatbot answers supplier payment status queries "
                    "and resolves discrepancies without AP analyst involvement."
                ),
                "applicable_ai_patterns": ["rag", "question_answering"],
            },
        ],
        "prerequisites": [
            "ERP system with AP module",
            "Digitised invoice intake (email, portal, or scan-to-digital)",
            "12+ months of invoice history",
        ],
        "typical_outcomes_when_done_well": [
            "70-85% reduction in manual data-entry FTE cost",
            "Invoice processing time: 5-8 days to under 4 hours",
            "Early-payment-discount capture improvement of 15-30%",
            "Error / duplicate payment rate reduction > 90%",
        ],
    },

    # T1-002  IT Incident Management
    {
        "process_id": "T1-002",
        "process_name": "IT Incident Management",
        "tier": 1,
        "industries_applicable": ["All"],
        "sub_processes": [
            {
                "sub_process_id": "T1-002-A",
                "sub_process_name": "Incident classification & intelligent routing",
                "value_pocket_sizing": "High — MTTA and misroute cost reduction",
                "reinvention_archetype": "Automation",
                "ai_pattern_description": (
                    "NLP classification model predicts correct assignment group, "
                    "priority, and category for incoming tickets; generative layer "
                    "drafts initial resolution suggestions from knowledge base."
                ),
                "applicable_ai_patterns": [
                    "classification",
                    "routing",
                    "nlp",
                ],
            },
            {
                "sub_process_id": "T1-002-B",
                "sub_process_name": "L1 auto-resolution & knowledge surfacing",
                "value_pocket_sizing": "High — L1 resolution cost avoidance",
                "reinvention_archetype": "Augmentation",
                "ai_pattern_description": (
                    "RAG over knowledge base surfaces resolution steps; "
                    "high-confidence routine incidents are auto-resolved with "
                    "user confirmation, bypassing human triage."
                ),
                "applicable_ai_patterns": ["rag", "semantic_search"],
            },
        ],
        "prerequisites": [
            "ITSM platform with API access (ServiceNow, Jira SM, BMC Helix)",
            "At least 10 000 historical resolved tickets",
            "Stable assignment-group taxonomy",
        ],
        "typical_outcomes_when_done_well": [
            "Mean-time-to-assign reduction of 60-80%",
            "Misroute rate reduction from 25-40% to under 5%",
            "L1 auto-resolution improvement of 15-25 percentage points",
        ],
    },

    # T1-003  Customer Support Ticketing
    {
        "process_id": "T1-003",
        "process_name": "Customer Support Ticketing & Contact Centre",
        "tier": 1,
        "industries_applicable": ["All"],
        "sub_processes": [
            {
                "sub_process_id": "T1-003-A",
                "sub_process_name": "Conversational AI deflection (tier-0)",
                "value_pocket_sizing": "High — 20-40% ticket deflection",
                "reinvention_archetype": "Automation",
                "ai_pattern_description": (
                    "RAG chatbot handles common customer inquiries end-to-end "
                    "via web, chat, or email without agent involvement."
                ),
                "applicable_ai_patterns": [
                    "rag",
                    "dialogue",
                    "classification",
                ],
            },
            {
                "sub_process_id": "T1-003-B",
                "sub_process_name": "Agent assist & next-best-action",
                "value_pocket_sizing": "High — AHT and CSAT value",
                "reinvention_archetype": "Augmentation",
                "ai_pattern_description": (
                    "Real-time agent-assist panel surfaces relevant knowledge "
                    "articles, past case resolutions, and recommended response "
                    "drafts during live customer interactions."
                ),
                "applicable_ai_patterns": [
                    "real_time_inference",
                    "recommendation",
                    "rag",
                ],
            },
        ],
        "prerequisites": [
            "CRM or contact centre platform with API (Salesforce, Zendesk, etc.)",
            "Structured knowledge base with 200+ articles",
            "12+ months of resolved case history",
        ],
        "typical_outcomes_when_done_well": [
            "Tier-0 deflection rate of 20-40%",
            "Average handle time reduction 25-35%",
            "CSAT improvement of 8-12 points",
        ],
    },

    # T1-004  Recruiting / HR
    {
        "process_id": "T1-004",
        "process_name": "Recruiting & Human Resources",
        "tier": 1,
        "industries_applicable": ["All"],
        "sub_processes": [
            {
                "sub_process_id": "T1-004-A",
                "sub_process_name": "AI-assisted CV screening & candidate ranking",
                "value_pocket_sizing": "Medium — recruiter capacity and time-to-hire",
                "reinvention_archetype": "Augmentation",
                "ai_pattern_description": (
                    "Extraction model parses CVs into structured profiles; "
                    "ranking model scores candidates against role requirements "
                    "with bias-auditing on score distributions."
                ),
                "applicable_ai_patterns": [
                    "extraction",
                    "classification",
                    "semantic_search",
                ],
            },
            {
                "sub_process_id": "T1-004-B",
                "sub_process_name": "HR policy & benefits self-service assistant",
                "value_pocket_sizing": "Medium — HR query deflection",
                "reinvention_archetype": "Augmentation",
                "ai_pattern_description": (
                    "RAG assistant over HR policy documents, benefits guides, "
                    "and onboarding materials gives employees instant, "
                    "cited answers to HR questions."
                ),
                "applicable_ai_patterns": ["rag", "question_answering"],
            },
        ],
        "prerequisites": [
            "ATS platform with API access",
            "HR policy documentation in digital form",
            "500+ historical hires with outcome data",
        ],
        "typical_outcomes_when_done_well": [
            "Time-to-shortlist reduction of 50-70%",
            "HR support ticket volume reduction of 25-35%",
            "New employee onboarding time reduction of 20-30%",
        ],
    },

    # T1-005  Knowledge Management
    {
        "process_id": "T1-005",
        "process_name": "Enterprise Knowledge Management",
        "tier": 1,
        "industries_applicable": ["All"],
        "sub_processes": [
            {
                "sub_process_id": "T1-005-A",
                "sub_process_name": "Enterprise AI knowledge assistant (RAG)",
                "value_pocket_sizing": "Medium — knowledge-worker productivity",
                "reinvention_archetype": "Augmentation",
                "ai_pattern_description": (
                    "RAG pipeline indexes internal documentation into a vector store; "
                    "employees get instant, cited answers via Teams, Slack, "
                    "or intranet chatbot."
                ),
                "applicable_ai_patterns": [
                    "rag",
                    "semantic_search",
                    "question_answering",
                ],
            },
            {
                "sub_process_id": "T1-005-B",
                "sub_process_name": "Automated knowledge capture & synthesis",
                "value_pocket_sizing": "Medium",
                "reinvention_archetype": "Augmentation",
                "ai_pattern_description": (
                    "LLM-based meeting transcription and summarisation "
                    "automatically captures decisions and action items, "
                    "keeping knowledge bases current."
                ),
                "applicable_ai_patterns": [
                    "speech_recognition",
                    "llm_generation",
                    "summarisation",
                ],
            },
        ],
        "prerequisites": [
            "Internal documentation in accessible digital repositories",
            "Collaboration platform with bot integration (Teams, Slack)",
            "IT security review on knowledge corpus",
        ],
        "typical_outcomes_when_done_well": [
            "Internal search time reduction: hours to minutes",
            "Tier-1 support ticket reduction of 25-40%",
            "New-hire time-to-productivity improvement of 2-3 weeks",
        ],
    },
]


# ---------------------------------------------------------------------------
# Financial Services (FS) — Tier 2 & 3 processes (6 entries)
# ---------------------------------------------------------------------------

FS_PROCESSES: List[Dict[str, Any]] = [

    # FS-001  Claims Adjudication
    {
        "process_id": "FS-001",
        "process_name": "Claims Adjudication & Straight-Through Processing",
        "tier": 2,
        "industries_applicable": ["Financial Services"],
        "sub_processes": [
            {
                "sub_process_id": "FS-001-A",
                "sub_process_name": "Automated claims triage & classification",
                "value_pocket_sizing": "High — 55-70% straight-through rate",
                "reinvention_archetype": "Automation",
                "ai_pattern_description": (
                    "ML classification model scores claims against policy rules, "
                    "historical payout patterns, and fraud signals; "
                    "routine claims are auto-adjudicated."
                ),
                "applicable_ai_patterns": [
                    "classification",
                    "gradient_boosting",
                    "anomaly_detection",
                ],
            },
            {
                "sub_process_id": "FS-001-B",
                "sub_process_name": "Fraud triage & SIU referral",
                "value_pocket_sizing": "High — fraud loss avoidance",
                "reinvention_archetype": "Augmentation",
                "ai_pattern_description": (
                    "Anomaly detection identifies suspicious claims patterns "
                    "and auto-generates SIU referral packages with evidence summaries."
                ),
                "applicable_ai_patterns": ["anomaly_detection", "document_generation"],
            },
        ],
        "prerequisites": [
            "Claims management system with API or data export",
            "3+ years of adjudicated claim history with outcomes",
            "Digital FNOL / claim-intake channel",
            "Actuarial / compliance sign-off on auto-adjudication thresholds",
        ],
        "typical_outcomes_when_done_well": [
            "Straight-through processing rate: 55-70% of routine claims",
            "Claims processing cost reduction: 30-45%",
            "Cycle time from 8-15 days to under 24 hours for auto-adjudicated claims",
        ],
    },

    # FS-002  KYC / AML
    {
        "process_id": "FS-002",
        "process_name": "KYC / AML & Financial Crime Compliance",
        "tier": 2,
        "industries_applicable": ["Financial Services"],
        "sub_processes": [
            {
                "sub_process_id": "FS-002-A",
                "sub_process_name": "Automated KYC document verification & entity matching",
                "value_pocket_sizing": "High — onboarding cost and time reduction",
                "reinvention_archetype": "Automation",
                "ai_pattern_description": (
                    "Computer vision + LLM extract and verify identity documents; "
                    "entity resolution matches customer to sanction lists and "
                    "adverse media in real time."
                ),
                "applicable_ai_patterns": [
                    "cv",
                    "document_understanding",
                    "entity_matching",
                ],
            },
            {
                "sub_process_id": "FS-002-B",
                "sub_process_name": "AML transaction monitoring & alert prioritisation",
                "value_pocket_sizing": "High — regulatory penalty avoidance and investigator productivity",
                "reinvention_archetype": "Augmentation",
                "ai_pattern_description": (
                    "ML model prioritises AML alerts by risk score, "
                    "cutting false-positive rate and letting investigators "
                    "focus on highest-risk cases."
                ),
                "applicable_ai_patterns": [
                    "classification",
                    "anomaly_detection",
                    "graph_nn",
                ],
            },
        ],
        "prerequisites": [
            "Core banking / CRM with customer profile data",
            "Sanction-list and adverse media data feeds",
            "Case management system for investigations",
        ],
        "typical_outcomes_when_done_well": [
            "False-positive alert reduction of 40-60%",
            "KYC onboarding time: days to minutes",
            "Investigator capacity freed by 30-50%",
        ],
    },

    # FS-003  Fraud Detection
    {
        "process_id": "FS-003",
        "process_name": "Real-Time Transaction Fraud Detection",
        "tier": 2,
        "industries_applicable": ["Financial Services"],
        "sub_processes": [
            {
                "sub_process_id": "FS-003-A",
                "sub_process_name": "Graph-neural-network fraud ring detection",
                "value_pocket_sizing": "High — typically 3-7x ROI on fraud losses avoided",
                "reinvention_archetype": "Reinvention",
                "ai_pattern_description": (
                    "Graph neural network models account, device, and merchant "
                    "relationships to expose rings and mule networks invisible to "
                    "rule-based systems."
                ),
                "applicable_ai_patterns": [
                    "graph_nn",
                    "anomaly_detection",
                    "streaming_ml",
                ],
            },
            {
                "sub_process_id": "FS-003-B",
                "sub_process_name": "Real-time transaction scoring (< 50 ms)",
                "value_pocket_sizing": "High",
                "reinvention_archetype": "Reinvention",
                "ai_pattern_description": (
                    "Streaming ML model scores every transaction within 50 ms; "
                    "feeds existing fraud operations queue with model confidence "
                    "to reduce analyst workload while catching more fraud."
                ),
                "applicable_ai_patterns": ["streaming_ml", "anomaly_detection"],
            },
        ],
        "prerequisites": [
            "Real-time transaction event stream",
            "24+ months of labelled fraud / non-fraud history",
            "MLOps infrastructure for < 100 ms model serving",
        ],
        "typical_outcomes_when_done_well": [
            "Fraud catch rate improvement of 20-35% vs. rule-based baseline",
            "False positive rate reduction of 40-60%",
            "Customer false-decline friction reduction of 30-50%",
        ],
    },

    # FS-004  AP Automation (FS variant — multi-entity / multi-currency)
    {
        "process_id": "FS-004",
        "process_name": "AP Automation — Financial Services Variant",
        "tier": 2,
        "industries_applicable": ["Financial Services"],
        "sub_processes": [
            {
                "sub_process_id": "FS-004-A",
                "sub_process_name": "Multi-entity, multi-currency invoice processing",
                "value_pocket_sizing": "High — cost reduction across many legal entities",
                "reinvention_archetype": "Automation",
                "ai_pattern_description": (
                    "Document understanding handles invoices in multiple currencies "
                    "and across complex multi-entity structures with inter-company "
                    "netting logic embedded."
                ),
                "applicable_ai_patterns": [
                    "document_understanding",
                    "extraction",
                    "classification",
                ],
            },
        ],
        "prerequisites": [
            "Multi-entity ERP or treasury management system",
            "Standardised chart of accounts across entities",
        ],
        "typical_outcomes_when_done_well": [
            "Invoice processing cost reduction of 60-75% across entity portfolio",
            "Inter-company reconciliation time reduction > 50%",
        ],
    },

    # FS-005  Regulatory Reporting
    {
        "process_id": "FS-005",
        "process_name": "Regulatory Reporting Automation",
        "tier": 2,
        "industries_applicable": ["Financial Services"],
        "sub_processes": [
            {
                "sub_process_id": "FS-005-A",
                "sub_process_name": "Automated report generation (Basel, DORA, IFRS9)",
                "value_pocket_sizing": "Medium — $500K-2M/yr cost avoidance",
                "reinvention_archetype": "Automation",
                "ai_pattern_description": (
                    "LLM generates narrative sections of regulatory reports from "
                    "data mart; validation agent cross-checks figures against "
                    "prior periods and known thresholds."
                ),
                "applicable_ai_patterns": [
                    "document_generation",
                    "validation",
                    "extraction",
                ],
            },
            {
                "sub_process_id": "FS-005-B",
                "sub_process_name": "Regulatory change monitoring & impact analysis",
                "value_pocket_sizing": "Medium — compliance team capacity and risk reduction",
                "reinvention_archetype": "Augmentation",
                "ai_pattern_description": (
                    "AI agent monitors regulatory feeds, classifies new rules "
                    "for relevance, and generates structured impact summaries "
                    "with pre-populated action owners."
                ),
                "applicable_ai_patterns": [
                    "classification",
                    "summarisation",
                    "extraction",
                ],
            },
        ],
        "prerequisites": [
            "Regulatory data mart with clean, reconciled source data",
            "Report templates in machine-readable format",
            "Compliance team engaged to review AI-generated drafts",
        ],
        "typical_outcomes_when_done_well": [
            "Report preparation cycle time reduction of 50-70%",
            "Manual error rate reduction > 80%",
            "Full audit trail with automated evidence linking",
        ],
    },

    # FS-006  Personalised Customer Engagement
    {
        "process_id": "FS-006",
        "process_name": "Personalised Customer Engagement & Next-Best-Offer",
        "tier": 3,
        "industries_applicable": ["Financial Services"],
        "sub_processes": [
            {
                "sub_process_id": "FS-006-A",
                "sub_process_name": "Real-time next-best-offer at digital touchpoints",
                "value_pocket_sizing": "High — cross-sell conversion lift",
                "reinvention_archetype": "Reinvention",
                "ai_pattern_description": (
                    "Personalisation engine scores product recommendations "
                    "at every customer touchpoint using contextual bandit "
                    "or multi-armed bandit approach with real-time event streaming."
                ),
                "applicable_ai_patterns": [
                    "recommendation",
                    "contextual_bandit",
                    "real_time_inference",
                ],
            },
        ],
        "prerequisites": [
            "Unified customer profile or CDP",
            "Digital channels with event streaming capability",
            "Product eligibility rules and offer catalogue",
        ],
        "typical_outcomes_when_done_well": [
            "Cross-sell conversion improvement of 15-30%",
            "Customer lifetime value improvement of 8-20%",
        ],
    },
]


# ---------------------------------------------------------------------------
# Healthcare & Life Sciences (HLS) — Tier 2 & 3 processes (4 entries)
# ---------------------------------------------------------------------------

HLS_PROCESSES: List[Dict[str, Any]] = [

    # HLS-001  Revenue Cycle Management
    {
        "process_id": "HLS-001",
        "process_name": "Revenue Cycle Management & Denial Prevention",
        "tier": 2,
        "industries_applicable": ["Healthcare & Life Sciences"],
        "sub_processes": [
            {
                "sub_process_id": "HLS-001-A",
                "sub_process_name": "Pre-submission claim scrubbing & denial prediction",
                "value_pocket_sizing": "High — 2-4 percentage point net collection rate improvement",
                "reinvention_archetype": "Automation",
                "ai_pattern_description": (
                    "Pre-submission model scores each claim for denial probability; "
                    "high-risk claims flagged for coder review with specific "
                    "fix recommendations before submission."
                ),
                "applicable_ai_patterns": [
                    "classification",
                    "gradient_boosting",
                    "nlp",
                ],
            },
            {
                "sub_process_id": "HLS-001-B",
                "sub_process_name": "Post-denial EOB analysis & appeals routing",
                "value_pocket_sizing": "Medium — denial recovery and write-off reduction",
                "reinvention_archetype": "Augmentation",
                "ai_pattern_description": (
                    "NLP model reads Explanation of Benefits documents, "
                    "categorises denial reason, and routes to appropriate "
                    "appeals workflow automatically."
                ),
                "applicable_ai_patterns": [
                    "nlp",
                    "classification",
                    "routing",
                ],
            },
        ],
        "prerequisites": [
            "Hospital billing system (Epic, Cerner, Meditech) with API",
            "18+ months of claims submission and denial data",
            "Payer contract data accessible",
        ],
        "typical_outcomes_when_done_well": [
            "Clean claims rate improvement of 8-15 percentage points",
            "Denial rate reduction of 20-35%",
            "Days in AR reduction of 5-12 days",
        ],
    },

    # HLS-002  Clinical Documentation
    {
        "process_id": "HLS-002",
        "process_name": "Clinical Documentation Intelligence (AI Scribe)",
        "tier": 2,
        "industries_applicable": ["Healthcare & Life Sciences"],
        "sub_processes": [
            {
                "sub_process_id": "HLS-002-A",
                "sub_process_name": "Ambient encounter transcription & SOAP note drafting",
                "value_pocket_sizing": "High — 1-2 hrs/physician/day recovered",
                "reinvention_archetype": "Augmentation",
                "ai_pattern_description": (
                    "Medical-grade ASR transcribes encounter audio; clinical LLM "
                    "extracts SOAP elements, maps ICD-10/CPT codes, and generates "
                    "EHR-template note draft for physician review and sign-off."
                ),
                "applicable_ai_patterns": [
                    "speech_recognition",
                    "llm_generation",
                    "medical_coding",
                ],
            },
            {
                "sub_process_id": "HLS-002-B",
                "sub_process_name": "Medical coding accuracy & HCC capture",
                "value_pocket_sizing": "High — revenue integrity",
                "reinvention_archetype": "Augmentation",
                "ai_pattern_description": (
                    "AI reviews clinical notes for documentation specificity, "
                    "prompts coders on HCC capture opportunities, and flags "
                    "medical necessity gaps before billing."
                ),
                "applicable_ai_patterns": [
                    "classification",
                    "extraction",
                    "nlp",
                ],
            },
        ],
        "prerequisites": [
            "EHR with FHIR API or equivalent integration",
            "HIPAA-compliant audio capture infrastructure",
            "Physician champion and clinical informatics support",
        ],
        "typical_outcomes_when_done_well": [
            "Physician documentation time reduction of 50-70%",
            "After-hours charting (pajama time) near-eliminated",
            "Coding accuracy improvement 15-25%; denial rate reduction 20-30%",
        ],
    },

    # HLS-003  Supply Chain / Pharmacy
    {
        "process_id": "HLS-003",
        "process_name": "Healthcare Supply Chain & Pharmacy Optimisation",
        "tier": 2,
        "industries_applicable": ["Healthcare & Life Sciences"],
        "sub_processes": [
            {
                "sub_process_id": "HLS-003-A",
                "sub_process_name": "Pharmaceutical demand forecasting & inventory optimisation",
                "value_pocket_sizing": "High — drug waste and stockout cost reduction",
                "reinvention_archetype": "Reinvention",
                "ai_pattern_description": (
                    "ML demand forecasting for drugs and medical supplies "
                    "incorporating patient census, seasonal patterns, and "
                    "procedure scheduling data to right-size inventory."
                ),
                "applicable_ai_patterns": [
                    "time_series",
                    "probabilistic_forecasting",
                    "optimisation",
                ],
            },
        ],
        "prerequisites": [
            "ERP or materials management system",
            "2+ years of consumption history by SKU",
            "Patient census and procedure scheduling feeds",
        ],
        "typical_outcomes_when_done_well": [
            "Drug waste reduction of 15-25%",
            "Stockout events for critical drugs reduction of 20-35%",
            "Inventory carrying cost reduction of 10-20%",
        ],
    },

    # HLS-004  Staff Scheduling
    {
        "process_id": "HLS-004",
        "process_name": "Clinical Staff Scheduling Optimisation",
        "tier": 3,
        "industries_applicable": ["Healthcare & Life Sciences"],
        "sub_processes": [
            {
                "sub_process_id": "HLS-004-A",
                "sub_process_name": "AI-assisted nurse / clinical staff scheduling",
                "value_pocket_sizing": "High — agency staff cost and overtime reduction",
                "reinvention_archetype": "Reinvention",
                "ai_pattern_description": (
                    "Constraint optimisation and demand forecasting models generate "
                    "staff schedules that match predicted patient volume to skill mix "
                    "while respecting regulatory and union constraints."
                ),
                "applicable_ai_patterns": [
                    "optimisation",
                    "scheduling",
                    "time_series",
                ],
            },
        ],
        "prerequisites": [
            "Workforce management system (Kronos, API Healthcare, etc.)",
            "Patient acuity and census forecasting capability",
            "Union / regulatory scheduling rules documented",
        ],
        "typical_outcomes_when_done_well": [
            "Agency / registry staff spend reduction of 15-30%",
            "Overtime cost reduction of 10-20%",
            "Staff satisfaction improvement from more predictable schedules",
        ],
    },
]


# ---------------------------------------------------------------------------
# Manufacturing (MFG) — Tier 2 & 3 processes (4 entries)
# ---------------------------------------------------------------------------

MFG_PROCESSES: List[Dict[str, Any]] = [

    # MFG-001  Field Service
    {
        "process_id": "MFG-001",
        "process_name": "Field Service & Asset Maintenance",
        "tier": 2,
        "industries_applicable": ["Manufacturing"],
        "sub_processes": [
            {
                "sub_process_id": "MFG-001-A",
                "sub_process_name": "Predictive failure detection & maintenance alerting",
                "value_pocket_sizing": "High — unplanned downtime costs $50K-500K/hr",
                "reinvention_archetype": "Reinvention",
                "ai_pattern_description": (
                    "LSTM / transformer model on historian / IoT sensor data "
                    "identifies deviation patterns preceding known failure modes; "
                    "alerts sent to CMMS with recommended action and parts list."
                ),
                "applicable_ai_patterns": [
                    "time_series",
                    "anomaly_detection",
                    "iot_streaming",
                ],
            },
            {
                "sub_process_id": "MFG-001-B",
                "sub_process_name": "AI-assisted field technician guidance",
                "value_pocket_sizing": "Medium — first-time fix rate improvement",
                "reinvention_archetype": "Augmentation",
                "ai_pattern_description": (
                    "Mobile RAG assistant gives field technicians instant access "
                    "to maintenance history, schematics, and resolution steps "
                    "for the asset they are servicing."
                ),
                "applicable_ai_patterns": ["rag", "question_answering"],
            },
        ],
        "prerequisites": [
            "IoT sensors or historian data on critical assets (18+ months)",
            "CMMS / EAM system with API",
            "Defined critical asset list",
        ],
        "typical_outcomes_when_done_well": [
            "Unplanned downtime reduction of 20-40%",
            "Maintenance cost reduction of 10-25%",
            "First-time fix rate improvement of 15-25 percentage points",
        ],
    },

    # MFG-002  Quality Inspection
    {
        "process_id": "MFG-002",
        "process_name": "Quality Inspection & Defect Detection",
        "tier": 2,
        "industries_applicable": ["Manufacturing"],
        "sub_processes": [
            {
                "sub_process_id": "MFG-002-A",
                "sub_process_name": "Automated visual inspection (computer vision)",
                "value_pocket_sizing": "High — defect escape cost 10-100x detection cost",
                "reinvention_archetype": "Automation",
                "ai_pattern_description": (
                    "Computer vision model detects surface defects, dimensional errors, "
                    "and assembly errors at machine speed; auto-routes rejects "
                    "and logs defect data for root-cause analysis."
                ),
                "applicable_ai_patterns": [
                    "cv",
                    "object_detection",
                    "anomaly_detection",
                ],
            },
        ],
        "prerequisites": [
            "Camera / imaging infrastructure at inspection station",
            "Historical defect image library (500+ images per defect class)",
            "Quality team willing to validate and tune model",
        ],
        "typical_outcomes_when_done_well": [
            "Defect escape rate reduction of 60-90%",
            "Inspection throughput 3-10x human rate",
            "QC labour cost reduction of 40-60%",
        ],
    },

    # MFG-003  Supply Chain Forecasting
    {
        "process_id": "MFG-003",
        "process_name": "Supply Chain Demand Forecasting",
        "tier": 2,
        "industries_applicable": ["Manufacturing"],
        "sub_processes": [
            {
                "sub_process_id": "MFG-003-A",
                "sub_process_name": "Multi-echelon probabilistic demand forecasting",
                "value_pocket_sizing": "High — each 1% forecast accuracy = 0.5% inventory cost",
                "reinvention_archetype": "Reinvention",
                "ai_pattern_description": (
                    "Ensemble of gradient-boosting and deep learning time-series models "
                    "with external signal ingestion (weather, economic, events) produces "
                    "probabilistic forecasts driving inventory safety-stock calculations."
                ),
                "applicable_ai_patterns": [
                    "time_series",
                    "probabilistic_forecasting",
                    "external_signals",
                ],
            },
        ],
        "prerequisites": [
            "ERP / SCM with 3+ years of demand history",
            "External signal data pipeline",
            "Demand planning team willing to adopt probabilistic outputs",
        ],
        "typical_outcomes_when_done_well": [
            "Forecast MAPE improvement of 20-35%",
            "Inventory carrying cost reduction of 10-20%",
            "Stockout frequency reduction of 15-30%",
        ],
    },

    # MFG-004  Production Scheduling
    {
        "process_id": "MFG-004",
        "process_name": "Production Planning & Scheduling Optimisation",
        "tier": 3,
        "industries_applicable": ["Manufacturing"],
        "sub_processes": [
            {
                "sub_process_id": "MFG-004-A",
                "sub_process_name": "Dynamic production scheduling & sequencing",
                "value_pocket_sizing": "High — OEE and changeover time value",
                "reinvention_archetype": "Reinvention",
                "ai_pattern_description": (
                    "Constraint optimisation or reinforcement learning generates "
                    "real-time production schedules balancing demand, capacity, "
                    "materials availability, and changeover costs."
                ),
                "applicable_ai_patterns": [
                    "optimisation",
                    "reinforcement_learning",
                    "simulation",
                ],
            },
        ],
        "prerequisites": [
            "MES integration with real-time capacity visibility",
            "Demand forecast input from supply chain team",
            "Bill-of-materials and routing data clean and maintained",
        ],
        "typical_outcomes_when_done_well": [
            "OEE improvement of 5-15%",
            "Changeover time reduction of 10-25%",
            "On-time-in-full delivery improvement of 5-10 percentage points",
        ],
    },
]


# ---------------------------------------------------------------------------
# Lookup structures
# ---------------------------------------------------------------------------

FULL_COVERAGE_INDUSTRIES = {
    "Financial Services",
    "Banking",
    "Insurance",
    "Healthcare & Life Sciences",
    "Healthcare",
    "Life Sciences",
    "Pharmaceuticals",
    "Manufacturing",
}

# NAICS code prefixes that map to canonical verticals
NAICS_TO_VERTICAL: Dict[str, str] = {
    "52": "Financial Services",
    "62": "Healthcare & Life Sciences",
    "31": "Manufacturing",
    "32": "Manufacturing",
    "33": "Manufacturing",
}

PROCESSES_BY_VERTICAL: Dict[str, List[Dict[str, Any]]] = {
    "Financial Services": TIER1_UNIVERSAL + FS_PROCESSES,
    "Healthcare & Life Sciences": TIER1_UNIVERSAL + HLS_PROCESSES,
    "Manufacturing": TIER1_UNIVERSAL + MFG_PROCESSES,
    "Other": TIER1_UNIVERSAL,
}


# ---------------------------------------------------------------------------
# Accessor functions
# ---------------------------------------------------------------------------


def get_industry_library() -> Dict[str, List[Dict[str, Any]]]:
    """Return the full industry library keyed by vertical name."""
    return {
        "universal": TIER1_UNIVERSAL,
        "Financial Services": FS_PROCESSES,
        "Healthcare & Life Sciences": HLS_PROCESSES,
        "Manufacturing": MFG_PROCESSES,
    }


def get_processes_for_industry(
    industry_label: str,
    naics_code: str = "",
) -> Dict[str, Any]:
    """Return applicable processes and coverage metadata for a given industry.

    Args:
        industry_label: Human-readable industry label (e.g. 'Financial Services').
        naics_code: NAICS code string used as fallback when label is ambiguous.

    Returns:
        dict with keys:
            processes: list of applicable process entries
            library_status: 'full_coverage' | 'tier1_only'
            industry_match: 'exact' | 'not_in_library'
            matched_vertical: canonical vertical name or None
            coverage_gaps: description of any gaps
            v05_gap_flagged: bool
    """
    label_lower = industry_label.strip().lower()
    matched_vertical: Optional[str] = None

    # Resolve via label
    if any(k in label_lower for k in ("financ", "bank", "insur", "capital", "asset")):
        matched_vertical = "Financial Services"
    elif any(k in label_lower for k in ("health", "life sci", "pharma", "biotech", "medic", "clinical")):
        matched_vertical = "Healthcare & Life Sciences"
    elif any(k in label_lower for k in ("manufactur", "industrial", "aerospace", "automotive", "chemical")):
        matched_vertical = "Manufacturing"

    # Fallback via NAICS prefix
    if matched_vertical is None and naics_code:
        matched_vertical = NAICS_TO_VERTICAL.get(naics_code[:2])

    if matched_vertical is not None:
        return {
            "processes": PROCESSES_BY_VERTICAL[matched_vertical],
            "library_status": "full_coverage",
            "industry_match": "exact",
            "matched_vertical": matched_vertical,
            "coverage_gaps": "",
            "v05_gap_flagged": False,
        }

    # No match — Tier 1 universal only
    return {
        "processes": TIER1_UNIVERSAL,
        "library_status": "tier1_only",
        "industry_match": "not_in_library",
        "matched_vertical": None,
        "coverage_gaps": (
            f"Industry '{industry_label}' is not in the V0 library (FS, HLS, MFG). "
            "Only Tier 1 universal processes returned. Full industry-specific coverage "
            "is planned for V0.5."
        ),
        "v05_gap_flagged": True,
    }
