"""
Pydantic V2 models for the DXC AI Readiness Diagnostic V0.
Translates TypeScript interfaces from Companion 05.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Primitives / enumerations
# ---------------------------------------------------------------------------

Confidence = Literal["high", "medium", "low"]

ConfidenceTier = Literal["confirmed", "probable", "possible", "not_detected"]

Persona = Literal["P1", "P2", "P3"]

DimensionId = Literal[
    "data_foundation",
    "governance_posture",
    "ai_investment_maturity",
    "org_change_readiness",
    "value_pocket_clarity",
    "regulatory_complexity",
]

Tier = Literal["Emerging", "Developing", "Established", "Leading"]

SizeBand = Literal["SMB", "Mid-Market", "Large", "Enterprise"]

Industry = Literal[
    "Financial Services",
    "Healthcare & Life Sciences",
    "Manufacturing",
    "Technology",
    "Retail",
    "Other",
]

Geography = Literal["US", "EU", "APAC", "UK", "LATAM", "MEA", "Global"]

ProcessingStatus = Literal[
    "pending",
    "running",
    "completed",
    "failed",
    "awaiting_partner_review",
]


# ---------------------------------------------------------------------------
# Audit / Consent
# ---------------------------------------------------------------------------


class AuditMetadata(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str = "system"
    version: str = "1.0"


class ConsentRecord(BaseModel):
    consent_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    prospect_id: str
    consent_given: bool
    consent_timestamp: datetime = Field(default_factory=datetime.utcnow)
    consent_version: str = "1.0"
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    data_retention_days: int = 90
    marketing_opt_in: bool = False


# ---------------------------------------------------------------------------
# Prospect
# ---------------------------------------------------------------------------


class Prospect(BaseModel):
    prospect_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    company_name: str
    industry: Industry
    size_band: SizeBand
    geography: Geography
    primary_contact_name: Optional[str] = None
    primary_contact_email: Optional[str] = None
    primary_contact_title: Optional[str] = None
    partner_id: Optional[str] = None
    partner_name: Optional[str] = None
    session_token: str = Field(default_factory=lambda: str(uuid.uuid4()))
    processing_status: ProcessingStatus = "pending"
    persona: Optional[Persona] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    audit: AuditMetadata = Field(default_factory=AuditMetadata)


# ---------------------------------------------------------------------------
# Persona Inference
# ---------------------------------------------------------------------------


class Concern(BaseModel):
    concern_id: str
    description: str
    weight: float = Field(ge=0.0, le=1.0)


class PersonaInference(BaseModel):
    inference_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    prospect_id: str
    assigned_persona: Persona
    confidence: Confidence
    reasoning: str
    title_signals: List[str] = Field(default_factory=list)
    industry_signals: List[str] = Field(default_factory=list)
    primary_concerns: List[Concern] = Field(default_factory=list)
    inferred_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Questionnaire
# ---------------------------------------------------------------------------


class QuestionOption(BaseModel):
    option_id: str  # "A", "B", "C", "D", etc.
    label: str
    score: Optional[int] = None  # None for informational/regulatory options
    description: Optional[str] = None


class ScaleAnchor(BaseModel):
    value: int
    label: str
    score: int


class QuestionPoolEntry(BaseModel):
    question_id: str  # e.g. "Q1.1"
    dimension_id: DimensionId
    question_text: str
    question_type: Literal["single_select", "multi_select", "scale_1_5", "open_short"]
    weight: float = Field(ge=0.0, le=1.0)
    options: Optional[List[QuestionOption]] = None
    scale_anchors: Optional[List[ScaleAnchor]] = None
    max_chars: Optional[int] = None  # for open_short
    persona_tags: Optional[List[Persona]] = None  # None = all personas
    industry_tags: Optional[List[str]] = None  # None = all industries
    skip_logic: Optional[Dict[str, Any]] = None  # condition -> skip target
    branching_logic: Optional[Dict[str, Any]] = None
    helper_text: Optional[str] = None
    persona_variant_text: Optional[Dict[str, str]] = None  # persona -> alt question text


class PersonalizedQuestion(BaseModel):
    question_id: str
    question_text: str  # may be persona-adapted
    question_type: Literal["single_select", "multi_select", "scale_1_5", "open_short"]
    weight: float
    dimension_id: DimensionId
    options: Optional[List[QuestionOption]] = None
    scale_anchors: Optional[List[ScaleAnchor]] = None
    max_chars: Optional[int] = None
    helper_text: Optional[str] = None
    skip_logic: Optional[Dict[str, Any]] = None


class PersonalizedQuestionnaire(BaseModel):
    questionnaire_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    prospect_id: str
    persona: Persona
    questions: List[PersonalizedQuestion]
    total_questions: int
    estimated_minutes: int
    generated_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Questionnaire Responses
# ---------------------------------------------------------------------------


class QuestionResponse(BaseModel):
    question_id: str
    dimension_id: DimensionId
    answer_type: Literal["single_select", "multi_select", "scale_1_5", "open_short"]
    # Union-style: one of these will be populated
    selected_option: Optional[str] = None  # option_id for single_select
    selected_options: Optional[List[str]] = None  # option_ids for multi_select
    scale_value: Optional[int] = None  # 1-5 for scale_1_5
    open_text: Optional[str] = None  # text for open_short
    score: Optional[int] = None  # computed score
    answered_at: datetime = Field(default_factory=datetime.utcnow)
    skipped: bool = False
    skip_reason: Optional[str] = None


class QuestionnaireResponse(BaseModel):
    response_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    prospect_id: str
    questionnaire_id: str
    responses: List[QuestionResponse]
    completed: bool = False
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    time_to_complete_seconds: Optional[int] = None


# ---------------------------------------------------------------------------
# Financial Research (B1)
# ---------------------------------------------------------------------------


class MAEvent(BaseModel):
    event_type: Literal["merger", "acquisition", "divestiture", "ipo", "partnership"]
    description: str
    date: Optional[str] = None
    value_usd_millions: Optional[float] = None
    counterparty: Optional[str] = None


class Source(BaseModel):
    source_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_type: Literal["sec_filing", "news", "press_release", "earnings_call", "analyst_report", "web"]
    url: Optional[str] = None
    title: Optional[str] = None
    published_date: Optional[str] = None
    relevance_score: Optional[float] = None


class FinancialResearch(BaseModel):
    research_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    prospect_id: str
    ticker: Optional[str] = None
    revenue_usd_millions: Optional[float] = None
    employee_count: Optional[int] = None
    recent_ma_events: List[MAEvent] = Field(default_factory=list)
    ai_mentions_in_filings: int = 0
    capex_trend: Optional[Literal["increasing", "stable", "decreasing"]] = None
    digital_transformation_signals: List[str] = Field(default_factory=list)
    sources: List[Source] = Field(default_factory=list)
    confidence: Confidence = "medium"
    researched_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# News Research (B2)
# ---------------------------------------------------------------------------


class AINewsSignal(BaseModel):
    signal_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    headline: str
    summary: str
    url: Optional[str] = None
    published_date: Optional[str] = None
    signal_type: Literal[
        "ai_investment",
        "ai_leadership_hire",
        "ai_product_launch",
        "regulatory_action",
        "competitor_move",
        "partnership",
        "risk_event",
    ]
    sentiment: Literal["positive", "neutral", "negative"] = "neutral"
    relevance_score: float = Field(default=0.5, ge=0.0, le=1.0)


class NewsResearch(BaseModel):
    research_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    prospect_id: str
    ai_signals: List[AINewsSignal] = Field(default_factory=list)
    competitor_mentions: List[str] = Field(default_factory=list)
    regulatory_mentions: List[str] = Field(default_factory=list)
    overall_ai_narrative: Optional[str] = None
    sources: List[Source] = Field(default_factory=list)
    researched_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Tech Stack Inference (B3)
# ---------------------------------------------------------------------------


class PlatformDetected(BaseModel):
    platform_name: str
    category: Literal[
        "cloud",
        "erp",
        "crm",
        "data_warehouse",
        "ml_platform",
        "rpa",
        "collaboration",
        "analytics",
        "other",
    ]
    confidence_tier: ConfidenceTier
    evidence: List[str] = Field(default_factory=list)
    ai_readiness_signal: Optional[str] = None


class TechStackInference(BaseModel):
    inference_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    prospect_id: str
    platforms_detected: List[PlatformDetected] = Field(default_factory=list)
    cloud_maturity: Literal["none", "basic", "intermediate", "advanced"] = "basic"
    data_platform_maturity: Literal["none", "basic", "intermediate", "advanced"] = "basic"
    existing_ai_tools: List[str] = Field(default_factory=list)
    tech_debt_signals: List[str] = Field(default_factory=list)
    overall_tech_readiness: Confidence = "medium"
    inferred_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Competitor Intelligence
# ---------------------------------------------------------------------------


class CompetitorAssessment(BaseModel):
    competitor_name: str
    ai_maturity_estimate: Literal["behind", "similar", "ahead", "unknown"] = "unknown"
    notable_ai_initiatives: List[str] = Field(default_factory=list)
    sources: List[str] = Field(default_factory=list)


class CompetitorIntelligence(BaseModel):
    intelligence_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    prospect_id: str
    industry: str
    competitors_assessed: List[CompetitorAssessment] = Field(default_factory=list)
    industry_ai_adoption_level: Literal["early", "growing", "mainstream", "advanced"] = "growing"
    competitive_pressure_narrative: Optional[str] = None
    researched_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Regulatory Context
# ---------------------------------------------------------------------------


class RegulatoryFramework(BaseModel):
    framework_id: str
    framework_name: str
    jurisdiction: str
    ai_specific: bool = False
    compliance_complexity: Literal["low", "medium", "high"] = "medium"
    key_requirements: List[str] = Field(default_factory=list)


class RegulatoryDevelopment(BaseModel):
    title: str
    description: str
    effective_date: Optional[str] = None
    impact_level: Literal["low", "medium", "high"] = "medium"
    url: Optional[str] = None


class HighRiskUseCase(BaseModel):
    use_case: str
    risk_rationale: str
    applicable_frameworks: List[str] = Field(default_factory=list)
    mitigation_requirements: List[str] = Field(default_factory=list)


class RegulatoryContext(BaseModel):
    context_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    prospect_id: str
    applicable_frameworks: List[RegulatoryFramework] = Field(default_factory=list)
    recent_developments: List[RegulatoryDevelopment] = Field(default_factory=list)
    high_risk_use_cases: List[HighRiskUseCase] = Field(default_factory=list)
    data_sovereignty_constraints: Optional[str] = None
    cross_border_implications: Optional[str] = None
    overall_regulatory_burden: Literal["low", "medium", "high", "very_high"] = "medium"
    analyzed_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Industry Library
# ---------------------------------------------------------------------------


class SubProcess(BaseModel):
    sub_process_id: str
    sub_process_name: str
    value_pocket_sizing: str  # e.g. "High", "Medium", "$X-Y per year"
    reinvention_archetype: str
    ai_pattern_description: str
    applicable_ai_patterns: List[str] = Field(default_factory=list)


class IndustryLibraryApplication(BaseModel):
    application_id: str
    application_name: str
    ai_approach: str
    expected_benefit: str
    implementation_complexity: Literal["low", "medium", "high"] = "medium"


class IndustryLibraryEntry(BaseModel):
    process_id: str
    process_name: str
    tier: Literal[1, 2, 3]
    industries_applicable: List[str]
    sub_processes: List[SubProcess]
    prerequisites: List[str] = Field(default_factory=list)
    typical_outcomes_when_done_well: List[str] = Field(default_factory=list)
    applications: List[IndustryLibraryApplication] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Synthesis Output (C2)
# ---------------------------------------------------------------------------


class DimensionScore(BaseModel):
    dimension_id: DimensionId
    dimension_name: str
    weight: float
    raw_score: float = Field(ge=0.0, le=100.0)
    weighted_score: float
    confidence: Confidence
    questions_answered: int
    questions_skipped: int
    key_signals: List[str] = Field(default_factory=list)


DimensionScores = Dict[str, DimensionScore]


class Finding(BaseModel):
    finding_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    dimension_id: DimensionId
    finding_type: Literal["strength", "gap", "risk", "opportunity"]
    severity: Literal["critical", "major", "moderate", "minor"] = "moderate"
    headline: str
    narrative: str
    evidence: List[str] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)


class ValueDifficultyMapping(BaseModel):
    dimension: str
    value_score: float = Field(ge=0.0, le=10.0)
    difficulty_score: float = Field(ge=0.0, le=10.0)
    label: str


class RecommendedNextStep(BaseModel):
    step_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    step_type: Literal[
        "apr_discovery",
        "governance_workshop",
        "data_assessment",
        "pilot_project",
        "executive_briefing",
        "roadmap_workshop",
    ]
    target_timeline: str
    dxc_practice: str
    estimated_value: Optional[str] = None
    prerequisites: List[str] = Field(default_factory=list)
    contact_role: Optional[str] = None


class PartnerAttentionFlag(BaseModel):
    flag_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    flag_type: Literal["upsell", "risk", "competitive", "timing", "relationship"]
    headline: str
    detail: str
    priority: Literal["high", "medium", "low"] = "medium"
    suggested_action: Optional[str] = None


class SynthesisOutput(BaseModel):
    synthesis_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    prospect_id: str
    overall_score: float = Field(ge=0.0, le=100.0)
    tier: Tier
    dimension_scores: DimensionScores
    findings: List[Finding]
    value_difficulty_map: List[ValueDifficultyMapping] = Field(default_factory=list)
    recommended_next_step: RecommendedNextStep
    partner_attention_flags: List[PartnerAttentionFlag] = Field(default_factory=list)
    executive_narrative: str
    synthesized_at: datetime = Field(default_factory=datetime.utcnow)
    model_used: str = "claude-opus-4-7"
    confidence: Confidence = "high"


# ---------------------------------------------------------------------------
# Quick Wins Output
# ---------------------------------------------------------------------------


class PrerequisiteCheck(BaseModel):
    prerequisite: str
    met: bool
    evidence: Optional[str] = None


class SelectedQuickWin(BaseModel):
    pattern_id: str
    name: str
    one_line_description: str
    rank: int
    selection_rationale: str
    prerequisite_checks: List[PrerequisiteCheck] = Field(default_factory=list)
    all_prerequisites_met: bool = True
    estimated_timeline_weeks: int
    estimated_roi_narrative: Optional[str] = None
    dxc_practice_owner: Optional[str] = None


class QuickWinPattern(BaseModel):
    pattern_id: str
    name: str
    one_line_description: str
    what_the_ai_does: str
    prerequisites: List[str]
    expected_outcomes: List[str]
    implementation_effort: Literal["low", "medium", "high"]
    timeline_to_value_weeks: int
    applicable_industries: List[str]
    applicable_sizes: List[SizeBand]
    disqualifying_conditions: List[str]
    peer_examples: List[str]


class QuickWinsOutput(BaseModel):
    output_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    prospect_id: str
    selected_quick_wins: List[SelectedQuickWin]
    total_candidates_evaluated: int
    selection_rationale_summary: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Scorecard Output
# ---------------------------------------------------------------------------


class DimensionDetail(BaseModel):
    dimension_id: DimensionId
    dimension_name: str
    score: float
    tier_label: str
    narrative: str
    key_strengths: List[str] = Field(default_factory=list)
    key_gaps: List[str] = Field(default_factory=list)
    weight: float


class ScorecardContent(BaseModel):
    overall_score: float
    tier: Tier
    dimension_details: List[DimensionDetail]
    findings_summary: List[Finding]
    recommended_next_step: RecommendedNextStep
    executive_narrative: str
    partner_attention_flags: List[PartnerAttentionFlag] = Field(default_factory=list)


class QuickWinsMemoContent(BaseModel):
    selected_quick_wins: List[SelectedQuickWin]
    executive_summary: str
    implementation_roadmap: Optional[str] = None


class FindingsAppendixContent(BaseModel):
    detailed_findings: List[Finding]
    methodology_note: str
    data_sources_used: List[str]
    confidence_statements: List[str]


class ScorecardOutput(BaseModel):
    output_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    prospect_id: str
    scorecard_content: ScorecardContent
    quick_wins_memo_content: QuickWinsMemoContent
    findings_appendix_content: FindingsAppendixContent
    scorecard_pdf_url: Optional[str] = None
    quick_wins_memo_pdf_url: Optional[str] = None
    findings_appendix_pdf_url: Optional[str] = None
    generated_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Validation Output
# ---------------------------------------------------------------------------


class ValidationFlag(BaseModel):
    flag_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    flag_type: Literal[
        "contradictory_responses",
        "incomplete_dimension",
        "outlier_score",
        "low_confidence_research",
        "regulatory_mismatch",
        "persona_mismatch",
    ]
    dimension_affected: Optional[DimensionId] = None
    description: str
    severity: Literal["blocking", "warning", "info"] = "warning"
    suggested_resolution: Optional[str] = None


class ConfidenceAdjustment(BaseModel):
    dimension_id: DimensionId
    original_score: float
    adjusted_score: float
    adjustment_rationale: str
    adjustment_magnitude: float  # +/- points


class ValidationOutput(BaseModel):
    validation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    prospect_id: str
    validation_flags: List[ValidationFlag] = Field(default_factory=list)
    confidence_adjustments: List[ConfidenceAdjustment] = Field(default_factory=list)
    overall_validation_passed: bool = True
    blocking_issues: List[str] = Field(default_factory=list)
    validated_at: datetime = Field(default_factory=datetime.utcnow)
    model_used: str = "claude-haiku-4-5-20251001"


# ---------------------------------------------------------------------------
# Partner Review
# ---------------------------------------------------------------------------


class PartnerActionAddNote(BaseModel):
    action_type: Literal["add_note"] = "add_note"
    note_text: str
    note_category: Optional[str] = None


class PartnerActionAdjustScore(BaseModel):
    action_type: Literal["adjust_score"] = "adjust_score"
    dimension_id: DimensionId
    original_score: float
    adjusted_score: float
    justification: str


class PartnerActionApprove(BaseModel):
    action_type: Literal["approve"] = "approve"
    approved_at: datetime = Field(default_factory=datetime.utcnow)
    approval_comment: Optional[str] = None


class PartnerActionRequestRevision(BaseModel):
    action_type: Literal["request_revision"] = "request_revision"
    revision_reason: str
    specific_sections: List[str] = Field(default_factory=list)


# Union type for partner actions
PartnerAction = Union[
    PartnerActionAddNote,
    PartnerActionAdjustScore,
    PartnerActionApprove,
    PartnerActionRequestRevision,
]


class TrainingSignal(BaseModel):
    signal_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    signal_type: Literal[
        "score_correction",
        "finding_edit",
        "quick_win_rerank",
        "narrative_rewrite",
        "flag_dismissed",
    ]
    original_value: Any
    corrected_value: Any
    context: Optional[str] = None
    captured_at: datetime = Field(default_factory=datetime.utcnow)


class PartnerReviewRecord(BaseModel):
    review_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    prospect_id: str
    partner_id: str
    partner_name: Optional[str] = None
    status: Literal["pending", "in_review", "approved", "revision_requested"] = "pending"
    actions: List[PartnerAction] = Field(default_factory=list)
    training_signals: List[TrainingSignal] = Field(default_factory=list)
    review_started_at: Optional[datetime] = None
    review_completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Cross-Practice Routing
# ---------------------------------------------------------------------------


class PracticeOpportunityRecord(BaseModel):
    opportunity_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    practice_name: str
    opportunity_type: str
    description: str
    estimated_value_band: Optional[str] = None
    urgency: Literal["immediate", "near_term", "long_term"] = "near_term"
    contact_suggested: Optional[str] = None


class CrossPracticeRouting(BaseModel):
    routing_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    prospect_id: str
    primary_practice: str
    practice_opportunities: List[PracticeOpportunityRecord] = Field(default_factory=list)
    routing_rationale: str
    routed_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Benchmarking
# ---------------------------------------------------------------------------


class BenchmarkRecord(BaseModel):
    record_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    industry: str
    size_band: SizeBand
    geography: Geography
    dimension_id: DimensionId
    score: float
    tier: Tier
    quarter: str  # e.g. "2025-Q1"
    partner_id: Optional[str] = None  # anonymized
    contributed_at: datetime = Field(default_factory=datetime.utcnow)


class BenchmarkContribution(BaseModel):
    contribution_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    prospect_id: str
    records: List[BenchmarkRecord]
    consent_given: bool = False
    contributed_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Feedstock
# ---------------------------------------------------------------------------


class FeedstockRecord(BaseModel):
    record_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    prospect_id: str
    record_type: Literal[
        "questionnaire_response",
        "partner_correction",
        "validation_flag",
        "synthesis_output",
        "quick_wins_selection",
    ]
    data: Dict[str, Any]
    quality_score: Optional[float] = None
    usable_for_training: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)


class FeedstockOutput(BaseModel):
    output_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    prospect_id: str
    records: List[FeedstockRecord]
    total_records: int
    usable_records: int
    generated_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Audit Log
# ---------------------------------------------------------------------------


class AuditLogEntry(BaseModel):
    entry_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    prospect_id: Optional[str] = None
    event_type: str  # e.g. "prospect_created", "synthesis_started", "pdf_generated"
    actor: str = "system"  # "system", partner_id, or user identifier
    details: Optional[Dict[str, Any]] = None
    severity: Literal["info", "warning", "error"] = "info"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    session_id: Optional[str] = None
    ip_address: Optional[str] = None
