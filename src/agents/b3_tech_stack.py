"""Agent B3 - Tech Stack Inference Agent.

Infers the prospect company's technology posture using LLM reasoning grounded
in the company's name, industry, size band, and geography.  For V0 there is no
confirmed external data source for tech stack (LinkedIn/Indeed have no public
APIs); confidence tiers therefore reflect "probable" or "possible" inference,
never "confirmed".

The LLM is instructed to use its training knowledge about common technology
choices in each industry/size/geography combination, and about any publicly
known technology partnerships or announcements from the specific company.
"""

import json
import time
import uuid
from typing import Any

from src.config import settings
from src.agents.base import AgentResult, AgentError, BaseAgent


_SYSTEM_PROMPT = """You are a technology stack inference assistant for the DXC AI Readiness Diagnostic. Your job is to infer the likely technology stack and AI readiness posture of a prospect company based on their name, industry, size, and geography.

Important: You are performing inference from your training knowledge, not confirmed data. All confidence tiers must be "probable" or "possible" — never "confirmed". Use "not_detected" only for categories where there is no plausible signal at all.

For the given company, infer:
1. Cloud platform(s) — AWS, Azure, GCP, hybrid, on-premises
2. ERP system(s) — SAP, Oracle ERP Cloud, Microsoft Dynamics 365, Workday, etc.
3. CRM system(s) — Salesforce, HubSpot, Microsoft Dynamics CRM, etc.
4. Data warehouse / lakehouse — Snowflake, Databricks, BigQuery, Azure Synapse, Redshift, etc.
5. ML/AI platform(s) — Azure ML, SageMaker, Vertex AI, Databricks MLflow, DataRobot, etc.
6. RPA tools — UiPath, Automation Anywhere, Blue Prism, Microsoft Power Automate
7. Collaboration platform — Microsoft 365 / Teams, Google Workspace, Slack
8. Analytics and BI — Tableau, Power BI, Looker, Qlik, MicroStrategy
9. Any existing AI tools or GenAI products in use

For each detected platform:
- Set confidence_tier to "probable" if this is a very common choice for this industry/size/geography combination or if there is a known public signal
- Set confidence_tier to "possible" if this is a plausible but not dominant choice
- Populate evidence with specific reasoning (e.g., "Common ERP choice for global manufacturing companies of this size", "AWS partnership announced at re:Invent 2023")

Also assess:
- Cloud maturity: none | basic | intermediate | advanced
- Data platform maturity: none | basic | intermediate | advanced
- Overall tech readiness for AI: high | medium | low
- Any tech debt signals (e.g., "likely legacy mainframe estate given banking industry and size", "probable on-premise SAP S/4HANA estate")
- Any AI readiness signals from known public announcements

Return ONLY structured JSON. No explanation outside the JSON structure.

Return JSON with exactly this structure:
{
  "inference_id": "<uuid4>",
  "inference_method": "llm_training_knowledge",
  "platforms_detected": [
    {
      "platform_name": "<string>",
      "category": "<cloud|erp|crm|data_warehouse|ml_platform|rpa|collaboration|analytics|other>",
      "confidence_tier": "<probable|possible|not_detected>",
      "evidence": ["<evidence string 1>", "<evidence string 2>"],
      "ai_readiness_signal": "<string or null — what does this platform's presence imply for AI readiness>"
    }
  ],
  "cloud_maturity": "<none|basic|intermediate|advanced>",
  "data_platform_maturity": "<none|basic|intermediate|advanced>",
  "existing_ai_tools": ["<tool or product name>"],
  "tech_debt_signals": ["<signal description>"],
  "overall_tech_readiness": "<high|medium|low>",
  "inference_rationale": "<2-3 sentence summary of the reasoning behind the assessment>",
  "notes": "<any important caveats about inference confidence or known gaps>",
  "confidence": "<high|medium|low>"
}

Note: "confidence" in the output refers to confidence in the overall inference, not the individual platform confidence_tier values. Given this is pure LLM inference without external tool data, the maximum overall confidence level is "medium"."""


class B3TechStackAgent(BaseAgent):
    """Agent B3: Tech Stack Inference."""

    agent_id = "B3_tech_stack"
    model = settings.model_sonnet
    latency_budget_seconds = 60

    def run(self, inputs: dict) -> AgentResult:
        """Infer the prospect company's technology stack and AI readiness posture.

        Args:
            inputs: dict with keys:
                - company_canonical_name (str, required)
                - company_industry_label (str, optional)
                - company_size_band_estimate (str, optional)
                  — "mid-market", "large", "global", or "unknown"
                - company_hq_country (str, optional)
                - prospect_id (str, optional)
                - financial_signals (list[str], optional) — AI/digital signals
                  from B1 agent (digital_transformation_signals, ai_investment_signals)
                - news_signals (list[str], optional) — AI signals from B2 agent

        Returns:
            AgentResult whose .data matches the B3 output schema (TechStackInference).
        """
        start = time.time()

        company_name = (inputs.get("company_canonical_name") or "").strip()
        if not company_name:
            return AgentError(
                error="company_canonical_name is required for B3 tech stack inference",
                agent_id=self.agent_id,
            )

        industry_label = (inputs.get("company_industry_label") or "").strip()
        size_band = (inputs.get("company_size_band_estimate") or "unknown").strip()
        hq_country = (inputs.get("company_hq_country") or "").strip()
        prospect_id = (inputs.get("prospect_id") or "").strip()

        # Optional upstream signals to ground the inference
        financial_signals: list = inputs.get("financial_signals") or []
        news_signals: list = inputs.get("news_signals") or []

        # ---- Build LLM prompt ----
        financial_block = (
            "Financial/EDGAR signals:\n" + "\n".join(f"  - {s}" for s in financial_signals)
            if financial_signals
            else "Financial/EDGAR signals: none provided"
        )
        news_block = (
            "News signals:\n" + "\n".join(f"  - {s}" for s in news_signals)
            if news_signals
            else "News signals: none provided"
        )

        user_prompt = f"""Infer the technology stack and AI readiness posture for the following company for the DXC AI Readiness Diagnostic:

Company: {company_name}
Industry: {industry_label or "unknown"}
Size band: {size_band}
HQ country: {hq_country or "unknown"}

Additional context from upstream research:
{financial_block}
{news_block}

Remember: All inference is from your training knowledge. Set all platform confidence_tier values to "probable" or "possible" only (never "confirmed"). Set overall "confidence" to at most "medium".

Return only the JSON structure as specified in your system prompt."""

        try:
            llm_result = self._call_llm(_SYSTEM_PROMPT, user_prompt, max_tokens=3000)
        except Exception as exc:
            return AgentError(
                error=f"LLM tech stack inference failed: {exc}",
                agent_id=self.agent_id,
            )

        # ---- Normalise output ----
        llm_result["inference_id"] = str(uuid.uuid4())
        llm_result["prospect_id"] = prospect_id
        llm_result.setdefault("inference_method", "llm_training_knowledge")
        llm_result.setdefault("platforms_detected", [])
        llm_result.setdefault("cloud_maturity", "basic")
        llm_result.setdefault("data_platform_maturity", "basic")
        llm_result.setdefault("existing_ai_tools", [])
        llm_result.setdefault("tech_debt_signals", [])
        llm_result.setdefault("overall_tech_readiness", "medium")
        llm_result.setdefault("inference_rationale", "")
        llm_result.setdefault("notes", "Inference based on LLM training knowledge; no external tool data used.")
        llm_result.setdefault("confidence", "medium")

        # Enforce confidence ceiling for pure LLM inference
        if llm_result.get("confidence") == "high":
            llm_result["confidence"] = "medium"
            llm_result["notes"] = (
                llm_result.get("notes", "") +
                " [Confidence capped at 'medium' — no external tool data available for V0.]"
            ).strip()

        # Enforce confidence_tier constraints on each platform
        valid_tiers = {"probable", "possible", "not_detected"}
        for platform in llm_result.get("platforms_detected", []):
            tier = platform.get("confidence_tier", "possible")
            if tier not in valid_tiers or tier == "confirmed":
                platform["confidence_tier"] = "probable"

        confidence_map = {"high": 0.7, "medium": 0.5, "low": 0.3}
        # B3 is always inference-only in V0, so we cap numeric confidence at 0.65
        numeric_confidence = min(
            confidence_map.get(llm_result.get("confidence", "medium"), 0.5),
            0.65,
        )

        # Small boost if upstream signals were provided
        if financial_signals or news_signals:
            numeric_confidence = min(numeric_confidence + 0.05, 0.65)

        return AgentResult(
            data=llm_result,
            confidence=numeric_confidence,
            latency_ms=self._elapsed_ms(start),
            agent_id=self.agent_id,
        )
