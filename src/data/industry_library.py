"""Industry Process Library for DXC AI Readiness Diagnostic V0.

Full coverage: Financial Services (FS), Healthcare & Life Sciences (HLS),
Manufacturing (MFG).

For all other industries: Tier 1 (universal) processes only — V0.5 gap flagged.
"""

from typing import List, Dict, Any


# ---------------------------------------------------------------------------
# Tier 1 — Universal processes (apply to all industries)
# ---------------------------------------------------------------------------

TIER1_UNIVERSAL: List[Dict[str, Any]] = [
    {
        "process_id": "T1-001",
        "process_name": "Intelligent Document Processing",
        "tier": 1,
        "industries_applicable": ["All"],
        "sub_processes": [
            {
                "sub_process_id": "T1-001-A",
                "sub_process_name": "Unstructured data extraction",
                "value_pocket_sizing": "High",
                "reinvention_archetype": "Augmentation",
                "ai_pattern_description": "LLM-based extraction of structured fields from contracts, invoices, forms",
                "applicable_ai_patterns": ["document_understanding", "extraction", "classification"],
            },
            {
                "sub_process_id": "T1-001-B",
                "sub_process_name": "Document routing and triage",
                "value_pocket_sizing": "Medium",
                "reinvention_archetype": "Automation",
                "ai_pattern_description": "Classify and route incoming documents to correct workflow queues",
                "applicable_ai_patterns": ["classification", "routing"],
            },
        ],
        "prerequisites": ["Digitised documents available", "Document management system in place"],
        "typical_outcomes_when_done_well": [
            "60-80% reduction in manual data-entry FTE cost",
            "Processing time from days to minutes",
            "Error rate reduction >90%",
        ],
        "applications": [
            {
                "application_id": "T1-001-APP1",
                "application_name": "Contract Intelligence",
                "ai_approach": "LLM extraction + semantic search",
                "expected_benefit": "Reduce contract review time by 70%",
                "implementation_complexity": "medium",
            }
        ],
    },
    {
        "process_id": "T1-002",
        "process_name": "Knowledge Management & Employee Support",
        "tier": 1,
        "industries_applicable": ["All"],
        "sub_processes": [
            {
                "sub_process_id": "T1-002-A",
                "sub_process_name": "Internal knowledge search",
                "value_pocket_sizing": "Medium",
                "reinvention_archetype": "Augmentation",
                "ai_pattern_description": "RAG-based enterprise knowledge assistant for employee self-service",
                "applicable_ai_patterns": ["rag", "semantic_search", "question_answering"],
            },
        ],
        "prerequisites": ["Internal documentation available in digital form"],
        "typical_outcomes_when_done_well": [
            "30-50% reduction in tier-1 support tickets",
            "Employee productivity uplift 15-25%",
        ],
        "applications": [
            {
                "application_id": "T1-002-APP1",
                "application_name": "AI Employee Assistant",
                "ai_approach": "RAG over internal knowledge bases",
                "expected_benefit": "Reduce HR/IT support load by 35%",
                "implementation_complexity": "low",
            }
        ],
    },
    {
        "process_id": "T1-003",
        "process_name": "Customer Service Automation",
        "tier": 1,
        "industries_applicable": ["All"],
        "sub_processes": [
            {
                "sub_process_id": "T1-003-A",
                "sub_process_name": "Intent classification and routing",
                "value_pocket_sizing": "High",
                "reinvention_archetype": "Automation",
                "ai_pattern_description": "Classify customer intent and route to appropriate resolution path",
                "applicable_ai_patterns": ["classification", "routing", "dialogue"],
            },
            {
                "sub_process_id": "T1-003-B",
                "sub_process_name": "Agent assist / next-best-action",
                "value_pocket_sizing": "High",
                "reinvention_archetype": "Augmentation",
                "ai_pattern_description": "Real-time guidance to human agents during customer interactions",
                "applicable_ai_patterns": ["real_time_inference", "recommendation"],
            },
        ],
        "prerequisites": ["CRM system with interaction history", "Contact centre infrastructure"],
        "typical_outcomes_when_done_well": [
            "20-40% handle-time reduction",
            "CSAT improvement 8-15 points",
            "First-contact resolution +10-20%",
        ],
        "applications": [],
    },
    {
        "process_id": "T1-004",
        "process_name": "Procurement & Spend Analytics",
        "tier": 1,
        "industries_applicable": ["All"],
        "sub_processes": [
            {
                "sub_process_id": "T1-004-A",
                "sub_process_name": "Spend categorisation",
                "value_pocket_sizing": "Medium",
                "reinvention_archetype": "Automation",
                "ai_pattern_description": "Automated classification of spend data into taxonomy categories",
                "applicable_ai_patterns": ["classification", "taxonomy_mapping"],
            },
        ],
        "prerequisites": ["ERP with accounts payable data"],
        "typical_outcomes_when_done_well": [
            "3-5% total spend savings from improved visibility",
            "Maverick spend reduction 20-40%",
        ],
        "applications": [],
    },
]


# ---------------------------------------------------------------------------
# Financial Services (FS) — Tier 2 & 3 processes
# ---------------------------------------------------------------------------

FS_PROCESSES: List[Dict[str, Any]] = [
    {
        "process_id": "FS-001",
        "process_name": "Credit Risk Underwriting",
        "tier": 2,
        "industries_applicable": ["Financial Services"],
        "sub_processes": [
            {
                "sub_process_id": "FS-001-A",
                "sub_process_name": "Automated credit decisioning",
                "value_pocket_sizing": "High — $2-8M/yr per $1B loan portfolio",
                "reinvention_archetype": "Reinvention",
                "ai_pattern_description": "ML models replacing or augmenting FICO-based decisioning with alternative data signals",
                "applicable_ai_patterns": ["gradient_boosting", "neural_net", "alternative_data"],
            },
            {
                "sub_process_id": "FS-001-B",
                "sub_process_name": "Document verification (KYC/KYB)",
                "value_pocket_sizing": "High",
                "reinvention_archetype": "Automation",
                "ai_pattern_description": "ID document extraction, liveness detection, entity matching",
                "applicable_ai_patterns": ["cv", "document_understanding", "entity_matching"],
            },
        ],
        "prerequisites": ["Historical loan performance data", "Core banking system access"],
        "typical_outcomes_when_done_well": [
            "Loss rate reduction 10-25%",
            "Approval decisioning time: days to seconds",
            "Onboarding cost reduction 30-50%",
        ],
        "applications": [
            {
                "application_id": "FS-001-APP1",
                "application_name": "AI Underwriting Workbench",
                "ai_approach": "Gradient boosting + LLM narrative generation",
                "expected_benefit": "25% reduction in credit losses on new originations",
                "implementation_complexity": "high",
            }
        ],
    },
    {
        "process_id": "FS-002",
        "process_name": "Fraud Detection & Financial Crime",
        "tier": 2,
        "industries_applicable": ["Financial Services"],
        "sub_processes": [
            {
                "sub_process_id": "FS-002-A",
                "sub_process_name": "Real-time transaction fraud scoring",
                "value_pocket_sizing": "High — typically 3-7x ROI",
                "reinvention_archetype": "Reinvention",
                "ai_pattern_description": "Graph neural networks and anomaly detection on transaction streams",
                "applicable_ai_patterns": ["graph_nn", "anomaly_detection", "streaming_ml"],
            },
            {
                "sub_process_id": "FS-002-B",
                "sub_process_name": "AML transaction monitoring",
                "value_pocket_sizing": "High — regulatory penalty avoidance",
                "reinvention_archetype": "Augmentation",
                "ai_pattern_description": "ML-based alert prioritisation reducing false-positive rate",
                "applicable_ai_patterns": ["classification", "anomaly_detection"],
            },
        ],
        "prerequisites": ["Transaction data lake", "Case management system"],
        "typical_outcomes_when_done_well": [
            "False-positive reduction 40-60%",
            "Fraud loss reduction 20-35%",
            "SAR filing quality improvement",
        ],
        "applications": [],
    },
    {
        "process_id": "FS-003",
        "process_name": "Regulatory Reporting Automation",
        "tier": 2,
        "industries_applicable": ["Financial Services"],
        "sub_processes": [
            {
                "sub_process_id": "FS-003-A",
                "sub_process_name": "Automated regulatory report generation",
                "value_pocket_sizing": "Medium — $500K-2M/yr cost avoidance",
                "reinvention_archetype": "Automation",
                "ai_pattern_description": "LLM-assisted generation and validation of Basel, DORA, IFRS9 reports",
                "applicable_ai_patterns": ["document_generation", "validation", "extraction"],
            },
        ],
        "prerequisites": ["Data warehouse with regulatory data mart"],
        "typical_outcomes_when_done_well": [
            "Report preparation time -60%",
            "Error rate reduction >80%",
            "Audit trail automation",
        ],
        "applications": [],
    },
    {
        "process_id": "FS-004",
        "process_name": "Personalised Customer Engagement",
        "tier": 3,
        "industries_applicable": ["Financial Services"],
        "sub_processes": [
            {
                "sub_process_id": "FS-004-A",
                "sub_process_name": "Next-best-offer / next-best-action",
                "value_pocket_sizing": "High",
                "reinvention_archetype": "Reinvention",
                "ai_pattern_description": "Real-time personalisation engine for product recommendations at customer touchpoints",
                "applicable_ai_patterns": ["recommendation", "real_time_inference", "contextual_bandit"],
            },
        ],
        "prerequisites": ["Unified customer profile", "Digital channels with event streaming"],
        "typical_outcomes_when_done_well": [
            "Product cross-sell conversion +15-30%",
            "Customer lifetime value improvement 8-20%",
        ],
        "applications": [],
    },
]


# ---------------------------------------------------------------------------
# Healthcare & Life Sciences (HLS) — Tier 2 & 3 processes
# ---------------------------------------------------------------------------

HLS_PROCESSES: List[Dict[str, Any]] = [
    {
        "process_id": "HLS-001",
        "process_name": "Clinical Documentation Intelligence",
        "tier": 2,
        "industries_applicable": ["Healthcare & Life Sciences"],
        "sub_processes": [
            {
                "sub_process_id": "HLS-001-A",
                "sub_process_name": "Ambient clinical documentation (AI scribe)",
                "value_pocket_sizing": "High — 1-2 hrs/physician/day saved",
                "reinvention_archetype": "Augmentation",
                "ai_pattern_description": "Speech-to-text + LLM drafting of clinical notes from patient encounter audio",
                "applicable_ai_patterns": ["speech_recognition", "llm_generation", "medical_coding"],
            },
            {
                "sub_process_id": "HLS-001-B",
                "sub_process_name": "Medical coding automation",
                "value_pocket_sizing": "High",
                "reinvention_archetype": "Automation",
                "ai_pattern_description": "Automated ICD-10/CPT code assignment from clinical notes",
                "applicable_ai_patterns": ["classification", "extraction", "nlp"],
            },
        ],
        "prerequisites": ["EHR integration capability", "Physician champion", "HIPAA-compliant infrastructure"],
        "typical_outcomes_when_done_well": [
            "Physician documentation time -50-70%",
            "Coding accuracy improvement 15-25%",
            "Denial rate reduction 20-35%",
        ],
        "applications": [
            {
                "application_id": "HLS-001-APP1",
                "application_name": "AI Clinical Scribe",
                "ai_approach": "Whisper-class ASR + LLM note structuring",
                "expected_benefit": "Recover 90 min/physician/day; reduce burnout",
                "implementation_complexity": "high",
            }
        ],
    },
    {
        "process_id": "HLS-002",
        "process_name": "Prior Authorization & Utilisation Management",
        "tier": 2,
        "industries_applicable": ["Healthcare & Life Sciences"],
        "sub_processes": [
            {
                "sub_process_id": "HLS-002-A",
                "sub_process_name": "Automated prior auth determination",
                "value_pocket_sizing": "High — $3-6M/yr per 500K lives",
                "reinvention_archetype": "Automation",
                "ai_pattern_description": "ML model trained on clinical criteria to auto-approve/pend/deny PA requests",
                "applicable_ai_patterns": ["classification", "rule_extraction", "document_understanding"],
            },
        ],
        "prerequisites": ["Clinical criteria library", "Claims data", "EHR API access"],
        "typical_outcomes_when_done_well": [
            "Auto-approval rate 40-60%",
            "Review time reduction 50%",
            "Provider abrasion reduction",
        ],
        "applications": [],
    },
    {
        "process_id": "HLS-003",
        "process_name": "Population Health & Risk Stratification",
        "tier": 2,
        "industries_applicable": ["Healthcare & Life Sciences"],
        "sub_processes": [
            {
                "sub_process_id": "HLS-003-A",
                "sub_process_name": "High-risk patient identification",
                "value_pocket_sizing": "High — avoidable admissions cost $15-30K each",
                "reinvention_archetype": "Reinvention",
                "ai_pattern_description": "Predictive models on claims + clinical data to identify patients at risk of deterioration",
                "applicable_ai_patterns": ["risk_scoring", "time_series", "gradient_boosting"],
            },
        ],
        "prerequisites": ["Claims data lake", "ADT feeds", "Care management workflow"],
        "typical_outcomes_when_done_well": [
            "Avoidable readmission reduction 15-25%",
            "Care management ROI 3-5x",
        ],
        "applications": [],
    },
    {
        "process_id": "HLS-004",
        "process_name": "Drug Discovery & Clinical Trial Optimisation",
        "tier": 3,
        "industries_applicable": ["Healthcare & Life Sciences"],
        "sub_processes": [
            {
                "sub_process_id": "HLS-004-A",
                "sub_process_name": "Clinical trial patient matching",
                "value_pocket_sizing": "High — each month of trial acceleration = $1-5M",
                "reinvention_archetype": "Reinvention",
                "ai_pattern_description": "NLP-based matching of patient records to trial eligibility criteria",
                "applicable_ai_patterns": ["nlp", "entity_matching", "semantic_search"],
            },
        ],
        "prerequisites": ["EHR data access", "Trial protocol library", "IRB approval process"],
        "typical_outcomes_when_done_well": [
            "Enrollment acceleration 20-40%",
            "Screen failure rate reduction",
        ],
        "applications": [],
    },
]


# ---------------------------------------------------------------------------
# Manufacturing (MFG) — Tier 2 & 3 processes
# ---------------------------------------------------------------------------

MFG_PROCESSES: List[Dict[str, Any]] = [
    {
        "process_id": "MFG-001",
        "process_name": "Predictive Maintenance & Asset Intelligence",
        "tier": 2,
        "industries_applicable": ["Manufacturing"],
        "sub_processes": [
            {
                "sub_process_id": "MFG-001-A",
                "sub_process_name": "Predictive failure detection",
                "value_pocket_sizing": "High — unplanned downtime costs $50K-500K/hr",
                "reinvention_archetype": "Reinvention",
                "ai_pattern_description": "Time-series anomaly detection on sensor data to predict equipment failure",
                "applicable_ai_patterns": ["time_series", "anomaly_detection", "iot_streaming"],
            },
            {
                "sub_process_id": "MFG-001-B",
                "sub_process_name": "Maintenance work order optimisation",
                "value_pocket_sizing": "Medium",
                "reinvention_archetype": "Augmentation",
                "ai_pattern_description": "AI-assisted scheduling and prioritisation of maintenance activities",
                "applicable_ai_patterns": ["optimisation", "scheduling", "recommendation"],
            },
        ],
        "prerequisites": ["IoT sensors on critical assets", "Historian or time-series DB", "CMMS system"],
        "typical_outcomes_when_done_well": [
            "Unplanned downtime reduction 20-40%",
            "Maintenance cost reduction 10-25%",
            "Asset life extension 15-20%",
        ],
        "applications": [
            {
                "application_id": "MFG-001-APP1",
                "application_name": "AI Asset Health Monitor",
                "ai_approach": "LSTM/transformer on sensor telemetry + work order NLP",
                "expected_benefit": "Prevent 3-5 unplanned outages/yr per major asset",
                "implementation_complexity": "high",
            }
        ],
    },
    {
        "process_id": "MFG-002",
        "process_name": "Quality Inspection & Defect Detection",
        "tier": 2,
        "industries_applicable": ["Manufacturing"],
        "sub_processes": [
            {
                "sub_process_id": "MFG-002-A",
                "sub_process_name": "Automated visual inspection",
                "value_pocket_sizing": "High — defect escape cost 10-100x detection cost",
                "reinvention_archetype": "Automation",
                "ai_pattern_description": "Computer vision models detecting surface defects, dimensional errors, assembly errors",
                "applicable_ai_patterns": ["cv", "object_detection", "anomaly_detection"],
            },
        ],
        "prerequisites": ["Camera/imaging infrastructure on line", "Historical defect image library"],
        "typical_outcomes_when_done_well": [
            "Defect escape rate reduction 60-90%",
            "Inspection throughput 3-10x human rate",
            "Labour cost reduction in QC 40-60%",
        ],
        "applications": [],
    },
    {
        "process_id": "MFG-003",
        "process_name": "Supply Chain Demand Forecasting",
        "tier": 2,
        "industries_applicable": ["Manufacturing"],
        "sub_processes": [
            {
                "sub_process_id": "MFG-003-A",
                "sub_process_name": "Multi-echelon demand forecasting",
                "value_pocket_sizing": "High — each 1% forecast accuracy = 0.5% inventory cost",
                "reinvention_archetype": "Reinvention",
                "ai_pattern_description": "Probabilistic forecasting models incorporating external signals (weather, economic, events)",
                "applicable_ai_patterns": ["time_series", "probabilistic_forecasting", "external_signals"],
            },
        ],
        "prerequisites": ["ERP/SCM system", "3+ years historical demand data", "External data feeds"],
        "typical_outcomes_when_done_well": [
            "Forecast accuracy improvement 20-35%",
            "Inventory reduction 10-20%",
            "Service level improvement 5-10%",
        ],
        "applications": [],
    },
    {
        "process_id": "MFG-004",
        "process_name": "Production Planning Optimisation",
        "tier": 3,
        "industries_applicable": ["Manufacturing"],
        "sub_processes": [
            {
                "sub_process_id": "MFG-004-A",
                "sub_process_name": "Dynamic production scheduling",
                "value_pocket_sizing": "High",
                "reinvention_archetype": "Reinvention",
                "ai_pattern_description": "Reinforcement learning or constraint optimisation for real-time production scheduling",
                "applicable_ai_patterns": ["optimisation", "reinforcement_learning", "simulation"],
            },
        ],
        "prerequisites": ["MES integration", "Real-time capacity visibility", "Demand forecast input"],
        "typical_outcomes_when_done_well": [
            "OEE improvement 5-15%",
            "Changeover time reduction 10-25%",
        ],
        "applications": [],
    },
]


# ---------------------------------------------------------------------------
# Lookup structures
# ---------------------------------------------------------------------------

# Industries with full library coverage in V0
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

# NAICS code prefixes that map to our full-coverage verticals
NAICS_TO_VERTICAL = {
    "52": "Financial Services",   # Finance and Insurance
    "62": "Healthcare & Life Sciences",  # Health Care and Social Assistance
    "31": "Manufacturing",
    "32": "Manufacturing",
    "33": "Manufacturing",
}

# All processes by vertical for quick lookup
PROCESSES_BY_VERTICAL: Dict[str, List[Dict[str, Any]]] = {
    "Financial Services": TIER1_UNIVERSAL + FS_PROCESSES,
    "Healthcare & Life Sciences": TIER1_UNIVERSAL + HLS_PROCESSES,
    "Manufacturing": TIER1_UNIVERSAL + MFG_PROCESSES,
    "Other": TIER1_UNIVERSAL,
}


def get_processes_for_industry(
    industry_label: str,
    naics_code: str = "",
) -> Dict[str, Any]:
    """Return applicable processes and coverage metadata for a given industry.

    Args:
        industry_label: Human-readable industry label (e.g. 'Financial Services').
        naics_code: NAICS code string (used as fallback when label is ambiguous).

    Returns:
        dict with keys: processes, library_status, industry_match, coverage_gaps
    """
    label_normalised = industry_label.strip().lower()

    # Resolve via label
    matched_vertical = None
    for vertical in FULL_COVERAGE_INDUSTRIES:
        if vertical.lower() in label_normalised or label_normalised in vertical.lower():
            # Map sub-labels to canonical verticals
            if any(k in label_normalised for k in ("financ", "bank", "insur", "capital")):
                matched_vertical = "Financial Services"
            elif any(k in label_normalised for k in ("health", "life sci", "pharma", "biotech", "medic")):
                matched_vertical = "Healthcare & Life Sciences"
            elif any(k in label_normalised for k in ("manufactur", "industrial", "aerospace", "automotive")):
                matched_vertical = "Manufacturing"
            break

    # Fallback: resolve via NAICS prefix
    if matched_vertical is None and naics_code:
        prefix_2 = naics_code[:2]
        matched_vertical = NAICS_TO_VERTICAL.get(prefix_2)

    if matched_vertical is not None:
        processes = PROCESSES_BY_VERTICAL[matched_vertical]
        return {
            "processes": processes,
            "library_status": "full_coverage",
            "industry_match": "exact",
            "matched_vertical": matched_vertical,
            "coverage_gaps": "",
            "v05_gap_flagged": False,
        }

    # No match — Tier 1 only
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
