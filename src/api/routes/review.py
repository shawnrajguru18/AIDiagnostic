"""
FastAPI routes for the senior partner review interface.
Partners use this to inspect, adjust, and approve scorecards before delivery.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import (
    get_db,
    PartnerReviewRecordORM,
    SynthesisOutputORM,
    ScorecardOutputORM,
    ValidationOutputORM,
    ProspectORM,
)

router = APIRouter(tags=["review"])


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------


class ReviewQueueItem(BaseModel):
    prospect_id: str
    company_name: str
    overall_score: float
    overall_tier: str
    review_status: str
    created_at: str
    validation_flags: int  # count of flags requiring attention


class ReviewQueueResponse(BaseModel):
    items: List[ReviewQueueItem]
    total: int


class ScorecardReviewDetail(BaseModel):
    prospect_id: str
    company_name: str
    overall_score: float
    overall_tier: str
    dimension_scores: Dict[str, Any]
    findings: List[Dict[str, Any]]
    recommended_next_step: Dict[str, Any]
    validation_flags: List[Dict[str, Any]]
    confidence_adjustments: List[Dict[str, Any]]
    partner_attention_flags: List[Dict[str, Any]]
    source_data_summary: Dict[str, Any]
    review_status: str


class ApproveRequest(BaseModel):
    notes: str = ""
    partner_id: str = "partner_001"  # in V1 this comes from auth JWT


class AdjustRequest(BaseModel):
    partner_id: str = "partner_001"
    adjustments: Dict[str, Any]
    """
    Expected shape:
    {
      "dimension_adjustments": [
        {
          "dimension_id": "data_foundation",
          "original_score": 52,
          "adjusted_score": 55,
          "justification": "Tech stack evidence suggests stronger foundation than self-reported."
        }
      ],
      "finding_edits": [
        {"finding_id": "<uuid>", "updated_headline": "...", "updated_narrative": "..."}
      ],
      "additional_notes": "..."
    }
    """


class ApproveResponse(BaseModel):
    prospect_id: str
    status: str
    approved_at: str
    review_id: str
    message: str


class AdjustResponse(BaseModel):
    prospect_id: str
    status: str
    adjustments_applied: int
    review_id: str
    message: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@router.get("/queue", response_model=ReviewQueueResponse)
async def get_review_queue(
    db: AsyncSession = Depends(get_db),
) -> ReviewQueueResponse:
    """List scorecards currently awaiting partner review.

    Returns items ordered by creation time (oldest first) so the
    most time-sensitive reviews surface at the top.
    """
    # Pull all partner review records that are pending or in_review
    stmt = (
        select(PartnerReviewRecordORM)
        .where(PartnerReviewRecordORM.status.in_(["pending", "in_review"]))
        .order_by(PartnerReviewRecordORM.created_at.asc())
    )
    result = await db.execute(stmt)
    review_records = result.scalars().all()

    items: List[ReviewQueueItem] = []

    for record in review_records:
        # Fetch synthesis output for score/tier
        synth_stmt = select(SynthesisOutputORM).where(
            SynthesisOutputORM.prospect_id == record.prospect_id
        )
        synth_result = await db.execute(synth_stmt)
        synthesis = synth_result.scalar_one_or_none()

        # Fetch prospect for company name
        prospect_stmt = select(ProspectORM).where(
            ProspectORM.prospect_id == record.prospect_id
        )
        prospect_result = await db.execute(prospect_stmt)
        prospect = prospect_result.scalar_one_or_none()

        # Fetch validation flag count
        val_stmt = select(ValidationOutputORM).where(
            ValidationOutputORM.prospect_id == record.prospect_id
        )
        val_result = await db.execute(val_stmt)
        validation = val_result.scalar_one_or_none()

        flag_count = 0
        if validation and validation.output_json:
            try:
                val_data = json.loads(validation.output_json)
                flag_count = len(val_data.get("validation_flags", []))
            except (json.JSONDecodeError, TypeError):
                pass

        items.append(
            ReviewQueueItem(
                prospect_id=record.prospect_id,
                company_name=prospect.company_name if prospect else "Unknown",
                overall_score=synthesis.overall_score if synthesis else 0.0,
                overall_tier=synthesis.tier if synthesis else "Unknown",
                review_status=record.status,
                created_at=record.created_at.isoformat(),
                validation_flags=flag_count,
            )
        )

    return ReviewQueueResponse(items=items, total=len(items))


@router.get("/{prospect_id}", response_model=ScorecardReviewDetail)
async def get_scorecard_for_review(
    prospect_id: str,
    db: AsyncSession = Depends(get_db),
) -> ScorecardReviewDetail:
    """Return the full scorecard, validation flags, and source data for partner review.

    This is the primary view for the partner review interface — it surfaces
    all AI-generated content alongside the evidence base and any flags that
    require human judgement.
    """
    # Fetch synthesis output
    synth_stmt = select(SynthesisOutputORM).where(
        SynthesisOutputORM.prospect_id == prospect_id
    )
    synth_result = await db.execute(synth_stmt)
    synthesis = synth_result.scalar_one_or_none()

    if not synthesis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No synthesis output found for prospect_id={prospect_id!r}. "
                   "Ensure the diagnostic pipeline has completed before accessing the review.",
        )

    # Fetch prospect
    prospect_stmt = select(ProspectORM).where(ProspectORM.prospect_id == prospect_id)
    prospect_result = await db.execute(prospect_stmt)
    prospect = prospect_result.scalar_one_or_none()

    # Fetch validation output
    val_stmt = select(ValidationOutputORM).where(
        ValidationOutputORM.prospect_id == prospect_id
    )
    val_result = await db.execute(val_stmt)
    validation = val_result.scalar_one_or_none()

    # Fetch scorecard output (if rendered)
    sc_stmt = select(ScorecardOutputORM).where(
        ScorecardOutputORM.prospect_id == prospect_id
    )
    sc_result = await db.execute(sc_stmt)
    scorecard_orm = sc_result.scalar_one_or_none()

    # Fetch review record
    review_stmt = select(PartnerReviewRecordORM).where(
        PartnerReviewRecordORM.prospect_id == prospect_id
    )
    review_result = await db.execute(review_stmt)
    review_record = review_result.scalar_one_or_none()

    # Parse synthesis JSON
    synthesis_data: Dict[str, Any] = {}
    if synthesis.output_json:
        try:
            synthesis_data = json.loads(synthesis.output_json)
        except (json.JSONDecodeError, TypeError):
            pass

    # Parse validation JSON
    validation_flags: List[Dict[str, Any]] = []
    confidence_adjustments: List[Dict[str, Any]] = []
    if validation and validation.output_json:
        try:
            val_data = json.loads(validation.output_json)
            validation_flags = val_data.get("validation_flags", [])
            confidence_adjustments = val_data.get("confidence_adjustments", [])
        except (json.JSONDecodeError, TypeError):
            pass

    return ScorecardReviewDetail(
        prospect_id=prospect_id,
        company_name=prospect.company_name if prospect else "Unknown",
        overall_score=synthesis.overall_score,
        overall_tier=synthesis.tier,
        dimension_scores=synthesis_data.get("dimension_scores", {}),
        findings=synthesis_data.get("findings", []),
        recommended_next_step=synthesis_data.get("recommended_next_step", {}),
        validation_flags=validation_flags,
        confidence_adjustments=confidence_adjustments,
        partner_attention_flags=synthesis_data.get("partner_attention_flags", []),
        source_data_summary={
            "scorecard_pdf_url": scorecard_orm.scorecard_pdf_url if scorecard_orm else None,
            "quick_wins_memo_pdf_url": scorecard_orm.quick_wins_memo_pdf_url if scorecard_orm else None,
            "findings_pdf_url": scorecard_orm.findings_appendix_pdf_url if scorecard_orm else None,
            "model_used": synthesis.model_used,
            "synthesized_at": synthesis.synthesized_at.isoformat(),
            "confidence": synthesis.confidence,
        },
        review_status=review_record.status if review_record else "no_review_record",
    )


@router.post("/{prospect_id}/approve", response_model=ApproveResponse)
async def approve_scorecard(
    prospect_id: str,
    request: ApproveRequest,
    db: AsyncSession = Depends(get_db),
) -> ApproveResponse:
    """Approve a scorecard for delivery to the prospect.

    Creates or updates the PartnerReviewRecord with an approval action
    and captures a training signal for the approval decision.
    """
    approved_at = datetime.utcnow()

    # Retrieve or create the review record
    review_stmt = select(PartnerReviewRecordORM).where(
        PartnerReviewRecordORM.prospect_id == prospect_id
    )
    review_result = await db.execute(review_stmt)
    review_record = review_result.scalar_one_or_none()

    if not review_record:
        review_record = PartnerReviewRecordORM(
            review_id=str(uuid.uuid4()),
            prospect_id=prospect_id,
            partner_id=request.partner_id,
            status="pending",
            created_at=datetime.utcnow(),
        )
        db.add(review_record)

    # Record the approval action
    actions = []
    if review_record.actions_json:
        try:
            actions = json.loads(review_record.actions_json)
        except (json.JSONDecodeError, TypeError):
            actions = []

    actions.append({
        "action_type": "approve",
        "partner_id": request.partner_id,
        "approved_at": approved_at.isoformat(),
        "approval_comment": request.notes,
    })

    review_record.actions_json = json.dumps(actions)
    review_record.status = "approved"
    review_record.review_completed_at = approved_at

    # Update prospect status
    prospect_stmt = select(ProspectORM).where(ProspectORM.prospect_id == prospect_id)
    prospect_result = await db.execute(prospect_stmt)
    prospect = prospect_result.scalar_one_or_none()
    if prospect:
        prospect.processing_status = "completed"
        prospect.updated_at = approved_at

    await db.flush()

    return ApproveResponse(
        prospect_id=prospect_id,
        status="approved",
        approved_at=approved_at.isoformat(),
        review_id=review_record.review_id,
        message=(
            f"Scorecard for prospect {prospect_id} approved by {request.partner_id}. "
            "Delivery to prospect portal is now authorised."
        ),
    )


@router.post("/{prospect_id}/adjust", response_model=AdjustResponse)
async def adjust_scorecard(
    prospect_id: str,
    request: AdjustRequest,
    db: AsyncSession = Depends(get_db),
) -> AdjustResponse:
    """Apply partner adjustments to a scorecard and save training signals.

    Adjustments are applied to the synthesis output stored in the database.
    Each adjustment is recorded as a training signal to improve future
    model calibration.

    Supported adjustment types (in ``request.adjustments``):
    - ``dimension_adjustments``: list of score adjustments per dimension
    - ``finding_edits``: list of headline / narrative edits per finding
    - ``additional_notes``: free-text partner notes
    """
    adjustments = request.adjustments
    applied_count = 0

    # Fetch synthesis output
    synth_stmt = select(SynthesisOutputORM).where(
        SynthesisOutputORM.prospect_id == prospect_id
    )
    synth_result = await db.execute(synth_stmt)
    synthesis = synth_result.scalar_one_or_none()

    if not synthesis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No synthesis output found for prospect_id={prospect_id!r}.",
        )

    synthesis_data: Dict[str, Any] = {}
    if synthesis.output_json:
        try:
            synthesis_data = json.loads(synthesis.output_json)
        except (json.JSONDecodeError, TypeError):
            synthesis_data = {}

    training_signals: List[Dict[str, Any]] = []

    # ---- Apply dimension score adjustments ----
    dim_adjustments = adjustments.get("dimension_adjustments", [])
    if dim_adjustments:
        dimension_scores = synthesis_data.get("dimension_scores", {})
        for adj in dim_adjustments:
            dim_id = adj.get("dimension_id")
            if not dim_id:
                continue
            original_score = adj.get("original_score")
            adjusted_score = adj.get("adjusted_score")
            if adjusted_score is None:
                continue

            # Apply to synthesis data
            if dim_id in dimension_scores:
                dimension_scores[dim_id]["raw_score"] = adjusted_score
                dimension_scores[dim_id]["weighted_score"] = (
                    adjusted_score * dimension_scores[dim_id].get("weight", 0.1667)
                )
            elif isinstance(dimension_scores.get(dim_id), (int, float)):
                dimension_scores[dim_id] = adjusted_score

            applied_count += 1

            # Record training signal
            training_signals.append({
                "signal_type": "score_correction",
                "dimension_id": dim_id,
                "original_value": original_score,
                "corrected_value": adjusted_score,
                "justification": adj.get("justification", ""),
                "partner_id": request.partner_id,
                "captured_at": datetime.utcnow().isoformat(),
            })

        synthesis_data["dimension_scores"] = dimension_scores

        # Recompute overall score if we have dimension data
        if dimension_scores:
            scores = []
            for dim_data in dimension_scores.values():
                if isinstance(dim_data, dict):
                    scores.append(dim_data.get("raw_score", 0))
                elif isinstance(dim_data, (int, float)):
                    scores.append(float(dim_data))
            if scores:
                new_overall = sum(scores) / len(scores)
                synthesis.overall_score = round(new_overall, 1)
                synthesis_data["overall_score"] = synthesis.overall_score

    # ---- Apply finding edits ----
    finding_edits = adjustments.get("finding_edits", [])
    if finding_edits:
        findings = synthesis_data.get("findings", [])
        finding_map = {f.get("finding_id"): f for f in findings if f.get("finding_id")}
        for edit in finding_edits:
            fid = edit.get("finding_id")
            if fid and fid in finding_map:
                original = finding_map[fid].copy()
                if "updated_headline" in edit:
                    finding_map[fid]["headline"] = edit["updated_headline"]
                if "updated_narrative" in edit:
                    finding_map[fid]["narrative"] = edit["updated_narrative"]
                applied_count += 1
                training_signals.append({
                    "signal_type": "finding_edit",
                    "finding_id": fid,
                    "original_value": original,
                    "corrected_value": finding_map[fid],
                    "partner_id": request.partner_id,
                    "captured_at": datetime.utcnow().isoformat(),
                })
        synthesis_data["findings"] = list(finding_map.values())

    # Persist updated synthesis data
    synthesis.output_json = json.dumps(synthesis_data)

    # Retrieve or create review record
    review_stmt = select(PartnerReviewRecordORM).where(
        PartnerReviewRecordORM.prospect_id == prospect_id
    )
    review_result = await db.execute(review_stmt)
    review_record = review_result.scalar_one_or_none()

    if not review_record:
        review_record = PartnerReviewRecordORM(
            review_id=str(uuid.uuid4()),
            prospect_id=prospect_id,
            partner_id=request.partner_id,
            status="in_review",
            created_at=datetime.utcnow(),
        )
        db.add(review_record)

    # Append training signals
    existing_signals = []
    if review_record.training_signals_json:
        try:
            existing_signals = json.loads(review_record.training_signals_json)
        except (json.JSONDecodeError, TypeError):
            existing_signals = []
    existing_signals.extend(training_signals)
    review_record.training_signals_json = json.dumps(existing_signals)
    review_record.status = "in_review"

    # Append adjustment actions
    existing_actions = []
    if review_record.actions_json:
        try:
            existing_actions = json.loads(review_record.actions_json)
        except (json.JSONDecodeError, TypeError):
            existing_actions = []
    existing_actions.append({
        "action_type": "adjust_score",
        "partner_id": request.partner_id,
        "adjustments": adjustments,
        "applied_count": applied_count,
        "adjusted_at": datetime.utcnow().isoformat(),
    })
    review_record.actions_json = json.dumps(existing_actions)

    await db.flush()

    return AdjustResponse(
        prospect_id=prospect_id,
        status="in_review",
        adjustments_applied=applied_count,
        review_id=review_record.review_id,
        message=(
            f"Applied {applied_count} adjustment(s) to the scorecard for prospect {prospect_id}. "
            f"{len(training_signals)} training signal(s) recorded. "
            "Submit /approve when the scorecard is ready for delivery."
        ),
    )
