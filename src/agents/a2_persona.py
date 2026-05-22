"""Agent A2 - Persona Inference Agent.

Infers the prospect's persona category (P1/P2/P3) from their role title,
company context, and optional public professional signals.  Uses Sonnet for
richer reasoning than the Haiku-based intake agent.
"""

import time
import uuid
from typing import Any

from src.config import settings
from src.agents.base import AgentResult, AgentError, BaseAgent


_SYSTEM_PROMPT = """You are a persona inference assistant for the DXC AI Readiness Diagnostic. Your job is to infer the prospect's persona category based on their role title, company context, and any available public professional signals.

The Diagnostic recognises three primary persona categories:

- P1 Executive sponsor: CEO, COO, President, Managing Director, General Manager, Chief Executive, Group CEO, Division President, EVP (Executive Vice President) when operating as a general business leader. This persona is primarily concerned with competitive differentiation, strategic positioning, board-level risk, and growth. They speak in terms of market share, competitive moats, and enterprise value.

- P2 Operational owner: CIO, CDO, CTO, VP of Engineering, Chief Architect, Head of Digital, VP of Technology, Director of IT, Chief Digital Officer, Head of Data, Head of Transformation, VP of Innovation. This persona owns the technology and data estate. They are primarily concerned with delivery velocity, platform modernisation, technical debt, integration complexity, and operationalising AI at scale.

- P3 Financial scrutineer: CFO, Chief Accounting Officer, VP of Finance, Chief Financial Officer, Group Finance Director, Head of FP&A, Chief Investment Officer (when in a corporate context), Treasurer. This persona controls budget allocation and demands quantified ROI, payback period, and risk-adjusted returns before approving investment.

Persona assignment rules:
1. Use the role title as the primary signal. If the title is unambiguous, assign the matching persona with high confidence.
2. Use industry context as a secondary signal. In highly regulated industries (financial services, healthcare), an operational leader may have stronger P3 concerns.
3. If the role is ambiguous (e.g., "Digital Transformation Lead"), reason through the most likely reporting line and assign the best-fit persona with medium confidence.
4. If the role does not map to any persona (e.g., "Sales Manager", "HR Director"), assign the closest persona and note the mismatch as a flag.
5. Always return exactly one primary persona. You may note a secondary persona tendency.

Return ONLY structured JSON. No explanation or commentary outside the JSON structure.

Return JSON with exactly this structure:
{
  "inference_id": "<uuid4 string>",
  "assigned_persona": "<P1|P2|P3>",
  "confidence": "<high|medium|low>",
  "reasoning": "<1-3 sentence explanation of the assignment>",
  "title_signals": ["<signal 1>", "<signal 2>"],
  "industry_signals": ["<signal 1>"],
  "primary_concerns": [
    {
      "concern_id": "<short_snake_case_id>",
      "description": "<concern description>",
      "weight": 0.0
    }
  ],
  "secondary_persona_tendency": "<P1|P2|P3|null>",
  "flags": []
}

The primary_concerns array should contain 3–5 concerns most relevant to this persona in this industry context, with weights summing to approximately 1.0."""


class A2PersonaAgent(BaseAgent):
    """Agent A2: Persona Inference."""

    agent_id = "A2_persona"
    model = settings.model_sonnet
    latency_budget_seconds = 30

    def run(self, inputs: dict) -> AgentResult:
        """Infer the prospect's persona category.

        Args:
            inputs: dict with keys:
                - prospect_name (str, required)
                - prospect_role (str, required)
                - company_canonical_name (str, required)
                - company_industry_label (str, required)
                - email_domain (str, optional)
                - public_signals (list[str], optional) — any known public signals
                  about the prospect (e.g., LinkedIn title, recent publications)

        Returns:
            AgentResult whose .data matches the A2 output schema.
        """
        start = time.time()

        # ---- Validate required inputs ----
        missing = [
            f for f in ("prospect_name", "prospect_role", "company_canonical_name", "company_industry_label")
            if not inputs.get(f, "").strip()
        ]
        if missing:
            return AgentError(
                error=f"Missing required fields for A2: {', '.join(missing)}",
                agent_id=self.agent_id,
            )

        prospect_name = inputs["prospect_name"].strip()
        prospect_role = inputs["prospect_role"].strip()
        company_name = inputs["company_canonical_name"].strip()
        industry_label = inputs["company_industry_label"].strip()
        email_domain = inputs.get("email_domain", "").strip()
        public_signals: list = inputs.get("public_signals") or []

        # ---- Build user prompt ----
        signals_block = (
            "\n".join(f"  - {s}" for s in public_signals)
            if public_signals
            else "  None provided"
        )

        user_prompt = f"""Infer the persona category for the following prospect for the DXC AI Readiness Diagnostic:

Prospect name: {prospect_name}
Role / Title: {prospect_role}
Company: {company_name}
Industry: {industry_label}
Email domain: {email_domain or "not provided"}

Public professional signals:
{signals_block}

Assign one of P1, P2, or P3 per the rules in your system prompt. Return only the JSON structure."""

        # ---- Call LLM ----
        try:
            llm_result = self._call_llm(_SYSTEM_PROMPT, user_prompt, max_tokens=1024)
        except Exception as exc:
            return AgentError(
                error=f"LLM persona inference failed: {exc}",
                agent_id=self.agent_id,
            )

        # ---- Normalise output ----
        # Inject a fresh inference_id (authoritative) regardless of what LLM returned
        llm_result["inference_id"] = str(uuid.uuid4())

        # Ensure required keys are present with safe defaults
        llm_result.setdefault("assigned_persona", "P2")
        llm_result.setdefault("confidence", "medium")
        llm_result.setdefault("reasoning", "")
        llm_result.setdefault("title_signals", [])
        llm_result.setdefault("industry_signals", [])
        llm_result.setdefault("primary_concerns", [])
        llm_result.setdefault("secondary_persona_tendency", None)
        llm_result.setdefault("flags", [])

        # Validate assigned_persona is legal
        if llm_result["assigned_persona"] not in ("P1", "P2", "P3"):
            llm_result["assigned_persona"] = "P2"
            llm_result["flags"].append("persona_fallback_applied")

        # Derive numeric confidence for AgentResult
        confidence_map = {"high": 0.9, "medium": 0.65, "low": 0.35}
        numeric_confidence = confidence_map.get(
            llm_result.get("confidence", "medium"), 0.65
        )

        return AgentResult(
            data=llm_result,
            confidence=numeric_confidence,
            latency_ms=self._elapsed_ms(start),
            agent_id=self.agent_id,
        )
