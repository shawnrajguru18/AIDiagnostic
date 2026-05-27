"""Main workflow orchestrator for the DXC AI Readiness Diagnostic V0.

Implements the DiagnosticWorkflow class, which manages the four pipeline
phases:

    intake  ->  research (B1/B2/B3 parallel)  ->  synthesis  ->  output

Each phase is an async method. The full pipeline is composed via
run_full_pipeline(). A demo runner is provided via run_demo_scenario().

Design notes:
- No external workflow framework dependency for V0 (LangGraph is available
  if needed for V0.5 but complicates local testing).
- asyncio.gather() used for the parallelisable research phase.
- SLA budgets and cost tracking are tracked per run and returned in the result.
- Audit log is an in-memory list for V0; replace with DB writes for V0.1+.
"""

from __future__ import annotations

import asyncio
import json
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Agent imports
# ---------------------------------------------------------------------------

from src.agents.a1_intake import A1IntakeAgent
from src.agents.b1_financial import B1FinancialAgent
from src.agents.b2_news import B2NewsAgent
from src.agents.b3_tech_stack import B3TechStackAgent
from src.agents.c1_industry import C1IndustryAgent
from src.agents.c2_synthesis import C2SynthesisAgent
from src.agents.c3_quick_wins import C3QuickWinsAgent
from src.agents.d1_output import D1OutputAgent
from src.agents.d2_validation import D2ValidationAgent

# ---------------------------------------------------------------------------
# SLA budgets (seconds per phase)
# ---------------------------------------------------------------------------

SLA_BUDGETS_SECONDS: Dict[str, int] = {
    "intake": 60,
    "research": 120,
    "synthesis": 180,
    "output": 120,
    "full_pipeline": 480,
}

# ---------------------------------------------------------------------------
# Global in-memory audit log (V0 only — replace with DB in V0.1+)
# ---------------------------------------------------------------------------

_AUDIT_LOG: List[Dict[str, Any]] = []


def get_audit_log() -> List[Dict[str, Any]]:
    """Return the current in-memory audit log (read-only access)."""
    return list(_AUDIT_LOG)


def clear_audit_log() -> None:
    """Clear the in-memory audit log (useful for testing)."""
    _AUDIT_LOG.clear()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _elapsed_s(start: float) -> float:
    return round(time.time() - start, 2)


def _audit(
    event_type: str,
    prospect_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    severity: str = "info",
) -> None:
    """Append an entry to the in-memory audit log."""
    _AUDIT_LOG.append(
        {
            "entry_id": str(uuid.uuid4()),
            "timestamp": _now_iso(),
            "event_type": event_type,
            "prospect_id": prospect_id,
            "severity": severity,
            "details": details or {},
        }
    )


def _agent_cost_record(agent_id: str, result: Any) -> Dict[str, Any]:
    """Build a cost record stub for an agent result.

    The Anthropic SDK does not expose token counts through the current
    BaseAgent._call_llm() interface. This stub records what is available
    and is designed to be replaced with real token tracking when
    _call_llm() is updated to return usage metadata.
    """
    return {
        "agent_id": agent_id,
        "latency_ms": getattr(result, "latency_ms", 0),
        "success": getattr(result, "success", False),
        "input_tokens": None,   # TODO: capture from message.usage.input_tokens
        "output_tokens": None,  # TODO: capture from message.usage.output_tokens
    }


def _check_sla(phase: str, elapsed_s: float) -> Optional[str]:
    """Return an SLA warning string if the phase exceeded its budget, else None."""
    budget = SLA_BUDGETS_SECONDS.get(phase)
    if budget and elapsed_s > budget:
        return (
            f"SLA_EXCEEDED: phase={phase} elapsed={elapsed_s}s budget={budget}s "
            f"overage={elapsed_s - budget:.1f}s"
        )
    return None


def _build_research_summary(b1: dict, b2: dict, b3: dict) -> dict:
    """Build a compact research summary dict for D1 consumption.

    Avoids passing full B outputs (which can be large) to D1 while retaining
    the key signals D1 needs for grounding claims.
    """
    return {
        "b1_financial": {
            "ticker": b1.get("ticker"),
            "revenue_usd_millions": b1.get("revenue_usd_millions"),
            "employee_count": b1.get("employee_count"),
            "capex_trend": b1.get("capex_trend"),
            "digital_transformation_signals": b1.get("digital_transformation_signals", [])[:5],
            "ai_mentions_in_filings": b1.get("ai_mentions_in_filings", 0),
            "confidence": b1.get("confidence"),
        },
        "b2_news": {
            "overall_ai_narrative": b2.get("overall_ai_narrative"),
            "ai_signals": b2.get("ai_signals", [])[:5],
            "regulatory_mentions": b2.get("regulatory_mentions", [])[:3],
            "competitor_mentions": b2.get("competitor_mentions", [])[:3],
        },
        "b3_tech_stack": {
            "cloud_maturity": b3.get("cloud_maturity"),
            "data_platform_maturity": b3.get("data_platform_maturity"),
            "overall_tech_readiness": b3.get("overall_tech_readiness"),
            "existing_ai_tools": b3.get("existing_ai_tools", []),
            "platforms_detected": [
                {
                    "platform_name": p.get("platform_name"),
                    "category": p.get("category"),
                    "confidence_tier": p.get("confidence_tier"),
                    "ai_readiness_signal": p.get("ai_readiness_signal"),
                }
                for p in b3.get("platforms_detected", [])[:8]
            ],
            "tech_debt_signals": b3.get("tech_debt_signals", [])[:3],
        },
    }


# (B agent stubs removed — real B1/B2/B3 agents are used via self.b1/b2/b3)


# ---------------------------------------------------------------------------
# DiagnosticWorkflow
# ---------------------------------------------------------------------------


class DiagnosticWorkflow:
    """Orchestrates the full DXC AI Readiness Diagnostic pipeline.

    All public methods are async. Use asyncio.run() or await from an async
    context. In FastAPI, use BackgroundTasks or a dedicated async route.

    Usage::

        workflow = DiagnosticWorkflow()
        result = await workflow.run_full_pipeline(submission, questionnaire_responses)
    """

    def __init__(self) -> None:
        # Instantiate agents (stateless — safe to share across runs)
        self.a1 = A1IntakeAgent()
        self.b1 = B1FinancialAgent()
        self.b2 = B2NewsAgent()
        self.b3 = B3TechStackAgent()
        self.c1 = C1IndustryAgent()
        self.c2 = C2SynthesisAgent()
        self.c3 = C3QuickWinsAgent()
        self.d1 = D1OutputAgent()
        self.d2 = D2ValidationAgent()

    # ------------------------------------------------------------------
    # Phase 1: Intake
    # ------------------------------------------------------------------

    async def run_intake(self, submission: dict) -> dict:
        """Run the intake phase: A1 validation and normalisation.

        In V0, A2 (persona inference) and A3 (question personalisation) are
        included as part of the intake flow when their agents are available.
        For now, persona is derived from the A1 output if present in submission,
        or defaults to 'P1'.

        Args:
            submission: Raw prospect submission dict. Required fields:
                - prospect_name, prospect_role, prospect_email, company_name_raw
                Optional: company_website, primary_persona

        Returns:
            dict with keys:
                - prospect_id: str
                - normalized: dict (A1 normalised company data)
                - primary_persona: str (P1|P2|P3)
                - validation_status: str
                - flags: list
                - phase_elapsed_s: float
                - sla_warning: str | None
                - agent_costs: list
        """
        phase_start = time.time()
        prospect_id = submission.get("prospect_id") or str(uuid.uuid4())

        _audit("intake_started", prospect_id=prospect_id, details={"submission_keys": list(submission.keys())})

        # Run A1
        a1_result = await asyncio.get_event_loop().run_in_executor(
            None, self.a1.run, submission
        )

        agent_costs = [_agent_cost_record("A1_intake", a1_result)]

        if not a1_result.success:
            _audit("intake_failed", prospect_id=prospect_id, details={"error": a1_result.error}, severity="error")
            return {
                "prospect_id": prospect_id,
                "success": False,
                "error": a1_result.error,
                "phase_elapsed_s": _elapsed_s(phase_start),
                "agent_costs": agent_costs,
            }

        normalized = a1_result.data.get("normalized", {})
        # Preserve the prospect_id from A1 output if available
        if "prospect_id" in a1_result.data:
            prospect_id = a1_result.data["prospect_id"]

        # Infer persona: use submission override, then derive from role
        primary_persona = submission.get("primary_persona") or self._infer_persona(
            prospect_role=normalized.get("prospect_role", ""),
            industry=normalized.get("company_industry_label", ""),
        )

        elapsed = _elapsed_s(phase_start)
        sla_warning = _check_sla("intake", elapsed)

        _audit(
            "intake_completed",
            prospect_id=prospect_id,
            details={
                "validation_status": a1_result.data.get("validation_status"),
                "company": normalized.get("company_canonical_name"),
                "persona": primary_persona,
                "elapsed_s": elapsed,
                "sla_warning": sla_warning,
            },
        )

        return {
            "prospect_id": prospect_id,
            "success": True,
            "normalized": normalized,
            "primary_persona": primary_persona,
            "validation_status": a1_result.data.get("validation_status"),
            "flags": a1_result.data.get("flags", []),
            "phase_elapsed_s": elapsed,
            "sla_warning": sla_warning,
            "agent_costs": agent_costs,
        }

    # ------------------------------------------------------------------
    # Phase 2: Research
    # ------------------------------------------------------------------

    async def run_research(self, prospect_id: str, normalized: dict) -> dict:
        """Run the research phase: B1, B2, B3 in parallel.

        B1 (financial research), B2 (news signals), B3 (tech stack inference)
        run concurrently using asyncio.gather. B4 (competitor) and B5
        (regulatory) are optional and run sequentially if available.

        Args:
            prospect_id: Prospect identifier from intake phase.
            normalized: Normalised company data from A1.

        Returns:
            dict with keys: b1, b2, b3, b4, b5, phase_elapsed_s, sla_warning, agent_costs
        """
        phase_start = time.time()

        _audit("research_started", prospect_id=prospect_id)

        company_name = normalized.get("company_canonical_name", "")
        ticker = normalized.get("company_ticker")
        hq_country = normalized.get("company_hq_country", "")
        industry_label = normalized.get("company_industry_label", "")
        size_band = normalized.get("company_size_band_estimate", "unknown")

        # Inputs for each B agent
        b1_inputs = {
            "company_canonical_name": company_name,
            "company_ticker": ticker,
            "company_hq_country": hq_country,
            "company_industry_label": industry_label,
            "prospect_id": prospect_id,
        }
        b2_inputs = {
            "company_canonical_name": company_name,
            "company_industry_label": industry_label,
            "prospect_id": prospect_id,
        }
        b3_inputs = {
            "company_canonical_name": company_name,
            "company_industry_label": industry_label,
            "company_size_band_estimate": size_band,
            "company_hq_country": hq_country,
            "prospect_id": prospect_id,
        }

        loop = asyncio.get_event_loop()

        # Run B1, B2, B3 in parallel via executor (agents are synchronous)
        b1_future = loop.run_in_executor(None, self.b1.run, b1_inputs)
        b2_future = loop.run_in_executor(None, self.b2.run, b2_inputs)
        b3_future = loop.run_in_executor(None, self.b3.run, b3_inputs)

        b1_agent_result, b2_agent_result, b3_agent_result = await asyncio.gather(
            b1_future, b2_future, b3_future, return_exceptions=True
        )

        def _safe_agent_result(result: Any, name: str) -> tuple[dict, str]:
            """Return (data_dict, agent_id) from an AgentResult or exception."""
            if isinstance(result, Exception):
                _audit(
                    f"{name}_exception",
                    prospect_id=prospect_id,
                    details={"error": str(result)},
                    severity="warning",
                )
                return {"_error": str(result), "_failed": True}, name
            if not result.success:
                _audit(
                    f"{name}_failed",
                    prospect_id=prospect_id,
                    details={"error": result.error},
                    severity="warning",
                )
                return {"_error": result.error, "_failed": True}, result.agent_id
            return result.data, result.agent_id

        b1_data, b1_agent_id = _safe_agent_result(b1_agent_result, "B1_financial")
        b2_data, b2_agent_id = _safe_agent_result(b2_agent_result, "B2_news")
        b3_data, b3_agent_id = _safe_agent_result(b3_agent_result, "B3_tech_stack")

        # Build cost records from AgentResult objects
        research_agent_costs = []
        for res, aid in [
            (b1_agent_result, "B1_financial"),
            (b2_agent_result, "B2_news"),
            (b3_agent_result, "B3_tech_stack"),
        ]:
            if not isinstance(res, Exception):
                research_agent_costs.append(_agent_cost_record(aid, res))

        b1: Dict[str, Any] = b1_data
        b2: Dict[str, Any] = b2_data
        b3: Dict[str, Any] = b3_data
        b4: Dict[str, Any] = {}
        b5: Dict[str, Any] = {}

        elapsed = _elapsed_s(phase_start)
        sla_warning = _check_sla("research", elapsed)

        _audit(
            "research_completed",
            prospect_id=prospect_id,
            details={
                "b1_failed": b1.get("_failed", False),
                "b2_failed": b2.get("_failed", False),
                "b3_failed": b3.get("_failed", False),
                "elapsed_s": elapsed,
                "sla_warning": sla_warning,
            },
        )

        return {
            "b1": b1,
            "b2": b2,
            "b3": b3,
            "b4": b4,
            "b5": b5,
            "phase_elapsed_s": elapsed,
            "sla_warning": sla_warning,
            "agent_costs": research_agent_costs,
        }

    # ------------------------------------------------------------------
    # Phase 3: Synthesis
    # ------------------------------------------------------------------

    async def run_synthesis(
        self,
        prospect_id: str,
        questionnaire_responses: dict,
        research: dict,
        normalized: dict,
        primary_persona: str,
    ) -> dict:
        """Run the synthesis phase: C1 -> C2 -> C3 (sequential dependencies).

        C1 (industry mapping) must complete before C2 (synthesis).
        C2 must complete before C3 (quick wins).

        Args:
            prospect_id: Prospect identifier.
            questionnaire_responses: Dict with 'responses' list of response dicts.
            research: Combined research output from run_research().
            normalized: Normalised company data from A1.
            primary_persona: P1|P2|P3.

        Returns:
            dict with keys: c1, c2, c3, phase_elapsed_s, sla_warning, agent_costs
        """
        phase_start = time.time()
        agent_costs = []

        _audit("synthesis_started", prospect_id=prospect_id)

        company_name = normalized.get("company_canonical_name", "Unknown")
        industry_label = normalized.get("company_industry_label", "")
        industry_naics = normalized.get("company_industry_naics", "")
        size_band = normalized.get("company_size_band_estimate", "unknown")

        # --- C1: Industry library mapping ---
        c1_inputs = {
            "company_canonical_name": company_name,
            "company_industry_label": industry_label,
            "company_industry_naics": industry_naics,
            "company_size_band_estimate": size_band,
        }
        c1_result = await asyncio.get_event_loop().run_in_executor(
            None, self.c1.run, c1_inputs
        )
        agent_costs.append(_agent_cost_record("C1_industry", c1_result))

        if not c1_result.success:
            _audit("c1_failed", prospect_id=prospect_id, details={"error": c1_result.error}, severity="warning")
            c1_data = {"applicable_processes": [], "library_status": "tier1_only", "confidence": 0.5}
        else:
            c1_data = c1_result.data

        # --- C2: Core synthesis ---
        responses_list = questionnaire_responses.get("responses", [])

        c2_inputs = {
            "company_canonical_name": company_name,
            "primary_persona": primary_persona,
            "company_industry_label": industry_label,
            "questionnaire_responses_json": responses_list,
            "b1_output_json": research.get("b1", {}),
            "b2_output_json": research.get("b2", {}),
            "b3_output_json": research.get("b3", {}),
            "c1_output_json": c1_data,
            "b4_output_json": research.get("b4"),
            "b5_output_json": research.get("b5"),
        }
        c2_result = await asyncio.get_event_loop().run_in_executor(
            None, self.c2.run, c2_inputs
        )
        agent_costs.append(_agent_cost_record("C2_synthesis", c2_result))

        if not c2_result.success:
            _audit("c2_failed", prospect_id=prospect_id, details={"error": c2_result.error}, severity="error")
            return {
                "success": False,
                "error": f"C2 synthesis failed: {c2_result.error}",
                "c1": c1_data,
                "c2": None,
                "c3": None,
                "phase_elapsed_s": _elapsed_s(phase_start),
                "agent_costs": agent_costs,
            }

        c2_data = c2_result.data

        # --- C3: Quick wins ---
        c3_inputs = {
            "company_canonical_name": company_name,
            "company_industry_label": industry_label,
            "company_size_band_estimate": size_band,
            "primary_persona": primary_persona,
            "c2_output_json": c2_data,
            "b3_output_json": research.get("b3", {}),
            "c1_output_json": c1_data,
        }
        c3_result = await asyncio.get_event_loop().run_in_executor(
            None, self.c3.run, c3_inputs
        )
        agent_costs.append(_agent_cost_record("C3_quick_wins", c3_result))

        if not c3_result.success:
            _audit("c3_failed", prospect_id=prospect_id, details={"error": c3_result.error}, severity="warning")
            c3_data = {"selected_quick_wins": [], "total_candidates_evaluated": 0}
        else:
            c3_data = c3_result.data

        elapsed = _elapsed_s(phase_start)
        sla_warning = _check_sla("synthesis", elapsed)

        _audit(
            "synthesis_completed",
            prospect_id=prospect_id,
            details={
                "overall_score": c2_data.get("overall_score"),
                "tier": c2_data.get("tier"),
                "quick_wins_count": len(c3_data.get("selected_quick_wins", [])),
                "elapsed_s": elapsed,
                "sla_warning": sla_warning,
            },
        )

        return {
            "success": True,
            "c1": c1_data,
            "c2": c2_data,
            "c3": c3_data,
            "phase_elapsed_s": elapsed,
            "sla_warning": sla_warning,
            "agent_costs": agent_costs,
        }

    # ------------------------------------------------------------------
    # Phase 4: Output
    # ------------------------------------------------------------------

    async def run_output(
        self,
        prospect_id: str,
        synthesis: dict,
        research: dict,
        normalized: dict,
        primary_persona: str,
        assessment_date: Optional[str] = None,
        questionnaire_responses: Optional[dict] = None,
    ) -> dict:
        """Run the output phase: D1 (generation) -> D2 (validation).

        Args:
            prospect_id: Prospect identifier.
            synthesis: Combined synthesis output from run_synthesis().
            research: Combined research output from run_research().
            normalized: Normalised company data from A1.
            primary_persona: P1|P2|P3.
            assessment_date: ISO date string (defaults to today).

        Returns:
            dict with keys: d1, d2, validation_passed, phase_elapsed_s, sla_warning, agent_costs
        """
        phase_start = time.time()
        agent_costs = []

        _audit("output_started", prospect_id=prospect_id)

        company_name = normalized.get("company_canonical_name", "Unknown")
        industry_label = normalized.get("company_industry_label", "")
        date_str = assessment_date or datetime.now(timezone.utc).date().isoformat()

        research_summary = _build_research_summary(
            b1=research.get("b1", {}),
            b2=research.get("b2", {}),
            b3=research.get("b3", {}),
        )

        # --- D1: Output generation ---
        d1_inputs = {
            "company_canonical_name": company_name,
            "primary_persona": primary_persona,
            "company_industry_label": industry_label,
            "assessment_date": date_str,
            "c2_output_json": synthesis.get("c2", {}),
            "c3_output_json": synthesis.get("c3", {}),
            "research_outputs_summary_json": research_summary,
        }
        d1_result = await asyncio.get_event_loop().run_in_executor(
            None, self.d1.run, d1_inputs
        )
        agent_costs.append(_agent_cost_record("D1_output", d1_result))

        if not d1_result.success:
            _audit("d1_failed", prospect_id=prospect_id, details={"error": d1_result.error}, severity="error")
            return {
                "success": False,
                "error": f"D1 output generation failed: {d1_result.error}",
                "d1": None,
                "d2": None,
                "validation_passed": False,
                "phase_elapsed_s": _elapsed_s(phase_start),
                "agent_costs": agent_costs,
            }

        d1_data = d1_result.data

        # --- D2: Validation ---
        all_research = {
            "b1": research.get("b1", {}),
            "b2": research.get("b2", {}),
            "b3": research.get("b3", {}),
        }
        # Pass questionnaire responses to D2 for fact-grounding checks
        responses_list = (questionnaire_responses or {}).get("responses", [])

        d2_inputs = {
            "d1_output_json": d1_data,
            "c2_output_json": synthesis.get("c2", {}),
            "research_outputs_json": all_research,
            "questionnaire_responses_json": responses_list,
        }
        d2_result = await asyncio.get_event_loop().run_in_executor(
            None, self.d2.run, d2_inputs
        )
        agent_costs.append(_agent_cost_record("D2_validation", d2_result))

        if not d2_result.success:
            _audit("d2_failed", prospect_id=prospect_id, details={"error": d2_result.error}, severity="warning")
            d2_data = {"overall_validation_passed": None, "blocking_issues": [], "validation_flags": []}
            validation_passed = None
        else:
            d2_data = d2_result.data
            validation_passed = d2_data.get("overall_validation_passed", True)

        elapsed = _elapsed_s(phase_start)
        sla_warning = _check_sla("output", elapsed)

        _audit(
            "output_completed",
            prospect_id=prospect_id,
            details={
                "validation_passed": validation_passed,
                "blocking_issues_count": len(d2_data.get("blocking_issues", [])),
                "warning_flags_count": sum(
                    1 for f in d2_data.get("validation_flags", []) if f.get("severity") == "warning"
                ),
                "elapsed_s": elapsed,
                "sla_warning": sla_warning,
            },
        )

        return {
            "success": True,
            "d1": d1_data,
            "d2": d2_data,
            "validation_passed": validation_passed,
            "phase_elapsed_s": elapsed,
            "sla_warning": sla_warning,
            "agent_costs": agent_costs,
        }

    # ------------------------------------------------------------------
    # Full pipeline
    # ------------------------------------------------------------------

    async def run_full_pipeline(
        self,
        submission: dict,
        questionnaire_responses: dict,
    ) -> dict:
        """Execute the complete diagnostic pipeline end to end.

        Phases:
            1. Intake (A1)
            2. Research (B1/B2/B3 parallel)
            3. Synthesis (C1 -> C2 -> C3)
            4. Output (D1 -> D2)

        Args:
            submission: Raw prospect submission (see run_intake() for fields).
            questionnaire_responses: Dict with 'responses' list of response dicts.

        Returns:
            Complete result dict with all phase outputs, timing, SLA warnings,
            and cost tracking.
        """
        pipeline_start = time.time()
        pipeline_id = str(uuid.uuid4())

        _audit("pipeline_started", details={"pipeline_id": pipeline_id})

        timing: Dict[str, float] = {}
        sla_warnings: List[str] = []
        agent_costs: List[Dict[str, Any]] = []

        # ---- Phase 1: Intake ----
        t0 = time.time()
        intake_result = await self.run_intake(submission)
        timing["intake_s"] = _elapsed_s(t0)
        agent_costs.extend(intake_result.get("agent_costs", []))

        if intake_result.get("sla_warning"):
            sla_warnings.append(intake_result["sla_warning"])

        if not intake_result.get("success", False):
            return self._pipeline_error(
                pipeline_id=pipeline_id,
                phase="intake",
                error=intake_result.get("error", "Intake failed"),
                timing=timing,
                sla_warnings=sla_warnings,
                agent_costs=agent_costs,
                pipeline_start=pipeline_start,
            )

        prospect_id = intake_result["prospect_id"]
        normalized = intake_result["normalized"]
        primary_persona = intake_result["primary_persona"]

        # ---- Phase 2: Research ----
        t0 = time.time()
        research_result = await self.run_research(
            prospect_id=prospect_id,
            normalized=normalized,
        )
        timing["research_s"] = _elapsed_s(t0)
        agent_costs.extend(research_result.get("agent_costs", []))
        if research_result.get("sla_warning"):
            sla_warnings.append(research_result["sla_warning"])

        # ---- Phase 3: Synthesis ----
        t0 = time.time()
        synthesis_result = await self.run_synthesis(
            prospect_id=prospect_id,
            questionnaire_responses=questionnaire_responses,
            research=research_result,
            normalized=normalized,
            primary_persona=primary_persona,
        )
        timing["synthesis_s"] = _elapsed_s(t0)
        agent_costs.extend(synthesis_result.get("agent_costs", []))
        if synthesis_result.get("sla_warning"):
            sla_warnings.append(synthesis_result["sla_warning"])

        if not synthesis_result.get("success", True):
            return self._pipeline_error(
                pipeline_id=pipeline_id,
                phase="synthesis",
                error=synthesis_result.get("error", "Synthesis failed"),
                timing=timing,
                sla_warnings=sla_warnings,
                agent_costs=agent_costs,
                pipeline_start=pipeline_start,
                partial={
                    "intake": intake_result,
                    "research": research_result,
                    "synthesis_partial": synthesis_result,
                },
            )

        # ---- Phase 4: Output ----
        t0 = time.time()
        output_result = await self.run_output(
            prospect_id=prospect_id,
            synthesis=synthesis_result,
            research=research_result,
            normalized=normalized,
            primary_persona=primary_persona,
            questionnaire_responses=questionnaire_responses,
        )
        timing["output_s"] = _elapsed_s(t0)
        agent_costs.extend(output_result.get("agent_costs", []))
        if output_result.get("sla_warning"):
            sla_warnings.append(output_result["sla_warning"])

        # ---- Aggregate ----
        total_elapsed = _elapsed_s(pipeline_start)
        timing["total_s"] = total_elapsed
        pipeline_sla = _check_sla("full_pipeline", total_elapsed)
        if pipeline_sla:
            sla_warnings.append(pipeline_sla)

        _audit(
            "pipeline_completed",
            prospect_id=prospect_id,
            details={
                "pipeline_id": pipeline_id,
                "total_elapsed_s": total_elapsed,
                "sla_warnings": sla_warnings,
                "validation_passed": output_result.get("validation_passed"),
                "overall_score": synthesis_result.get("c2", {}).get("overall_score") if synthesis_result.get("c2") else None,
                "tier": synthesis_result.get("c2", {}).get("tier") if synthesis_result.get("c2") else None,
            },
        )

        return {
            "pipeline_id": pipeline_id,
            "prospect_id": prospect_id,
            "success": True,
            "phases": {
                "intake": intake_result,
                "research": research_result,
                "synthesis": synthesis_result,
                "output": output_result,
            },
            "timing": timing,
            "sla_warnings": sla_warnings,
            "agent_costs": agent_costs,
            "cost_summary": self._summarise_costs(agent_costs),
            "validation_passed": output_result.get("validation_passed"),
            "scorecard_content": output_result.get("d1", {}).get("scorecard_content"),
            "quick_wins_memo_content": output_result.get("d1", {}).get("quick_wins_memo_content"),
            "findings_appendix_content": output_result.get("d1", {}).get("findings_appendix_content"),
            "validation_output": output_result.get("d2"),
            "overall_score": synthesis_result.get("c2", {}).get("overall_score"),
            "tier": synthesis_result.get("c2", {}).get("tier"),
        }

    # ------------------------------------------------------------------
    # Demo scenario runner
    # ------------------------------------------------------------------

    async def run_demo_scenario(self, fixture_name: str) -> dict:
        """Run the full pipeline on a named demo fixture.

        Uses the pre-built fixture data from src.data.fixtures.*. Each fixture
        contains a realistic prospect profile and questionnaire responses with
        expected scoring outcomes documented for QA.

        Args:
            fixture_name: One of "meridian_fs" | "northern_care" | "aurelian_tech"

        Returns:
            Full pipeline result dict (same structure as run_full_pipeline).

        Raises:
            ValueError: If fixture_name is not recognised.
        """
        _KNOWN_FIXTURES = ("meridian_fs", "northern_care", "aurelian_tech")
        if fixture_name not in _KNOWN_FIXTURES:
            raise ValueError(
                f"Unknown fixture '{fixture_name}'. "
                f"Available fixtures: {list(_KNOWN_FIXTURES)}"
            )

        # Import fixture data lazily to avoid circular imports
        if fixture_name == "meridian_fs":
            from src.data.fixtures.meridian_fs import MERIDIAN_FS_FIXTURE as fx
        elif fixture_name == "northern_care":
            from src.data.fixtures.northern_care import NORTHERN_CARE_FIXTURE as fx
        else:
            from src.data.fixtures.aurelian_tech import AURELIAN_TECH_FIXTURE as fx

        prospect = fx["prospect"]
        responses = fx["responses"]

        # Build submission dict in the format run_intake() expects
        # Fixture uses primary_contact_* keys; normalize here.
        submission = {
            "prospect_name": prospect.get("prospect_name") or prospect.get("primary_contact_name", "Demo User"),
            "prospect_role": prospect.get("prospect_role") or prospect.get("primary_contact_title", "Executive"),
            "prospect_email": prospect.get("prospect_email") or prospect.get("primary_contact_email", "demo@example.com"),
            "company_name_raw": prospect.get("company_name") or prospect.get("company_canonical_name", ""),
            "company_website": prospect.get("company_website", ""),
            "primary_persona": prospect.get("persona", "P1"),
        }

        questionnaire_responses = {"responses": responses}

        _audit(
            "demo_scenario_started",
            details={"fixture_name": fixture_name, "company": submission["company_name_raw"]},
        )

        return await self.run_full_pipeline(submission, questionnaire_responses)

    # ------------------------------------------------------------------
    # Internal utilities
    # ------------------------------------------------------------------

    def _infer_persona(self, prospect_role: str, industry: str) -> str:
        """Simple rule-based persona inference from job title.

        This is a lightweight fallback. The full A2 persona agent provides
        higher-quality inference when implemented.
        """
        role_lower = prospect_role.lower()

        # P3 signals
        if any(k in role_lower for k in ("cfo", "finance", "financial", "treasurer", "controller", "vp finance")):
            return "P3"

        # P2 signals
        if any(k in role_lower for k in ("cto", "cio", "engineer", "architect", "infrastructure", "it director", "technology director", "informatics", "devops", "platform")):
            return "P2"

        # P1 default (CEO, CDO, CMO, COO, board, strategy, general management)
        return "P1"

    def _pipeline_error(
        self,
        pipeline_id: str,
        phase: str,
        error: str,
        timing: dict,
        sla_warnings: list,
        agent_costs: list,
        pipeline_start: float,
        partial: Optional[dict] = None,
    ) -> dict:
        """Build a standardised pipeline error response."""
        timing["total_s"] = _elapsed_s(pipeline_start)
        _audit(
            "pipeline_failed",
            details={"pipeline_id": pipeline_id, "failed_phase": phase, "error": error},
            severity="error",
        )
        return {
            "pipeline_id": pipeline_id,
            "success": False,
            "failed_phase": phase,
            "error": error,
            "timing": timing,
            "sla_warnings": sla_warnings,
            "agent_costs": agent_costs,
            "cost_summary": self._summarise_costs(agent_costs),
            "partial": partial or {},
        }

    def _summarise_costs(self, agent_costs: list) -> dict:
        """Summarise cost tracking across all agent calls."""
        total_latency_ms = sum(c.get("latency_ms", 0) for c in agent_costs)
        successful_calls = sum(1 for c in agent_costs if c.get("success"))
        failed_calls = sum(1 for c in agent_costs if not c.get("success"))

        return {
            "total_agent_calls": len(agent_costs),
            "successful_calls": successful_calls,
            "failed_calls": failed_calls,
            "total_latency_ms": total_latency_ms,
            "input_tokens_total": None,   # TODO: implement when token tracking added
            "output_tokens_total": None,  # TODO: implement when token tracking added
            "estimated_cost_usd": None,   # TODO: implement when token counts available
            "per_agent": agent_costs,
        }
