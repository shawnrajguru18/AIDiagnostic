"""Quick Wins Library for DXC AI Readiness Diagnostic V0.
Source: Companion 02 — Quick Win Pattern Library.

All 15 patterns (QW-001 through QW-015) with full field coverage.
Each entry is a dict compatible with the QuickWinPattern schema in
src.models.schemas.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Quick Win pattern library — 15 entries (QW-001 through QW-015)
# ---------------------------------------------------------------------------

QUICK_WIN_PATTERNS: List[Dict[str, Any]] = [

    # -------------------------------------------------------------------------
    # QW-001  Invoice & AP Automation
    # -------------------------------------------------------------------------
    {
        "pattern_id": "QW-001",
        "name": "Intelligent Invoice & Accounts-Payable Automation",
        "one_line_description": (
            "AI-powered document understanding extracts, validates, and routes "
            "supplier invoices end-to-end, slashing manual processing cost."
        ),
        "what_the_ai_does": (
            "A large language model with document-understanding capabilities reads "
            "incoming invoices (PDF, image, EDI) to extract header and line-item data, "
            "matches against POs and goods receipts in the ERP, flags exceptions, and "
            "routes for approval or straight-through payment — all without human keying."
        ),
        "prerequisites": [
            "ERP system with AP module (SAP, Oracle, Dynamics, or equivalent)",
            "Digitised invoice intake (email, portal, or scan)",
            "At least 12 months of historical invoice data for model tuning",
            "Executive sponsor in Finance",
        ],
        "expected_outcomes": [
            "70-85% reduction in manual data-entry FTE cost",
            "Invoice processing time from 5-8 days to under 4 hours",
            "Early-payment-discount capture improvement of 15-30%",
            "Error / duplicate payment rate reduction > 90%",
        ],
        "implementation_effort": "low",
        "timeline_to_value_weeks": 8,
        "applicable_industries": [
            "Financial Services",
            "Healthcare & Life Sciences",
            "Manufacturing",
            "Technology",
            "Retail",
            "Other",
        ],
        "applicable_sizes": ["Mid-Market", "Large", "Enterprise"],
        "disqualifying_conditions": [
            "Fewer than 200 invoices per month (ROI too low)",
            "No digital invoice channel — 100% paper-only with no scanning",
            "ERP replacement project in-flight that would invalidate integration",
        ],
        "peer_examples": [
            "Global manufacturer reduced AP team FTE from 42 to 11 after deployment",
            "Regional bank cut invoice cycle time from 9 days to 6 hours across 14 entities",
            "Healthcare system achieved $2.1M annual savings on a $0.4M implementation",
        ],
    },

    # -------------------------------------------------------------------------
    # QW-002  IT Incident Management Triage
    # -------------------------------------------------------------------------
    {
        "pattern_id": "QW-002",
        "name": "AI-Powered IT Incident Triage & Routing",
        "one_line_description": (
            "Automatically classify, prioritise, and route IT incidents to the right "
            "resolver group, cutting mean-time-to-assign and reducing misroutes."
        ),
        "what_the_ai_does": (
            "An NLP classification model reads incoming incident tickets (from ITSM "
            "tool like ServiceNow or Jira) and predicts the correct assignment group, "
            "priority, and category. A generative layer drafts an initial resolution "
            "suggestion by searching the knowledge base. The model continuously retrains "
            "on closure outcomes."
        ),
        "prerequisites": [
            "ITSM platform with API access (ServiceNow, Jira Service Management, BMC Helix)",
            "At least 10 000 historical resolved tickets for training",
            "Defined assignment group taxonomy (stable for 6+ months)",
        ],
        "expected_outcomes": [
            "Mean-time-to-assign reduction of 60-80%",
            "Misroute rate reduction from 25-40% to under 5%",
            "L1 auto-resolution rate improvement of 15-25 percentage points",
            "Analyst time on triage freed for higher-complexity work",
        ],
        "implementation_effort": "low",
        "timeline_to_value_weeks": 6,
        "applicable_industries": [
            "Financial Services",
            "Healthcare & Life Sciences",
            "Manufacturing",
            "Technology",
            "Retail",
            "Other",
        ],
        "applicable_sizes": ["Mid-Market", "Large", "Enterprise"],
        "disqualifying_conditions": [
            "Fewer than 500 incidents per month",
            "No structured ITSM tool — tickets managed via email or spreadsheet",
            "Assignment group taxonomy in active restructuring",
        ],
        "peer_examples": [
            "Fortune 500 retailer reduced misroutes by 78% and saved 4 FTE of triage effort",
            "Global bank cut MTTA from 47 min to 8 min across 3 service desks",
        ],
    },

    # -------------------------------------------------------------------------
    # QW-003  Customer Support Ticket Deflection
    # -------------------------------------------------------------------------
    {
        "pattern_id": "QW-003",
        "name": "AI Customer Support Ticket Deflection & Agent Assist",
        "one_line_description": (
            "Conversational AI deflects routine inquiries and equips human agents "
            "with real-time next-best-action guidance to cut handle time."
        ),
        "what_the_ai_does": (
            "A retrieval-augmented generation (RAG) layer over the knowledge base answers "
            "common customer questions via chat or email auto-reply. For escalated tickets, "
            "an agent-assist panel surfaces relevant articles, prior case resolutions, and "
            "a recommended response draft, reducing average handle time."
        ),
        "prerequisites": [
            "CRM or customer service platform (Salesforce Service Cloud, Zendesk, ServiceNow CSM)",
            "Structured knowledge base with 200+ articles",
            "12 months of resolved case history with outcomes",
            "Defined escalation taxonomy",
        ],
        "expected_outcomes": [
            "Tier-0 / self-service deflection rate of 20-40%",
            "Average handle time reduction 25-35%",
            "CSAT improvement of 8-12 points",
            "First-contact resolution improvement of 10-20 percentage points",
        ],
        "implementation_effort": "medium",
        "timeline_to_value_weeks": 10,
        "applicable_industries": [
            "Financial Services",
            "Healthcare & Life Sciences",
            "Manufacturing",
            "Technology",
            "Retail",
            "Other",
        ],
        "applicable_sizes": ["Mid-Market", "Large", "Enterprise"],
        "disqualifying_conditions": [
            "No structured knowledge base — institutional knowledge is entirely in agents' heads",
            "Highly regulated interaction types requiring verbatim scripted responses (e.g., collections)",
            "Contact volume < 1 000 contacts / month",
        ],
        "peer_examples": [
            "Telecom provider deflected 31% of tier-1 tickets, saving $3.2M annually",
            "Health insurer cut average handle time from 8.4 to 5.9 minutes",
        ],
    },

    # -------------------------------------------------------------------------
    # QW-004  Recruiting & HR Screening Automation
    # -------------------------------------------------------------------------
    {
        "pattern_id": "QW-004",
        "name": "AI-Assisted Recruiting & CV Screening",
        "one_line_description": (
            "AI screens and ranks inbound applications against job criteria, "
            "cutting time-to-shortlist and reducing recruiter workload."
        ),
        "what_the_ai_does": (
            "A structured extraction model parses CVs to produce standardised candidate "
            "profiles. A ranking model scores each candidate against job-requirement "
            "embeddings and past hire outcomes, producing a shortlist with explanations "
            "for recruiters. Bias auditing runs continuously on scoring distributions."
        ),
        "prerequisites": [
            "ATS platform (Workday, SuccessFactors, Greenhouse, Lever, or equivalent)",
            "Minimum 500 historical hires with outcome labels (hired / not hired / performance rating)",
            "Defined competency framework or job-requirement taxonomy",
            "Legal / HR sign-off on AI-assisted hiring policy",
        ],
        "expected_outcomes": [
            "Time-to-shortlist reduction of 50-70%",
            "Recruiter capacity freed: 30-45% more roles per recruiter",
            "Increase in diverse shortlist representation (when bias controls applied)",
            "Cost-per-hire reduction of 15-25%",
        ],
        "implementation_effort": "medium",
        "timeline_to_value_weeks": 12,
        "applicable_industries": [
            "Financial Services",
            "Healthcare & Life Sciences",
            "Manufacturing",
            "Technology",
            "Retail",
            "Other",
        ],
        "applicable_sizes": ["Mid-Market", "Large", "Enterprise"],
        "disqualifying_conditions": [
            "Fewer than 200 annual external hires (volume too low for model quality)",
            "ATS not available or being replaced",
            "Jurisdictions with strict AI-in-hiring prohibitions that have not been assessed",
        ],
        "peer_examples": [
            "Global professional services firm reduced shortlisting time from 12 days to 2.5 days",
            "Healthcare network increased diversity in shortlists by 22% with bias-aware scoring",
        ],
    },

    # -------------------------------------------------------------------------
    # QW-005  Claims Adjudication Automation (FS / HLS)
    # -------------------------------------------------------------------------
    {
        "pattern_id": "QW-005",
        "name": "AI-Assisted Claims Adjudication & Straight-Through Processing",
        "one_line_description": (
            "Machine learning classifies and auto-adjudicates routine insurance or "
            "healthcare claims, driving straight-through rates above 60%."
        ),
        "what_the_ai_does": (
            "A gradient-boosted classification model scores each incoming claim against "
            "policy rules, historical payout patterns, and fraud signals. Low-complexity "
            "claims with high confidence are straight-through processed; borderline "
            "claims are queued for human review with AI-generated rationale and suggested "
            "disposition. Anomaly detection flags potential fraud for SIU referral."
        ),
        "prerequisites": [
            "Claims management system with API or data export",
            "3+ years of adjudicated claim history with outcomes",
            "Digital FNOL or claim-intake channel",
            "Actuarial / compliance sign-off on auto-adjudication thresholds",
        ],
        "expected_outcomes": [
            "Straight-through processing rate: 55-70% of routine claims",
            "Claims processing cost reduction: 30-45%",
            "Cycle time reduction: from 8-15 days to under 24 hours for auto-adjudicated claims",
            "Fraud detection improvement: 20-35% more fraud caught at lower false-positive rate",
        ],
        "implementation_effort": "medium",
        "timeline_to_value_weeks": 14,
        "applicable_industries": ["Financial Services", "Healthcare & Life Sciences"],
        "applicable_sizes": ["Large", "Enterprise"],
        "disqualifying_conditions": [
            "No structured claims data — paper-based FNOL",
            "Fewer than 500 claims per month (model performance insufficient)",
            "Regulatory environment prohibits automated adjudication in this line of business",
            "Core system replacement in-flight",
        ],
        "peer_examples": [
            "Regional P&C insurer achieved 62% STP rate within 6 months, cutting unit cost by 38%",
            "Health plan reduced claims backlog by 70% and cut appeals rate by 18%",
        ],
    },

    # -------------------------------------------------------------------------
    # QW-006  Clinical Documentation AI Scribe (HLS)
    # -------------------------------------------------------------------------
    {
        "pattern_id": "QW-006",
        "name": "Ambient AI Clinical Documentation (AI Scribe)",
        "one_line_description": (
            "AI listens to physician-patient encounters and auto-drafts structured "
            "clinical notes, recovering 1-2 hours of physician time per day."
        ),
        "what_the_ai_does": (
            "A medical-grade speech recognition model transcribes the encounter audio. "
            "A clinical LLM extracts subjective, objective, assessment, and plan (SOAP) "
            "elements, maps to ICD-10/CPT codes, and generates a note draft in the EHR "
            "template format. The physician reviews and signs in under 3 minutes; "
            "corrections feed a continuous fine-tuning loop."
        ),
        "prerequisites": [
            "EHR system with FHIR API or equivalent integration capability",
            "HIPAA-compliant audio capture infrastructure (device or ambient mic)",
            "Physician champion and clinical informatics support",
            "Clinical validation and sign-off process for note drafts",
        ],
        "expected_outcomes": [
            "Documentation time reduction of 50-70% per encounter",
            "Physician after-hours charting (pajama time) eliminated or near-eliminated",
            "Physician burnout index improvement measurable within 90 days",
            "Coding accuracy improvement 15-25%; denial rate reduction 20-30%",
        ],
        "implementation_effort": "medium",
        "timeline_to_value_weeks": 12,
        "applicable_industries": ["Healthcare & Life Sciences"],
        "applicable_sizes": ["Mid-Market", "Large", "Enterprise"],
        "disqualifying_conditions": [
            "EHR does not support API integration and vendor refuses to allow it",
            "Physician group unwilling to pilot — no champion identified",
            "Audio capture not feasible due to facility constraints",
            "Non-English primary language with no supported ASR model",
        ],
        "peer_examples": [
            "Regional health system with 400 physicians recovered 800 physician-hours per week",
            "Academic medical centre reduced after-hours charting by 68% in 90-day pilot",
        ],
    },

    # -------------------------------------------------------------------------
    # QW-007  Enterprise Knowledge Assistant (RAG)
    # -------------------------------------------------------------------------
    {
        "pattern_id": "QW-007",
        "name": "Enterprise AI Knowledge Assistant (RAG-Based)",
        "one_line_description": (
            "A retrieval-augmented generation assistant gives employees instant, "
            "cited answers from internal knowledge bases, policies, and documents."
        ),
        "what_the_ai_does": (
            "A RAG pipeline indexes internal documentation (SharePoint, Confluence, "
            "policy libraries, SOPs, past project deliverables) into a vector store. "
            "Employee natural-language queries retrieve relevant chunks and an LLM "
            "synthesises a grounded answer with source citations. The assistant is "
            "embedded in Microsoft Teams, Slack, or the intranet portal."
        ),
        "prerequisites": [
            "Internal documentation available in digital form (PDF, Word, HTML, or Wiki)",
            "Collaboration platform with bot integration capability (Teams, Slack)",
            "IT security review and data classification of knowledge corpus",
            "Content owner engagement to maintain document freshness",
        ],
        "expected_outcomes": [
            "HR / IT tier-1 support ticket volume reduction of 25-40%",
            "Employee time-to-answer for internal questions: hours to minutes",
            "New employee onboarding time reduction of 20-30%",
            "Knowledge-worker productivity uplift of 15-25%",
        ],
        "implementation_effort": "low",
        "timeline_to_value_weeks": 8,
        "applicable_industries": [
            "Financial Services",
            "Healthcare & Life Sciences",
            "Manufacturing",
            "Technology",
            "Retail",
            "Other",
        ],
        "applicable_sizes": ["Mid-Market", "Large", "Enterprise"],
        "disqualifying_conditions": [
            "Critical knowledge exists only in people's heads — no written documentation",
            "Highly sensitive / classified documentation with no approved LLM hosting environment",
            "No collaboration platform — employees work via email only",
        ],
        "peer_examples": [
            "Professional services firm reduced policy-related queries to HR by 44%",
            "Manufacturing company cut new-hire time-to-productivity by 3 weeks",
        ],
    },

    # -------------------------------------------------------------------------
    # QW-008  Revenue Cycle Management Automation (HLS)
    # -------------------------------------------------------------------------
    {
        "pattern_id": "QW-008",
        "name": "AI-Driven Revenue Cycle Management & Denial Prevention",
        "one_line_description": (
            "Predictive models flag likely claim denials before submission and "
            "auto-correct coding errors, materially improving net collection rate."
        ),
        "what_the_ai_does": (
            "A pre-submission scrubbing model scores each claim for denial probability "
            "based on payer-specific rules, coding patterns, and historical denial reasons. "
            "High-risk claims are flagged for coder review with specific fix recommendations. "
            "Post-denial, an NLP model reads Explanation of Benefits (EOB) documents to "
            "categorise denial reason and route to the appropriate appeals workflow."
        ),
        "prerequisites": [
            "Practice management or hospital billing system (Epic, Cerner, Meditech, or equivalent)",
            "At least 18 months of claims submission and denial data",
            "Coding team willing to act on AI-generated flags",
            "Payer contract data accessible",
        ],
        "expected_outcomes": [
            "Clean claims rate improvement of 8-15 percentage points",
            "Denial rate reduction of 20-35%",
            "Days in AR reduction of 5-12 days",
            "Net collection rate improvement of 2-4 percentage points",
        ],
        "implementation_effort": "medium",
        "timeline_to_value_weeks": 14,
        "applicable_industries": ["Healthcare & Life Sciences"],
        "applicable_sizes": ["Mid-Market", "Large", "Enterprise"],
        "disqualifying_conditions": [
            "Fewer than 1 000 claims per month",
            "Billing done entirely by third-party RCM vendor with no system access",
            "EHR / billing system replacement planned within 12 months",
        ],
        "peer_examples": [
            "Community health system improved net collection by 3.2% ($4.8M) in year one",
            "Specialty practice reduced denial rate from 14% to 8% within 6 months",
        ],
    },

    # -------------------------------------------------------------------------
    # QW-009  Predictive Maintenance (MFG)
    # -------------------------------------------------------------------------
    {
        "pattern_id": "QW-009",
        "name": "Predictive Asset Maintenance & Failure Prevention",
        "one_line_description": (
            "Time-series anomaly detection on sensor data predicts equipment failures "
            "1-3 weeks in advance, preventing unplanned downtime."
        ),
        "what_the_ai_does": (
            "An LSTM or transformer model trained on historian / IoT sensor telemetry "
            "(vibration, temperature, pressure, current) identifies deviation patterns "
            "that precede known failure modes. Alerts are sent to the CMMS with a "
            "recommended maintenance action and parts list. Technician feedback on false "
            "positives continuously improves precision."
        ),
        "prerequisites": [
            "IoT sensors or historian data on critical assets (at least 18 months history)",
            "CMMS / EAM system (SAP PM, IBM Maximo, or equivalent) with API",
            "Defined critical asset list (top 20-50 assets by downtime impact)",
            "Maintenance engineering resource to validate alerts and provide feedback",
        ],
        "expected_outcomes": [
            "Unplanned downtime reduction of 20-40%",
            "Maintenance cost reduction of 10-25% (shift from corrective to predictive)",
            "Asset life extension of 15-20%",
            "Safety incident reduction correlated with equipment health",
        ],
        "implementation_effort": "medium",
        "timeline_to_value_weeks": 16,
        "applicable_industries": ["Manufacturing"],
        "applicable_sizes": ["Mid-Market", "Large", "Enterprise"],
        "disqualifying_conditions": [
            "No sensor data — assets have no instrumentation",
            "Insufficient failure history (fewer than 20 failure events per asset type)",
            "Assets near end-of-life with replacement planned within 18 months",
        ],
        "peer_examples": [
            "Auto manufacturer prevented 12 unplanned line stoppages in year one ($18M value)",
            "Chemical plant reduced maintenance spend by 22% while improving OEE by 6%",
        ],
    },

    # -------------------------------------------------------------------------
    # QW-010  Code Acceleration / Developer Productivity
    # -------------------------------------------------------------------------
    {
        "pattern_id": "QW-010",
        "name": "AI-Powered Developer Productivity (Code Acceleration)",
        "one_line_description": (
            "AI code assistants integrated into the development workflow accelerate "
            "feature delivery, reduce defects, and cut code review time."
        ),
        "what_the_ai_does": (
            "A code-generation model (e.g., GitHub Copilot, Amazon CodeWhisperer, or "
            "internally hosted equivalent) is integrated into developer IDEs and CI/CD "
            "pipelines. It suggests code completions, generates unit tests, explains "
            "legacy code, and flags security vulnerabilities. A metrics layer tracks "
            "acceptance rate, throughput, and defect density to quantify productivity gains."
        ),
        "prerequisites": [
            "Modern IDE environment (VS Code, JetBrains, or equivalent)",
            "Version control system with CI/CD pipeline",
            "Developer willingness to adopt AI tooling (culture of experimentation helpful)",
            "Security review of code-assistant tool data-handling (especially for proprietary IP)",
        ],
        "expected_outcomes": [
            "Developer throughput increase of 20-40% (lines of accepted code / sprint)",
            "Unit test coverage improvement of 15-30 percentage points",
            "Code review cycle time reduction of 25-35%",
            "Developer satisfaction / retention improvement measurable in engagement surveys",
        ],
        "implementation_effort": "low",
        "timeline_to_value_weeks": 4,
        "applicable_industries": [
            "Financial Services",
            "Healthcare & Life Sciences",
            "Manufacturing",
            "Technology",
            "Retail",
            "Other",
        ],
        "applicable_sizes": ["SMB", "Mid-Market", "Large", "Enterprise"],
        "disqualifying_conditions": [
            "Proprietary codebase with extreme IP sensitivity and no approved on-premises LLM option",
            "Development team of fewer than 5 engineers (ROI threshold not met)",
            "Waterfall process with no iterative delivery cycles",
        ],
        "peer_examples": [
            "SaaS company increased feature delivery velocity by 34% within 60 days of rollout",
            "Financial services firm reduced time-to-merge PRs by 28% across 600 engineers",
        ],
    },

    # -------------------------------------------------------------------------
    # QW-011  Fraud Detection Enhancement (FS)
    # -------------------------------------------------------------------------
    {
        "pattern_id": "QW-011",
        "name": "Real-Time Transaction Fraud Detection Enhancement",
        "one_line_description": (
            "Graph neural network and anomaly detection models improve fraud catch rate "
            "while cutting false positives that frustrate good customers."
        ),
        "what_the_ai_does": (
            "A graph neural network models relationships between accounts, devices, "
            "and merchants to detect rings and mule networks invisible to rule-based "
            "systems. A streaming anomaly model scores each transaction within 50 ms "
            "for real-time decisioning. The combined output feeds the existing fraud "
            "operations queue, prioritised by model confidence, reducing analyst review "
            "workload while catching more fraud."
        ),
        "prerequisites": [
            "Transaction data stream (real-time or near-real-time event feed)",
            "Case management system with analyst feedback loop",
            "At least 24 months of labelled fraud / non-fraud transaction history",
            "MLOps infrastructure for low-latency model serving (< 100 ms SLA)",
        ],
        "expected_outcomes": [
            "Fraud catch rate improvement of 20-35% vs. rule-based baseline",
            "False positive rate reduction of 40-60%",
            "Customer friction events (false declines) reduction of 30-50%",
            "Analyst review queue reduction enabling same headcount to cover higher volumes",
        ],
        "implementation_effort": "high",
        "timeline_to_value_weeks": 20,
        "applicable_industries": ["Financial Services"],
        "applicable_sizes": ["Large", "Enterprise"],
        "disqualifying_conditions": [
            "Transaction volume < 50 000 / month (insufficient for graph model quality)",
            "No real-time transaction event stream — batch-only fraud detection",
            "Existing fraud model recently replaced (< 12 months ago) with strong performance",
        ],
        "peer_examples": [
            "Regional bank reduced fraud losses by 28% while cutting false positives by 51%",
            "Payments processor caught $12M in additional fraud in first year post-deployment",
        ],
    },

    # -------------------------------------------------------------------------
    # QW-012  Regulatory Reporting Automation (FS)
    # -------------------------------------------------------------------------
    {
        "pattern_id": "QW-012",
        "name": "AI-Assisted Regulatory Report Generation & Validation",
        "one_line_description": (
            "LLM-assisted report generation and validation cuts regulatory reporting "
            "cycle time and reduces manual error rates for Basel, DORA, and IFRS9 filings."
        ),
        "what_the_ai_does": (
            "A pipeline extracts data from the regulatory data mart, applies "
            "business logic, and uses an LLM to generate narrative sections of reports. "
            "A validation agent cross-checks calculated figures against prior periods "
            "and known regulatory thresholds, flagging anomalies with explanations "
            "before human review. Digital signatures and audit trail are automated."
        ),
        "prerequisites": [
            "Regulatory data mart or data warehouse with clean, reconciled source data",
            "Regulatory report templates in machine-readable format",
            "Internal controls and sign-off workflow defined",
            "Compliance team willing to review AI-generated drafts",
        ],
        "expected_outcomes": [
            "Report preparation cycle time reduction of 50-70%",
            "Manual error rate reduction > 80%",
            "Compliance analyst capacity freed for interpretation vs. data collection",
            "Full audit trail with automated evidence linking",
        ],
        "implementation_effort": "medium",
        "timeline_to_value_weeks": 16,
        "applicable_industries": ["Financial Services"],
        "applicable_sizes": ["Large", "Enterprise"],
        "disqualifying_conditions": [
            "Regulatory data mart does not exist — data sourced manually from 20+ systems",
            "Regulatory requirements in active change (transition year for new standard)",
            "Fewer than 5 regulatory reports per year (insufficient ROI)",
        ],
        "peer_examples": [
            "European bank reduced COREP/FINREP production effort by 62% across 8 legal entities",
            "US broker-dealer cut FR Y-9C preparation from 6 weeks to 10 business days",
        ],
    },

    # -------------------------------------------------------------------------
    # QW-013  Supply Chain Demand Forecasting (MFG / Retail)
    # -------------------------------------------------------------------------
    {
        "pattern_id": "QW-013",
        "name": "AI-Powered Supply Chain Demand Forecasting",
        "one_line_description": (
            "Probabilistic ML forecasting incorporating external signals improves "
            "forecast accuracy by 20-35%, reducing inventory costs and stockouts."
        ),
        "what_the_ai_does": (
            "An ensemble of gradient-boosting and deep learning time-series models "
            "ingests historical sales/shipment data alongside external signals (weather, "
            "economic indicators, promotions, competitor events). Probabilistic output "
            "provides confidence intervals that drive inventory safety-stock calculations "
            "in the ERP / SCM system, replacing static Excel-based consensus forecasts."
        ),
        "prerequisites": [
            "ERP or SCM system with demand / shipment history (3+ years preferred)",
            "Data pipeline for external signal ingestion",
            "Demand planning team willing to adopt probabilistic outputs",
            "SKU / product hierarchy cleaned and maintained",
        ],
        "expected_outcomes": [
            "Forecast MAPE improvement of 20-35%",
            "Inventory carrying cost reduction of 10-20%",
            "Stockout event frequency reduction of 15-30%",
            "Planner time shifted to exception management vs. forecast building",
        ],
        "implementation_effort": "medium",
        "timeline_to_value_weeks": 16,
        "applicable_industries": ["Manufacturing", "Retail"],
        "applicable_sizes": ["Mid-Market", "Large", "Enterprise"],
        "disqualifying_conditions": [
            "Fewer than 24 months of demand history",
            "Product catalogue turning over > 50% annually (insufficient history per SKU)",
            "Single-product or extremely low-SKU count (fewer than 50 SKUs)",
        ],
        "peer_examples": [
            "Consumer goods manufacturer reduced inventory by $24M while improving fill rate by 4%",
            "Pharmaceutical distributor cut stockouts by 28% for critical drug categories",
        ],
    },

    # -------------------------------------------------------------------------
    # QW-014  Contract Intelligence & Risk Review
    # -------------------------------------------------------------------------
    {
        "pattern_id": "QW-014",
        "name": "AI Contract Intelligence & Risk Review Automation",
        "one_line_description": (
            "LLM-powered contract analysis extracts key terms, flags non-standard "
            "clauses, and surfaces risk signals, cutting legal review time by 60-70%."
        ),
        "what_the_ai_does": (
            "An LLM with document-understanding capability reads incoming contracts "
            "(supplier agreements, customer MSAs, NDAs) to extract structured metadata "
            "(parties, term, renewal, payment, liability caps, IP ownership, data-sharing "
            "clauses). A risk-scoring model flags deviations from standard playbook "
            "positions. Output is a structured review summary that legal counsel can "
            "approve or escalate in minutes rather than hours."
        ),
        "prerequisites": [
            "Contract repository or CLM system with digital contract storage",
            "Standard contract playbook or clause library defined",
            "Legal team buy-in and willingness to review AI output",
            "At least 500 executed contracts for pattern extraction",
        ],
        "expected_outcomes": [
            "Contract review time reduction of 60-75%",
            "Non-standard clause detection rate improvement > 90%",
            "Contract cycle time (request to signed) reduction of 25-40%",
            "Legal spend reduction or redeployment to higher-value advisory work",
        ],
        "implementation_effort": "low",
        "timeline_to_value_weeks": 10,
        "applicable_industries": [
            "Financial Services",
            "Healthcare & Life Sciences",
            "Manufacturing",
            "Technology",
            "Retail",
            "Other",
        ],
        "applicable_sizes": ["Mid-Market", "Large", "Enterprise"],
        "disqualifying_conditions": [
            "Contracts primarily in non-English languages with no supported model",
            "Contract repository entirely paper-based with no scanning infrastructure",
            "Legal function is fully outsourced with no internal counsel",
        ],
        "peer_examples": [
            "Global technology company reduced NDA review from 3 days to 45 minutes",
            "Manufacturing firm identified $8M in under-invoiced customer contracts during backlog review",
        ],
    },

    # -------------------------------------------------------------------------
    # QW-015  AI-Augmented Sales Prospecting & Lead Scoring
    # -------------------------------------------------------------------------
    {
        "pattern_id": "QW-015",
        "name": "AI-Augmented Sales Prospecting & Propensity-to-Buy Lead Scoring",
        "one_line_description": (
            "Propensity models score and prioritise leads by purchase likelihood, "
            "boosting conversion rates and reducing wasted sales effort."
        ),
        "what_the_ai_does": (
            "A gradient-boosting model trained on CRM history, firmographic data, "
            "intent signals (web visits, content downloads, event attendance), and "
            "external data (news, job postings, tech stack signals) scores each account "
            "and contact for propensity to buy, upsell, or churn. Sales reps see a "
            "daily prioritised call / email list with AI-generated talking points and "
            "relevance rationale. The model retrains monthly on closed-won / lost outcomes."
        ),
        "prerequisites": [
            "CRM system with at least 24 months of opportunity history and outcomes",
            "Marketing automation platform with engagement signals",
            "Sales leadership commitment to adopting model-driven prioritisation",
            "Third-party firmographic / intent data feed (ZoomInfo, Bombora, or equivalent)",
        ],
        "expected_outcomes": [
            "Lead-to-opportunity conversion rate improvement of 15-30%",
            "Sales cycle length reduction of 10-20%",
            "Revenue per sales rep improvement of 12-25%",
            "Churn early-warning enabling retention intervention 60-90 days earlier",
        ],
        "implementation_effort": "medium",
        "timeline_to_value_weeks": 12,
        "applicable_industries": [
            "Financial Services",
            "Healthcare & Life Sciences",
            "Manufacturing",
            "Technology",
            "Retail",
            "Other",
        ],
        "applicable_sizes": ["Mid-Market", "Large", "Enterprise"],
        "disqualifying_conditions": [
            "Fewer than 500 closed opportunities in CRM history",
            "CRM data quality severely degraded (> 40% missing or inaccurate key fields)",
            "Sales process entirely relationship / referral based with no outbound motion",
        ],
        "peer_examples": [
            "B2B software company improved pipeline creation by 38% within one quarter",
            "Financial services firm reduced churn by 22% by acting on early-warning scores",
        ],
    },
]


# ---------------------------------------------------------------------------
# Accessor functions
# ---------------------------------------------------------------------------


def get_quick_wins_library() -> List[Dict[str, Any]]:
    """Return the complete list of 15 Quick Win patterns."""
    return list(QUICK_WIN_PATTERNS)


def get_quick_win_by_id(pattern_id: str) -> Optional[Dict[str, Any]]:
    """Return a single Quick Win pattern by pattern_id, or None if not found."""
    for pattern in QUICK_WIN_PATTERNS:
        if pattern["pattern_id"] == pattern_id:
            return pattern
    return None


def get_quick_wins_for_prospect(
    industry_label: str,
    size_band: str,
) -> List[Dict[str, Any]]:
    """Return filtered quick win candidates for a given industry and size band.

    Args:
        industry_label: Company industry label (e.g. 'Financial Services')
        size_band: Company size band (e.g. 'Mid-Market', 'Large', 'Enterprise')

    Returns:
        List of matching quick win pattern dicts, ordered by timeline_to_value_weeks.
    """
    label_lower = industry_label.strip().lower()
    candidates = []

    for pattern in QUICK_WIN_PATTERNS:
        applicable = pattern["applicable_industries"]
        industry_match = any(
            ind.lower() in label_lower or label_lower in ind.lower()
            for ind in applicable
        )
        if not industry_match:
            continue

        size_match = size_band in pattern["applicable_sizes"]
        if not size_match:
            continue

        candidates.append(pattern)

    return sorted(candidates, key=lambda p: p["timeline_to_value_weeks"])
