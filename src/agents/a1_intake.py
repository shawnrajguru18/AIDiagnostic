"""Agent A1 - Intake Validation Agent.

Validates and normalises prospect submission data before it enters the
diagnostic pipeline.  Company resolution and industry classification are
delegated to the LLM (Haiku); everything else is rule-based.
"""

import re
import time
import uuid
from typing import Any

from src.config import settings
from src.agents.base import AgentResult, AgentError, BaseAgent


_SYSTEM_PROMPT = """You are an intake validation assistant for the DXC AI Readiness Diagnostic. Your job is to validate and normalize prospect submission data and prepare it for downstream processing.

Given a prospect submission, you will:
1. Validate that the company name resolves to a real, identifiable enterprise
2. Identify the canonical company name
3. Identify the company's industry classification (use NAICS or equivalent)
4. Identify the company's likely SEC ticker or LEI if publicly traded
5. Identify the company's primary geography (HQ country, major operating jurisdictions)
6. Flag any submission that appears malformed, test-data, or fraudulent

Return ONLY structured JSON. Do not include explanation or commentary outside the JSON structure.

If the company is ambiguous, return a list of candidates with reasoning.
If the company appears to be a placeholder or test data, flag it but do not reject.

Return JSON with exactly this structure:
{
  "validation_status": "<valid|ambiguous|flagged|rejected>",
  "company_canonical_name": "<string>",
  "company_ticker": "<string or null>",
  "company_lei": "<string or null>",
  "company_industry_naics": "<string>",
  "company_industry_label": "<string>",
  "company_hq_country": "<string>",
  "company_size_band_estimate": "<mid-market|large|global|unknown>",
  "disambiguation_candidates": [],
  "flags": [],
  "confidence": {
    "company_resolution": 0.0,
    "industry_classification": 0.0
  }
}"""


# Simple email regex (RFC 5322 simplified)
_EMAIL_RE = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
)

# Known test/placeholder company names
_TEST_COMPANY_NAMES = frozenset(
    {
        "test", "testco", "test company", "acme", "acme corp", "acme corporation",
        "example", "example inc", "example corp", "foo", "bar", "foobar",
        "placeholder", "dummy", "demo company", "my company", "company name",
        "your company", "na", "n/a", "tbd", "unknown",
    }
)


class A1IntakeAgent(BaseAgent):
    """Agent A1: Intake Validation."""

    agent_id = "A1_intake"
    model = settings.model_haiku
    latency_budget_seconds = 30

    # ------------------------------------------------------------------
    # Rule-based validation helpers
    # ------------------------------------------------------------------

    def _validate_required_fields(self, inputs: dict) -> list[str]:
        """Return a list of validation error messages for missing/empty required fields."""
        errors: list[str] = []
        required = ["prospect_name", "prospect_role", "prospect_email", "company_name_raw"]
        for field in required:
            if not inputs.get(field, "").strip():
                errors.append(f"Missing required field: {field}")
        return errors

    def _validate_email(self, email: str) -> tuple[bool, list[str]]:
        """Validate email format. Returns (is_valid, list_of_flags)."""
        flags: list[str] = []
        if not _EMAIL_RE.match(email):
            return False, [f"Invalid email format: {email!r}"]
        domain = email.split("@")[-1].lower()
        if domain in {"gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com"}:
            flags.append("personal_email_domain")
        return True, flags

    def _check_test_data(self, company_name: str) -> bool:
        """Return True if the company name looks like test/placeholder data."""
        return company_name.strip().lower() in _TEST_COMPANY_NAMES

    # ------------------------------------------------------------------
    # LLM resolution
    # ------------------------------------------------------------------

    def _resolve_company(self, inputs: dict) -> dict:
        """Ask the LLM to resolve company identity and industry."""
        company_name = inputs["company_name_raw"].strip()
        website = inputs.get("company_website", "").strip()
        prospect_email_domain = inputs.get("prospect_email", "").split("@")[-1]

        user_prompt = f"""Resolve and classify the following company for the DXC AI Readiness Diagnostic intake:

Company name (as submitted): {company_name}
Website hint: {website or "not provided"}
Prospect email domain: {prospect_email_domain}
Prospect name: {inputs.get("prospect_name", "")}
Prospect role: {inputs.get("prospect_role", "")}

Return ONLY the JSON structure specified in your system prompt. Use your training knowledge to identify the company and classify it."""

        return self._call_llm(_SYSTEM_PROMPT, user_prompt, max_tokens=1024)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def run(self, inputs: dict) -> AgentResult:
        """Validate and normalise a prospect submission.

        Args:
            inputs: dict with keys:
                - prospect_name (str, required)
                - prospect_role (str, required)
                - prospect_email (str, required)
                - company_name_raw (str, required)
                - company_website (str, optional)

        Returns:
            AgentResult whose .data matches the A1 output schema.
        """
        start = time.time()

        # ---- Step 1: required-field checks ----
        field_errors = self._validate_required_fields(inputs)
        if field_errors:
            return AgentError(
                error="; ".join(field_errors),
                agent_id=self.agent_id,
            )

        prospect_name = inputs["prospect_name"].strip()
        prospect_role = inputs["prospect_role"].strip()
        prospect_email = inputs["prospect_email"].strip()
        company_name_raw = inputs["company_name_raw"].strip()

        flags: list[str] = []
        validation_status = "valid"

        # ---- Step 2: email validation ----
        email_ok, email_flags = self._validate_email(prospect_email)
        if not email_ok:
            return AgentError(
                error=f"Invalid prospect email: {email_flags}",
                agent_id=self.agent_id,
            )
        flags.extend(email_flags)

        # ---- Step 3: test-data detection ----
        if self._check_test_data(company_name_raw):
            flags.append("possible_test_data")
            validation_status = "flagged"

        # ---- Step 4: LLM company resolution ----
        try:
            llm_result = self._resolve_company(inputs)
        except Exception as exc:
            return AgentError(
                error=f"LLM company resolution failed: {exc}",
                agent_id=self.agent_id,
            )

        # Merge LLM flags with rule-based flags
        llm_flags = llm_result.get("flags", [])
        if isinstance(llm_flags, list):
            flags.extend(llm_flags)

        # LLM may override validation_status if it sees stronger signals
        llm_status = llm_result.get("validation_status", "valid")
        status_priority = {"rejected": 4, "flagged": 3, "ambiguous": 2, "valid": 1}
        if status_priority.get(llm_status, 0) > status_priority.get(validation_status, 0):
            validation_status = llm_status

        confidence = llm_result.get("confidence", {})

        output = {
            "validation_status": validation_status,
            "prospect_id": str(uuid.uuid4()),
            "normalized": {
                "prospect_name": prospect_name,
                "prospect_role": prospect_role,
                "prospect_email": prospect_email,
                "company_canonical_name": llm_result.get("company_canonical_name", company_name_raw),
                "company_ticker": llm_result.get("company_ticker"),
                "company_lei": llm_result.get("company_lei"),
                "company_industry_naics": llm_result.get("company_industry_naics", ""),
                "company_industry_label": llm_result.get("company_industry_label", ""),
                "company_hq_country": llm_result.get("company_hq_country", ""),
                "company_size_band_estimate": llm_result.get(
                    "company_size_band_estimate", "unknown"
                ),
            },
            "disambiguation_candidates": llm_result.get("disambiguation_candidates", []),
            "flags": list(dict.fromkeys(flags)),  # deduplicate while preserving order
            "confidence": {
                "company_resolution": float(
                    confidence.get("company_resolution", 0.0)
                ),
                "industry_classification": float(
                    confidence.get("industry_classification", 0.0)
                ),
            },
        }

        overall_confidence = (
            output["confidence"]["company_resolution"]
            + output["confidence"]["industry_classification"]
        ) / 2.0

        return AgentResult(
            data=output,
            confidence=overall_confidence,
            latency_ms=self._elapsed_ms(start),
            agent_id=self.agent_id,
        )
