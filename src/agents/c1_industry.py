"""Agent C1 - Industry Process Library Agent.

Maps the prospect's industry to applicable AI processes from the DXC
Industry Process Library. For V0, full coverage exists for Financial
Services (FS), Healthcare & Life Sciences (HLS), and Manufacturing (MFG).
All other industries receive Tier 1 universal patterns only, with a V0.5
gap flag raised.

Model: claude-sonnet-4-6
"""

from __future__ import annotations

import json
import time
from typing import Any

from src.config import settings
from src.agents.base import AgentResult, AgentError, BaseAgent
from src.data.industry_library import get_processes_for_industry


_SYSTEM_PROMPT = """You are the Industry Process Library Agent (C1) for the DXC AI Readiness Diagnostic.

Your role is to analyse a prospect's industry profile and map it to the most applicable AI-reinvention processes from the DXC Industry Process Library. You reason with precision about which processes match the prospect's profile and produce output the synthesis agent can act on directly.

## Your responsibilities

1. Review the structured industry library data provided to you — it has already been filtered for the prospect's industry and size band.

2. Select and prioritise the applicable processes from this filtered library. Do not invent processes not present in the library data.

3. For each selected process, evaluate:
   - Relevance to the prospect's size band and business model
   - Whether prerequisites are likely met based on the company profile
   - Priority ranking (highest potential value first)

4. Identify any meaningful coverage gaps — processes that would be relevant but are not in the V0 library. Flag these clearly as V0.5 gaps.

5. Assess confidence in your mapping based on the quality of the industry/NAICS classification provided.

## Tier definitions

- **Tier 1**: Universal processes applicable across all industries (document processing, knowledge management, customer service AI, procurement analytics)
- **Tier 2**: Industry-specific high-priority processes with clear ROI and broad applicability within the vertical
- **Tier 3**: Advanced industry-specific processes with higher prerequisites and complexity

## Output format

Return ONLY valid JSON matching this structure exactly:

```json
{
  "library_status": "<full_coverage|partial_coverage|tier1_only>",
  "industry_match": "<exact|adjacent|not_in_library>",
  "matched_vertical": "<Financial Services|Healthcare & Life Sciences|Manufacturing|null>",
  "applicable_processes": [
    {
      "process_id": "<string>",
      "process_name": "<string>",
      "tier": <1|2|3>,
      "relevance_rationale": "<1-2 sentences specific to this prospect>",
      "priority_rank": <integer starting at 1>,
      "prerequisite_assessment": "<met|likely_met|uncertain|likely_not_met>",
      "top_sub_processes": ["<sub_process_name>", "..."]
    }
  ],
  "coverage_gaps": "<string describing gaps, or empty string if none>",
  "v05_gap_flagged": <true|false>,
  "confidence": <0.0 to 1.0>,
  "confidence_rationale": "<brief explanation of confidence level>"
}
```

## Rules

- Be specific to the prospect. Do not write generic descriptions.
- Priority rank 1 = highest value/relevance to this specific prospect.
- If library_status is tier1_only, applicable_processes contains only Tier 1 entries.
- prerequisite_assessment must reference the prospect's known characteristics.
- confidence reflects how certain you are the industry mapping is correct, not how good the prospect is.
- Do not add fields not shown in the output structure above.
- Do not include explanatory text outside the JSON block.
"""


class C1IndustryAgent(BaseAgent):
    """Agent C1: Industry Process Library Mapping.

    Loads the industry library from src.data.industry_library, filters it
    for the prospect's industry and size band, then uses the LLM to produce
    a prioritised, prospect-specific process mapping.
    """

    agent_id = "C1_industry"
    model = settings.model_sonnet
    latency_budget_seconds = 45

    def run(self, inputs: dict) -> AgentResult:
        """Map the prospect to applicable industry processes.

        Args:
            inputs: dict with keys:
                - company_industry_label (str, required)
                - company_industry_naics (str, optional)
                - company_size_band_estimate (str, optional — mid-market|large|global|unknown)
                - company_canonical_name (str, optional — used for context)
                - business_model_signals (list[str], optional)

        Returns:
            AgentResult whose .data matches the C1 output schema.
        """
        start = time.time()

        industry_label = inputs.get("company_industry_label", "").strip()
        naics_code = inputs.get("company_industry_naics", "").strip()
        size_band = inputs.get("company_size_band_estimate", "unknown").strip()
        company_name = inputs.get("company_canonical_name", "the prospect").strip()
        business_model_signals = inputs.get("business_model_signals", [])

        if not industry_label:
            return AgentError(
                error="company_industry_label is required for C1 industry mapping.",
                agent_id=self.agent_id,
            )

        # --- Step 1: Load and pre-filter the library ---
        try:
            library_data = get_processes_for_industry(
                industry_label=industry_label,
                naics_code=naics_code,
            )
        except Exception as exc:
            return AgentError(
                error=f"Industry library lookup failed: {exc}",
                agent_id=self.agent_id,
            )

        # --- Step 2: Call LLM for prospect-specific mapping ---
        user_prompt = self._build_user_prompt(
            company_name=company_name,
            industry_label=industry_label,
            naics_code=naics_code,
            size_band=size_band,
            business_model_signals=business_model_signals,
            library_data=library_data,
        )

        try:
            llm_result = self._call_llm(
                system_prompt=_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                max_tokens=3000,
            )
        except Exception as exc:
            return AgentError(
                error=f"LLM call failed in C1: {exc}",
                agent_id=self.agent_id,
            )

        # --- Step 3: Merge library metadata with LLM output ---
        output = {
            "library_status": llm_result.get(
                "library_status", library_data["library_status"]
            ),
            "industry_match": llm_result.get(
                "industry_match", library_data["industry_match"]
            ),
            "matched_vertical": llm_result.get(
                "matched_vertical", library_data.get("matched_vertical")
            ),
            "applicable_processes": llm_result.get("applicable_processes", []),
            "coverage_gaps": llm_result.get(
                "coverage_gaps", library_data.get("coverage_gaps", "")
            ),
            "v05_gap_flagged": llm_result.get(
                "v05_gap_flagged", library_data.get("v05_gap_flagged", False)
            ),
            "confidence": float(llm_result.get("confidence", 0.7)),
            "confidence_rationale": llm_result.get("confidence_rationale", ""),
            # Metadata
            "total_library_processes_evaluated": len(library_data["processes"]),
            "total_processes_selected": len(llm_result.get("applicable_processes", [])),
        }

        confidence = output["confidence"]

        return AgentResult(
            data=output,
            confidence=confidence,
            latency_ms=self._elapsed_ms(start),
            agent_id=self.agent_id,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_user_prompt(
        self,
        company_name: str,
        industry_label: str,
        naics_code: str,
        size_band: str,
        business_model_signals: list,
        library_data: dict,
    ) -> str:
        """Build the user prompt with prospect context and library data."""
        processes_json = json.dumps(library_data["processes"], indent=2)
        signals_text = (
            "\n".join(f"  - {s}" for s in business_model_signals)
            if business_model_signals
            else "  (none provided)"
        )

        return f"""## Prospect Profile

Company: {company_name}
Industry label (as submitted): {industry_label}
NAICS code: {naics_code or "not provided"}
Size band: {size_band}
Business model signals:
{signals_text}

## Library Pre-Filter Result

Library status: {library_data["library_status"]}
Industry match type: {library_data["industry_match"]}
Matched vertical: {library_data.get("matched_vertical", "None")}
Pre-existing coverage gap note: {library_data.get("coverage_gaps", "None")}
V0.5 gap flagged by library: {library_data.get("v05_gap_flagged", False)}

## Filtered Industry Process Library

The following processes have already been filtered for this prospect's industry.
Map them to the prospect and produce your prioritised output.

```json
{processes_json}
```

Now produce the JSON output as specified in your system prompt.
Be specific to {company_name} — do not write generic descriptions.
"""
