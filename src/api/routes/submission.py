"""
FastAPI routes for the prospect submission flow.
Handles intake, questionnaire delivery, completion, status, and demo scenarios.
"""

from __future__ import annotations

import asyncio
import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db, ProspectORM, QuestionnaireResponseORM, SynthesisOutputORM
from src.data.questionnaire import get_question_pool, get_questions_for_persona as get_questions_by_persona

router = APIRouter(prefix="/api/submission", tags=["submission"])


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------


class SubmissionRequest(BaseModel):
    prospect_name: str
    prospect_role: str
    prospect_email: str
    company_name: str
    company_website: Optional[str] = None
    # Consent flags
    c2_benchmark_consent: bool = True   # default opt-in to anonymous benchmarking
    c3_internal_ai_consent: bool = False
    c4_cross_practice_consent: bool = False

    @field_validator("prospect_name", "prospect_role", "company_name")
    @classmethod
    def must_not_be_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field must not be blank.")
        return v.strip()

    @field_validator("prospect_email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        import re
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(pattern, v):
            raise ValueError(f"Invalid email address: {v!r}")
        return v.strip().lower()


class QuestionnaireAnswerRequest(BaseModel):
    prospect_id: str
    responses: List[Dict[str, Any]]  # [{question_id: str, answer: dict}]


class SubmissionResponse(BaseModel):
    prospect_id: str
    status: str
    questionnaire: Optional[Dict[str, Any]] = None
    message: str


class CompletionResponse(BaseModel):
    prospect_id: str
    status: str
    portal_link: str
    delivery_promise: str
    message: str


class StatusResponse(BaseModel):
    prospect_id: str
    processing_status: str
    overall_score: Optional[float] = None
    overall_tier: Optional[str] = None
    completed_at: Optional[str] = None
    message: str


# ---------------------------------------------------------------------------
# In-memory processing state (for V0; replace with DB in V1)
# ---------------------------------------------------------------------------

_PROCESSING_STATE: Dict[str, Dict[str, Any]] = {}


# ---------------------------------------------------------------------------
# Background pipeline task
# ---------------------------------------------------------------------------


async def _run_pipeline_background(
    prospect_id: str,
    submission_data: Dict[str, Any],
    questionnaire_responses: Optional[List[Dict[str, Any]]] = None,
) -> None:
    """Simulate the full diagnostic pipeline in the background.

    In production this invokes the DiagnosticWorkflow orchestrator.
    In V0 we run a lightweight simulation that produces a plausible result.
    """
    _PROCESSING_STATE[prospect_id]["status"] = "running"

    try:
        # Attempt to import and use the real workflow if available
        from src.orchestrator.workflow import DiagnosticWorkflow
        workflow = DiagnosticWorkflow()
        result = await asyncio.wait_for(
            workflow.run(
                prospect_id=prospect_id,
                submission_data=submission_data,
                questionnaire_responses=questionnaire_responses or [],
            ),
            timeout=300,  # 5-minute hard cap
        )
        _PROCESSING_STATE[prospect_id]["status"] = "completed"
        _PROCESSING_STATE[prospect_id]["result"] = result
    except ImportError:
        # Workflow not yet implemented — produce a stub result
        await asyncio.sleep(2)
        _PROCESSING_STATE[prospect_id]["status"] = "completed"
        _PROCESSING_STATE[prospect_id]["result"] = {
            "overall_score": 55.0,
            "overall_tier": "Developing",
            "message": "Stub result — orchestrator not yet implemented",
        }
    except Exception as exc:
        _PROCESSING_STATE[prospect_id]["status"] = "failed"
        _PROCESSING_STATE[prospect_id]["error"] = str(exc)


# ---------------------------------------------------------------------------
# Questionnaire builder (lightweight persona-aware selection for V0)
# ---------------------------------------------------------------------------


def _build_questionnaire(
    prospect_id: str,
    persona: str = "P1",
    company_name: str = "Your Company",
) -> Dict[str, Any]:
    """Build a personalised questionnaire for the given persona."""
    pool = get_questions_by_persona(persona)
    # Limit to 16 questions for V0
    selected = pool[:16]

    questions = []
    for q in selected:
        question_text = q.get("question_text", "")
        # Apply persona variant text if available
        variant_map = q.get("persona_variant_text") or {}
        question_text = variant_map.get(persona, question_text)

        questions.append({
            "question_id": q["question_id"],
            "dimension_id": q["dimension_id"],
            "question_text": question_text,
            "question_type": q["question_type"],
            "weight": q["weight"],
            "options": q.get("options"),
            "scale_anchors": q.get("scale_anchors"),
            "max_chars": q.get("max_chars"),
            "helper_text": q.get("helper_text"),
            "skip_logic": q.get("skip_logic"),
        })

    return {
        "questionnaire_id": str(uuid.uuid4()),
        "prospect_id": prospect_id,
        "persona": persona,
        "questions": questions,
        "total_questions": len(questions),
        "estimated_minutes": max(8, len(questions) // 2),
        "generated_at": datetime.utcnow().isoformat(),
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@router.post("/start", response_model=SubmissionResponse)
async def start_submission(
    request: SubmissionRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> SubmissionResponse:
    """Validate the prospect submission and return a personalised questionnaire.

    Steps:
    1. Validate submission fields.
    2. Assign a prospect_id and infer a default persona (P1 for executive roles).
    3. Build and return the personalised questionnaire.
    4. Kick off background research agents (B1, B2, B3).
    """
    prospect_id = str(uuid.uuid4())

    # Infer persona from role keywords
    role_lower = request.prospect_role.lower()
    if any(kw in role_lower for kw in ("ceo", "coo", "cfo", "cto", "cio", "cdo", "chief", "vp", "president", "director", "svp", "evp")):
        persona = "P1"
    elif any(kw in role_lower for kw in ("architect", "engineer", "developer", "data scientist", "analyst", "technical", "manager")):
        persona = "P2"
    else:
        persona = "P3"

    # Persist the prospect record
    prospect_orm = ProspectORM(
        prospect_id=prospect_id,
        company_name=request.company_name,
        industry="Other",  # will be resolved by A1 in background
        size_band="Large",
        geography="US",
        primary_contact_name=request.prospect_name,
        primary_contact_email=request.prospect_email,
        primary_contact_title=request.prospect_role,
        session_token=str(uuid.uuid4()),
        processing_status="pending",
        persona=persona,
    )
    db.add(prospect_orm)
    await db.flush()

    # Initialise in-memory state
    _PROCESSING_STATE[prospect_id] = {
        "status": "pending",
        "created_at": datetime.utcnow().isoformat(),
        "company_name": request.company_name,
        "persona": persona,
    }

    # Build questionnaire
    questionnaire = _build_questionnaire(prospect_id, persona, request.company_name)

    # Start background research
    submission_dict = {
        "prospect_name": request.prospect_name,
        "prospect_role": request.prospect_role,
        "prospect_email": request.prospect_email,
        "company_name": request.company_name,
        "company_website": request.company_website,
        "consent": {
            "c2_benchmark": request.c2_benchmark_consent,
            "c3_internal_ai": request.c3_internal_ai_consent,
            "c4_cross_practice": request.c4_cross_practice_consent,
        },
    }
    background_tasks.add_task(
        _run_pipeline_background,
        prospect_id=prospect_id,
        submission_data=submission_dict,
    )

    return SubmissionResponse(
        prospect_id=prospect_id,
        status="questionnaire_ready",
        questionnaire=questionnaire,
        message=(
            f"Welcome, {request.prospect_name}. Your personalised {questionnaire['total_questions']}-question "
            f"diagnostic is ready. Estimated completion time: {questionnaire['estimated_minutes']} minutes."
        ),
    )


@router.post("/complete", response_model=CompletionResponse)
async def complete_questionnaire(
    request: QuestionnaireAnswerRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> CompletionResponse:
    """Save questionnaire responses and trigger the synthesis pipeline.

    The synthesis pipeline (scoring + findings + quick wins + PDF rendering)
    runs asynchronously. The endpoint returns immediately with a portal link
    and a 24-hour delivery promise.
    """
    prospect_id = request.prospect_id

    # Persist questionnaire responses
    response_orm = QuestionnaireResponseORM(
        response_id=str(uuid.uuid4()),
        prospect_id=prospect_id,
        questionnaire_id=str(uuid.uuid4()),  # will be linked in V1
        responses_json=json.dumps(request.responses),
        completed=True,
        started_at=datetime.utcnow(),
        completed_at=datetime.utcnow(),
    )
    db.add(response_orm)
    await db.flush()

    # Update in-memory state
    state = _PROCESSING_STATE.get(prospect_id, {})
    state["status"] = "running"
    state["responses_received"] = len(request.responses)
    _PROCESSING_STATE[prospect_id] = state

    # Trigger synthesis in background
    background_tasks.add_task(
        _run_pipeline_background,
        prospect_id=prospect_id,
        submission_data=state.get("submission", {}),
        questionnaire_responses=request.responses,
    )

    portal_link = f"https://diagnostic.dxc.com/results/{prospect_id}"

    return CompletionResponse(
        prospect_id=prospect_id,
        status="processing",
        portal_link=portal_link,
        delivery_promise="Your AI Readiness Scorecard will be ready within 24 hours.",
        message=(
            f"Thank you! We received {len(request.responses)} responses. "
            f"Your scorecard is being generated and will be available at {portal_link} "
            f"within 24 hours. A senior DXC partner will review the findings before delivery."
        ),
    )


@router.get("/status/{prospect_id}", response_model=StatusResponse)
async def get_status(
    prospect_id: str,
    db: AsyncSession = Depends(get_db),
) -> StatusResponse:
    """Return the current processing status for a given prospect_id."""
    state = _PROCESSING_STATE.get(prospect_id)

    if not state:
        # Try the DB as a fallback
        from sqlalchemy import select
        stmt = select(SynthesisOutputORM).where(
            SynthesisOutputORM.prospect_id == prospect_id
        )
        result = await db.execute(stmt)
        synthesis = result.scalar_one_or_none()

        if synthesis:
            return StatusResponse(
                prospect_id=prospect_id,
                processing_status="completed",
                overall_score=synthesis.overall_score,
                overall_tier=synthesis.tier,
                completed_at=synthesis.synthesized_at.isoformat(),
                message="Scorecard is ready.",
            )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No submission found for prospect_id={prospect_id!r}",
        )

    processing_status = state.get("status", "unknown")
    result = state.get("result", {})

    return StatusResponse(
        prospect_id=prospect_id,
        processing_status=processing_status,
        overall_score=result.get("overall_score"),
        overall_tier=result.get("overall_tier"),
        completed_at=state.get("completed_at"),
        message={
            "pending": "Your submission is queued for processing.",
            "running": "Your diagnostic is being generated — research agents are active.",
            "completed": "Your scorecard is ready.",
            "failed": f"Processing failed: {state.get('error', 'unknown error')}",
        }.get(processing_status, f"Status: {processing_status}"),
    )


@router.get("/demo/{scenario}")
async def run_demo_scenario(scenario: str) -> Dict[str, Any]:
    """Run one of the three demo scenarios end-to-end.

    Supported scenarios:
    - ``meridian_fs``     : MeridianFS (Financial Services, Large, ~55 Developing)
    - ``northern_care``   : NorthernCare Health (Healthcare, Mid-Market, ~41 Emerging)
    - ``aurelian_tech``   : Aurelian Technologies (Technology, Enterprise, ~68 Established)

    Returns the complete scorecard output including synthesised content,
    radar chart data URI, and all three PDF artifact sizes.
    """
    valid_scenarios = {"meridian_fs", "northern_care", "aurelian_tech"}
    if scenario not in valid_scenarios:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Unknown scenario {scenario!r}. "
                f"Valid options: {sorted(valid_scenarios)}"
            ),
        )

    try:
        from src.orchestrator.workflow import DiagnosticWorkflow
        workflow = DiagnosticWorkflow()
        result = await workflow.run_demo_scenario(scenario)
        return result
    except ImportError:
        # Orchestrator not yet implemented — return a stub fixture
        pass

    # Stub fixtures per scenario
    fixtures: Dict[str, Dict[str, Any]] = {
        "meridian_fs": _stub_meridian_fs(),
        "northern_care": _stub_northern_care(),
        "aurelian_tech": _stub_aurelian_tech(),
    }

    return fixtures[scenario]


# ---------------------------------------------------------------------------
# Stub fixtures (used when orchestrator is not yet available)
# ---------------------------------------------------------------------------


def _stub_meridian_fs() -> Dict[str, Any]:
    return {
        "scenario": "meridian_fs",
        "company_name": "MeridianFS",
        "overall_score": 55,
        "overall_tier": "Developing",
        "dimension_scores": {
            "data_foundation": 50,
            "governance_posture": 62,
            "ai_investment_maturity": 48,
            "org_change_readiness": 55,
            "value_pocket_clarity": 68,
            "regulatory_complexity": 44,
        },
        "findings": [
            {"headline": "Data estate is partially integrated; ML-ready dataset coverage below 40%."},
            {"headline": "AI governance framework adopted but enforcement mechanisms are limited."},
            {"headline": "AI investment concentrated in pilots; MLOps function not yet formalised."},
            {"headline": "Regulatory exposure across SR 11-7 and EU AI Act requires near-term action."},
        ],
        "recommended_next_step": {
            "title": "AI Potential Review (APR) Discovery Session",
            "description": "A structured two-day engagement with your leadership team to validate findings and produce a 90-day activation roadmap.",
        },
        "quick_wins": [
            "AI-assisted contract review (procurement team, 6–10 weeks)",
            "Intelligent claims processing signal layer (8–12 weeks)",
            "AI literacy baseline assessment and role-specific upskilling plan",
        ],
        "stub": True,
        "note": "Stub output — run with orchestrator for full AI-generated content.",
    }


def _stub_northern_care() -> Dict[str, Any]:
    return {
        "scenario": "northern_care",
        "company_name": "NorthernCare Health",
        "overall_score": 41,
        "overall_tier": "Emerging",
        "dimension_scores": {
            "data_foundation": 35,
            "governance_posture": 38,
            "ai_investment_maturity": 30,
            "org_change_readiness": 44,
            "value_pocket_clarity": 55,
            "regulatory_complexity": 42,
        },
        "findings": [
            {"headline": "Data remains heavily siloed across clinical and administrative systems."},
            {"headline": "No formal AI governance policy; HIPAA controls exist but are not AI-specific."},
            {"headline": "AI investment at exploration stage only — no production AI systems deployed."},
            {"headline": "High HIPAA and FDA (SaMD) regulatory burden constrains near-term deployment velocity."},
        ],
        "recommended_next_step": {
            "title": "Data Foundation Readiness Assessment",
            "description": "A focused 30-day engagement to map the data estate, identify quick wins for integration, and produce a prioritised data readiness roadmap ahead of AI deployment.",
        },
        "quick_wins": [
            "Clinical document summarisation using approved LLM (HIPAA BAA in place)",
            "Scheduling optimisation pilot using existing EHR data",
            "AI governance policy workshop and CAIO role definition",
        ],
        "stub": True,
        "note": "Stub output — run with orchestrator for full AI-generated content.",
    }


def _stub_aurelian_tech() -> Dict[str, Any]:
    return {
        "scenario": "aurelian_tech",
        "company_name": "Aurelian Technologies",
        "overall_score": 68,
        "overall_tier": "Established",
        "dimension_scores": {
            "data_foundation": 72,
            "governance_posture": 70,
            "ai_investment_maturity": 75,
            "org_change_readiness": 65,
            "value_pocket_clarity": 73,
            "regulatory_complexity": 58,
        },
        "findings": [
            {"headline": "Strong data mesh architecture with 70%+ ML-ready dataset coverage."},
            {"headline": "Embedded AI governance with automated model monitoring in place."},
            {"headline": "Multiple AI systems in production; MLOps team established and growing."},
            {"headline": "Opportunity to accelerate from Established to Leading through role-specific upskilling at scale."},
        ],
        "recommended_next_step": {
            "title": "AI Scale-Up Roadmap Workshop",
            "description": "A two-day executive workshop to identify the next three AI value pockets, define the scaling roadmap from Established to Leading, and align organisational capability investment.",
        },
        "quick_wins": [
            "Expand GenAI co-pilot from engineering to product and marketing teams (8 weeks)",
            "Deploy predictive churn model using existing customer data lake",
            "Launch role-specific AI upskilling for top 5 non-technical job families",
        ],
        "stub": True,
        "note": "Stub output — run with orchestrator for full AI-generated content.",
    }
