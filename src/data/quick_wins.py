"""Quick Wins Library for DXC AI Readiness Diagnostic V0.

Each pattern is a proven, fast-to-value AI use case that can be delivered
in 8-16 weeks with measurable ROI. Selection criteria:
  - Implementation effort: low or medium
  - Time-to-value: <= 16 weeks
  - Prerequisites achievable by target prospect profile
"""

from typing import List, Dict, Any


QUICK_WIN_PATTERNS: List[Dict[str, Any]] = [
    # -----------------------------------------------------------------------
    # Universal / Cross-Industry
    # -----------------------------------------------------------------------
    {
        "pattern_id": "QW-001",
        "name": "AI-Powered Contract Intelligence",
        "one_line_description": "Extract key clauses, obligations, and risk terms from contracts automatically.",
        "what_the_ai_does": (
            "An LLM-based extraction pipeline ingests contracts in any format and identifies "
            "key fields: parties, governing law, termination clauses, payment terms, liability caps, "
            "and non-standard provisions. Output is structured data reviewable in a simple dashboard."
        ),
        "prerequisites": [
            "Contracts available in digital format (PDF or Word)",
            "Legal or procurement team willing to validate output",
            "Data classification policy allows AI processing of contract content",
        ],
        "expected_outcomes": [
            "Contract review time reduced 60-80%",
            "Missed obligation risk materially reduced",
            "Self-service contract search enabled",
        ],
        "implementation_effort": "low",
        "timeline_to_value_weeks": 8,
        "applicable_industries": ["All"],
        "applicable_sizes": ["Mid-Market", "Large", "Enterprise"],
        "disqualifying_conditions": [
            "Contracts stored only in physical paper with no scanning infrastructure",
            "Data classification policy prohibits AI processing of legal documents",
        ],
        "peer_examples": [
            "Mid-market logistics firm reduced contract review from 4 hrs to 20 mins per agreement",
            "Regional bank cut contract risk exceptions by 35% in first quarter post-deployment",
        ],
    },
    {
        "pattern_id": "QW-002",
        "name": "Employee Knowledge Assistant (RAG)",
        "one_line_description": "Give employees instant answers from internal documentation without IT tickets.",
        "what_the_ai_does": (
            "A retrieval-augmented generation system indexes internal policies, SOPs, product "
            "documentation, and HR guides. Employees ask questions in natural language and receive "
            "cited, accurate answers in seconds."
        ),
        "prerequisites": [
            "Internal documentation in accessible digital repositories (SharePoint, Confluence, etc.)",
            "At least 500 documents to form a meaningful knowledge base",
            "IT approval for secure document ingestion",
        ],
        "expected_outcomes": [
            "Tier-1 support tickets reduced 30-50%",
            "New employee ramp time reduced 2-4 weeks",
            "Employee satisfaction with information access improved",
        ],
        "implementation_effort": "low",
        "timeline_to_value_weeks": 6,
        "applicable_industries": ["All"],
        "applicable_sizes": ["Mid-Market", "Large", "Enterprise"],
        "disqualifying_conditions": [
            "Internal documentation does not exist in structured digital form",
            "Security policy prohibits cloud-based AI processing of internal documents",
        ],
        "peer_examples": [
            "500-person technology firm reduced HR queries by 40% in 6 weeks",
            "Manufacturer cut new-line-worker training support calls by 45%",
        ],
    },
    {
        "pattern_id": "QW-003",
        "name": "AI Meeting Summarisation & Action Extraction",
        "one_line_description": "Turn meeting recordings into structured summaries, decisions, and action items automatically.",
        "what_the_ai_does": (
            "Transcription integrated with LLM summarisation captures every meeting, extracts "
            "decisions and assigned actions, and routes follow-ups to owners — eliminating manual "
            "note-taking and missed commitments."
        ),
        "prerequisites": [
            "Video conferencing platform (Teams, Zoom, Webex)",
            "Acceptable use policy updated for AI transcription",
            "Pilot group of 20-50 users willing to participate",
        ],
        "expected_outcomes": [
            "90%+ of action items captured vs ~60% without AI",
            "Meeting admin time reduced 1-2 hrs/week per knowledge worker",
            "Decision audit trail created automatically",
        ],
        "implementation_effort": "low",
        "timeline_to_value_weeks": 4,
        "applicable_industries": ["All"],
        "applicable_sizes": ["Mid-Market", "Large", "Enterprise"],
        "disqualifying_conditions": [
            "Regulatory prohibition on recording meetings in the prospect's jurisdiction",
            "All-in-person workforce with no video conferencing infrastructure",
        ],
        "peer_examples": [
            "Professional services firm saved 2.5 hrs/week per consultant",
            "Healthcare payer reduced compliance meeting re-work by 60%",
        ],
    },
    {
        "pattern_id": "QW-004",
        "name": "Intelligent Invoice Processing",
        "one_line_description": "Automate accounts payable data entry and matching with AI document understanding.",
        "what_the_ai_does": (
            "Computer vision and LLM extraction capture line-item data from invoices in any format, "
            "match to POs, flag discrepancies, and push clean data to ERP — replacing manual keying."
        ),
        "prerequisites": [
            "ERP system (SAP, Oracle, Dynamics, or similar)",
            "Invoice volume >500/month to justify automation",
            "AP team willing to validate and refine in pilot phase",
        ],
        "expected_outcomes": [
            "Invoice processing cost reduced 60-80%",
            "Processing time from days to hours",
            "Early payment discount capture improved",
        ],
        "implementation_effort": "medium",
        "timeline_to_value_weeks": 10,
        "applicable_industries": ["All"],
        "applicable_sizes": ["Mid-Market", "Large", "Enterprise"],
        "disqualifying_conditions": [
            "Invoice volume <200/month (insufficient to justify)",
            "No ERP system in place for integration target",
        ],
        "peer_examples": [
            "Mid-market manufacturer reduced AP headcount requirement by 3 FTEs",
            "Distributor improved early payment discount capture by $400K/yr",
        ],
    },
    # -----------------------------------------------------------------------
    # Financial Services
    # -----------------------------------------------------------------------
    {
        "pattern_id": "QW-FS-001",
        "name": "AI-Assisted Loan Document Review",
        "one_line_description": "Accelerate credit underwriting by extracting financial covenants and risk flags from loan packages.",
        "what_the_ai_does": (
            "LLM-based document analysis ingests loan applications, financial statements, and "
            "supporting documents, extracts structured fields (debt ratios, covenants, ownership "
            "structure), flags inconsistencies, and drafts a credit memo outline for analyst review."
        ),
        "prerequisites": [
            "Loan documents available in digital format",
            "Credit underwriting team willing to use AI-assisted workflow",
            "Data governance approval for AI processing of financial documents",
        ],
        "expected_outcomes": [
            "Underwriting cycle time reduced 30-50%",
            "Analyst capacity freed for complex judgement",
            "Document completeness errors reduced",
        ],
        "implementation_effort": "medium",
        "timeline_to_value_weeks": 12,
        "applicable_industries": ["Financial Services"],
        "applicable_sizes": ["Mid-Market", "Large", "Enterprise"],
        "disqualifying_conditions": [
            "Less than 50 loan originations per month",
            "Core banking system prevents document extraction",
        ],
        "peer_examples": [
            "Community bank reduced underwriting time from 12 days to 6 days",
            "Asset-based lender cut document review FTE cost by 35%",
        ],
    },
    {
        "pattern_id": "QW-FS-002",
        "name": "Regulatory Change Monitoring & Impact Analysis",
        "one_line_description": "Continuously monitor regulatory publications and flag material changes with compliance impact summaries.",
        "what_the_ai_does": (
            "An AI agent monitors regulatory feeds (CFPB, OCC, FRB, FCA, ECB, etc.), classifies "
            "new rules for relevance to the institution's product set, and generates structured "
            "impact summaries with action owners pre-populated."
        ),
        "prerequisites": [
            "Compliance team willing to receive AI-generated impact briefs",
            "List of applicable regulators and product types",
            "Secure environment for regulatory content processing",
        ],
        "expected_outcomes": [
            "Regulatory change detection lag reduced from weeks to days",
            "Compliance team capacity freed from manual monitoring",
            "Audit-ready change log maintained automatically",
        ],
        "implementation_effort": "low",
        "timeline_to_value_weeks": 8,
        "applicable_industries": ["Financial Services"],
        "applicable_sizes": ["Mid-Market", "Large", "Enterprise"],
        "disqualifying_conditions": [
            "Single-jurisdiction, single-product institution with minimal regulatory surface",
        ],
        "peer_examples": [
            "Regional bank reduced compliance monitoring FTE cost by 1.5 FTEs",
            "Insurance carrier cut regulatory change response time by 40%",
        ],
    },
    # -----------------------------------------------------------------------
    # Healthcare & Life Sciences
    # -----------------------------------------------------------------------
    {
        "pattern_id": "QW-HLS-001",
        "name": "AI Prior Authorization Pre-Screening",
        "one_line_description": "Reduce prior auth burden by auto-screening requests against clinical criteria before submission.",
        "what_the_ai_does": (
            "AI checks incoming prior auth requests against payer clinical criteria, identifies "
            "missing documentation, flags likely-to-deny cases for clinical review, and auto-populates "
            "peer-to-peer request templates — before the request is submitted."
        ),
        "prerequisites": [
            "Electronic prior auth submission in place (or fax-to-digital conversion)",
            "Payer clinical criteria library accessible",
            "Revenue cycle or case management team engaged",
        ],
        "expected_outcomes": [
            "First-pass approval rate improved 15-25%",
            "Auth team time per request reduced 30-40%",
            "Denial write-offs reduced",
        ],
        "implementation_effort": "medium",
        "timeline_to_value_weeks": 12,
        "applicable_industries": ["Healthcare & Life Sciences"],
        "applicable_sizes": ["Mid-Market", "Large", "Enterprise"],
        "disqualifying_conditions": [
            "Less than 100 prior auth requests per month",
            "No electronic submission capability",
        ],
        "peer_examples": [
            "300-bed hospital reduced auth-related denials by $1.2M/yr",
            "Multi-specialty practice cut auth processing time by 35%",
        ],
    },
    {
        "pattern_id": "QW-HLS-002",
        "name": "Clinical Documentation Quality Review",
        "one_line_description": "Flag incomplete or non-specific clinical documentation before claim submission to reduce denials.",
        "what_the_ai_does": (
            "AI reviews clinical notes for documentation specificity (HCC capture, medical necessity "
            "language, procedure documentation completeness) and prompts coders and providers to "
            "address gaps before the claim is billed."
        ),
        "prerequisites": [
            "EHR with documentation accessible for review",
            "HIM/coding team willing to work with AI-generated quality alerts",
            "HIPAA-compliant processing environment",
        ],
        "expected_outcomes": [
            "HCC capture rate improved 10-20%",
            "Claim denial rate reduced 15-25%",
            "Coder productivity improved 20-30%",
        ],
        "implementation_effort": "medium",
        "timeline_to_value_weeks": 10,
        "applicable_industries": ["Healthcare & Life Sciences"],
        "applicable_sizes": ["Mid-Market", "Large", "Enterprise"],
        "disqualifying_conditions": [
            "Paper-based clinical documentation with no EHR",
            "Physician group too small (<5 providers) for meaningful volume",
        ],
        "peer_examples": [
            "Health system recovered $2.1M in additional HCC revenue in year 1",
            "Physician practice reduced denial write-offs by 28%",
        ],
    },
    # -----------------------------------------------------------------------
    # Manufacturing
    # -----------------------------------------------------------------------
    {
        "pattern_id": "QW-MFG-001",
        "name": "AI-Powered Visual Quality Inspection Pilot",
        "one_line_description": "Deploy computer vision on one production line to catch defects at machine speed.",
        "what_the_ai_does": (
            "A computer vision model trained on historical defect images inspects every unit on "
            "the target line, classifies defect types, triggers automatic reject or rework routing, "
            "and logs defect data for root cause analysis."
        ),
        "prerequisites": [
            "Camera infrastructure installable at inspection station",
            "Historical defect image library (minimum 500 images per defect class)",
            "Quality team willing to validate and tune model",
        ],
        "expected_outcomes": [
            "Defect escape rate reduced 60-80% on pilot line",
            "Inspection throughput 3-5x human rate",
            "Defect root-cause data improved for process improvement",
        ],
        "implementation_effort": "medium",
        "timeline_to_value_weeks": 14,
        "applicable_industries": ["Manufacturing"],
        "applicable_sizes": ["Mid-Market", "Large", "Enterprise"],
        "disqualifying_conditions": [
            "No historical defect images available for model training",
            "Production environment prevents camera installation",
        ],
        "peer_examples": [
            "Automotive supplier reduced customer quality escapes by 70% on pilot line",
            "Electronics manufacturer cut final inspection FTE cost by 2.5 FTEs on one line",
        ],
    },
    {
        "pattern_id": "QW-MFG-002",
        "name": "Predictive Maintenance Pilot on Critical Asset",
        "one_line_description": "Use sensor data from one critical machine to predict failure before it causes downtime.",
        "what_the_ai_does": (
            "A time-series anomaly detection model ingests vibration, temperature, and operational "
            "sensor data from a designated critical asset, establishes baseline patterns, and issues "
            "early warnings 24-72 hours before predicted failure with recommended maintenance actions."
        ),
        "prerequisites": [
            "IoT sensors installed on target asset (or retrofittable)",
            "12+ months of historical sensor data available",
            "Maintenance team willing to act on AI-generated alerts",
        ],
        "expected_outcomes": [
            "2-4 unplanned outages prevented in first year",
            "Maintenance scheduled during planned downtime windows",
            "ROI typically 3-8x on cost of solution in year 1",
        ],
        "implementation_effort": "medium",
        "timeline_to_value_weeks": 16,
        "applicable_industries": ["Manufacturing"],
        "applicable_sizes": ["Mid-Market", "Large", "Enterprise"],
        "disqualifying_conditions": [
            "Target asset has no sensor coverage and retrofitting is not feasible",
            "Less than 6 months of sensor data available",
        ],
        "peer_examples": [
            "Process manufacturer avoided $800K unplanned outage in month 4 of deployment",
            "Food & beverage plant reduced maintenance costs by 18% on pilot asset class",
        ],
    },
    {
        "pattern_id": "QW-MFG-003",
        "name": "AI Demand Sensing for Short-Horizon Forecasting",
        "one_line_description": "Improve 4-8 week demand forecast accuracy using AI signals from sales, weather, and market data.",
        "what_the_ai_does": (
            "An ML forecasting model supplements statistical baseline forecasts with leading indicator "
            "signals (sales pipeline, weather, macroeconomic indices, competitor promotions) to improve "
            "short-horizon accuracy and reduce safety stock requirements."
        ),
        "prerequisites": [
            "ERP/SCM with at least 2 years of demand history",
            "Sales team willing to share pipeline data as signal input",
            "S&OP process in place to consume forecast outputs",
        ],
        "expected_outcomes": [
            "Short-horizon forecast MAPE improved 15-30%",
            "Safety stock reduction 5-15%",
            "Stockout frequency reduced 10-20%",
        ],
        "implementation_effort": "medium",
        "timeline_to_value_weeks": 12,
        "applicable_industries": ["Manufacturing"],
        "applicable_sizes": ["Mid-Market", "Large", "Enterprise"],
        "disqualifying_conditions": [
            "Fewer than 50 active SKUs (insufficient for meaningful pattern learning)",
            "No historical demand data in structured form",
        ],
        "peer_examples": [
            "Consumer goods manufacturer reduced safety stock by $3.2M while improving fill rate",
            "Industrial equipment supplier improved MAPE by 22% in short-horizon horizon",
        ],
    },
]


def get_quick_wins_for_prospect(
    industry_label: str,
    size_band: str,
) -> List[Dict[str, Any]]:
    """Return filtered quick win candidates for a given industry and size band.

    Filtering logic:
    1. applicable_industries must include 'All' or match the prospect's industry
    2. applicable_sizes must include the prospect's size band

    Args:
        industry_label: Company industry label (e.g. 'Financial Services')
        size_band: Company size band (e.g. 'Mid-Market', 'Large', 'Enterprise')

    Returns:
        List of matching quick win pattern dicts
    """
    label_lower = industry_label.strip().lower()
    candidates = []

    for pattern in QUICK_WIN_PATTERNS:
        # Check industry match
        applicable = pattern["applicable_industries"]
        industry_match = "All" in applicable or any(
            ind.lower() in label_lower or label_lower in ind.lower()
            for ind in applicable
        )
        if not industry_match:
            continue

        # Check size band match
        size_match = size_band in pattern["applicable_sizes"]
        if not size_match:
            continue

        candidates.append(pattern)

    return candidates
