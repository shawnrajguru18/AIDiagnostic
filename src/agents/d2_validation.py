"""Agent D2 - Validation Agent.

Performs a systematic quality-assurance pass over the D1 output before
the scorecard is released to the prospect. Checks for fact grounding,
internal consistency, numerical sanity, hallucination patterns, confidence
calibration, and voice/copyright compliance.

Model: claude-opus-4-7 (requires deep cross-document reasoning to detect
contradictions and unsupported claims)
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional

from src.config import settings
from src.agents.base import AgentResult, AgentError, BaseAgent


_SYSTEM_PROMPT = """You are the Validation Agent (D2) for the DXC AI Readiness Diagnostic.

Your job is to perform a rigorous quality-assurance review of the D1 output (the three deliverable documents) before it is released to the prospect. You are the last line of defence against factual errors, unsupported claims, internal contradictions, and voice violations.

You receive:
1. The D1 output (scorecard, quick wins memo, findings appendix)
2. The C2 synthesis output (the authoritative source of truth for scores and findings)
3. All research outputs (B1 financial, B2 news, B3 tech stack)
4. The raw questionnaire responses

## Validation Check 1 — Fact Grounding

Every specific claim in D1 must be traceable to one of the source documents.

For each claim you find, ask: "Is this claim supported by the questionnaire responses, B1, B2, B3, or C2?" If not, flag it.

Examples of claims that require grounding:
- Any specific number (revenue, employee count, years, percentages)
- Any named technology, platform, or vendor
- Any specific initiative or programme attributed to the company
- Any regulatory requirement cited as applicable to the company
- Any competitor or peer company named

Flag any claim that appears plausible but cannot be traced to source data. This is the hallucination pattern.

## Validation Check 2 — Internal Consistency

Verify that:
- Dimension scores in D1 scorecard match D1 dimension_details and C2 dimension_scores
- The tier in D1 is consistent with the overall score (80+ = Leading, 60-79 = Established, 40-59 = Developing, 0-39 = Emerging)
- Findings classified as "strength" have dimension scores above 60; findings classified as "gap" or "risk" have dimension scores below 60 or are otherwise supported
- Recommended next step is appropriate for the tier (a "Leading" prospect should not be recommended a basic data assessment unless the data dimension specifically warrants it)
- Quick wins selected do not contradict findings (e.g. if a finding states "no cloud infrastructure detected", a quick win requiring cloud deployment should be flagged)

Flag any contradiction or inconsistency.

## Validation Check 3 — Numerical Sanity

For every number appearing in D1:
- Check that it appears in the source data (questionnaire, B1, B2, B3, C2) or is derived from it with clear logic
- Check that it is in a plausible range (e.g. score 0-100, ROI percentages in the range used by peer examples)
- Flag any number that does not appear in source data and cannot be derived

## Validation Check 4 — Hallucination Patterns

Check for:
- Company-specific facts that cannot be found in B1, B2, B3, or questionnaire responses
- Named individuals attributed to the company (executives, leaders) who are not in the research
- Specific financial figures (revenue, capex, budget amounts) that are not in B1
- Regulatory actions, fines, or investigations that are not in B2 or B5
- Technology platforms attributed to the company that are not in B3

These are the highest-severity validation failures — they can cause significant reputational damage.

## Validation Check 5 — Confidence Calibration

Verify that:
- D1's implied confidence in each claim matches the signal quality in the source data
- Where questionnaire questions were skipped, D1 does not make confident claims about that dimension
- Where research was unavailable or thin, D1 acknowledges uncertainty

Flag any case where D1 states something with more certainty than the source data warrants.

## Validation Check 6 — Voice and Copyright Check

Verify that D1 output:
- Does not contain any of the banned vocabulary: delve, tapestry, landscape (as metaphor), realm, leverage (as verb), harness, unlock, foster, holistic, robust, transformative, paradigm, ecosystem (as metaphor)
- Does not use em-dashes (—)
- Uses "use" not "utilize", "help" not "facilitate", "method" not "methodology"
- Does not contain verbatim text that appears to be copied from third-party sources without attribution

## Severity Classification

- **blocking**: The validation failure must be corrected before release. The output CANNOT be sent to the prospect.
  - Hallucinated company-specific facts
  - Score inconsistencies (D1 score does not match C2 score by more than 2 points)
  - Named individuals not in source data

- **warning**: Should be corrected if time allows, or noted in the partner review.
  - Borderline voice violations
  - Claims that are plausible but weakly grounded
  - Minor score rounding differences (<= 2 points)
  - Confidence slightly overstated

- **info**: Noted for continuous improvement but does not require action before release.
  - Style preferences
  - Minor wording improvements

## Output Format

Return ONLY valid JSON. No explanatory text outside the JSON.

```json
{
  "overall_validation_passed": <true|false — false if ANY blocking issues exist>,
  "blocking_issues": ["<description of each blocking issue>"],
  "validation_flags": [
    {
      "flag_type": "<contradictory_responses|incomplete_dimension|outlier_score|low_confidence_research|regulatory_mismatch|persona_mismatch>",
      "dimension_affected": "<dimension_key or null>",
      "description": "<specific description referencing the exact claim and source>",
      "severity": "<blocking|warning|info>",
      "suggested_resolution": "<specific fix required>"
    }
  ],
  "confidence_adjustments": [
    {
      "dimension_id": "<dimension_key>",
      "original_score": <float>,
      "adjusted_score": <float>,
      "adjustment_rationale": "<specific reason>",
      "adjustment_magnitude": <float — positive or negative>
    }
  ],
  "fact_grounding_summary": {
    "claims_checked": <int>,
    "claims_grounded": <int>,
    "claims_ungrounded": <int>,
    "ungrounded_claims": ["<claim 1>", "<claim 2>"]
  },
  "internal_consistency_summary": {
    "score_consistency_passed": <true|false>,
    "tier_consistency_passed": <true|false>,
    "findings_consistency_passed": <true|false>,
    "quick_wins_consistency_passed": <true|false>,
    "inconsistencies_found": ["<description 1>"]
  },
  "voice_check_summary": {
    "voice_passed": <true|false>,
    "violations_found": ["<violation: 'leveraging' in scorecard paragraph 2>"]
  },
  "validation_notes": "<overall 2-3 sentence assessment of the D1 output quality>"
}
```
"""


class D2ValidationAgent(BaseAgent):
    """Agent D2: Validation.

    Performs systematic QA over D1 output before prospect delivery.
    Returns a ValidationOutput with flags, confidence adjustments,
    and a pass/fail verdict.
    """

    agent_id = "D2_validation"
    model = settings.model_opus
    latency_budget_seconds = 120

    def run(self, inputs: dict) -> AgentResult:
        """Validate D1 output against source data.

        Args:
            inputs: dict with keys:
                - d1_output_json (dict, required — the D1 output to validate)
                - c2_output_json (dict, required — authoritative synthesis data)
                - research_outputs_json (dict, required — all B outputs: b1, b2, b3)
                - questionnaire_responses_json (list, required — raw responses)

        Returns:
            AgentResult whose .data matches the D2 ValidationOutput structure.
        """
        start = time.time()

        required = [
            "d1_output_json",
            "c2_output_json",
            "research_outputs_json",
            "questionnaire_responses_json",
        ]
        missing = [k for k in required if k not in inputs or inputs[k] is None]
        if missing:
            return AgentError(
                error=f"D2 missing required inputs: {missing}",
                agent_id=self.agent_id,
            )

        d1 = inputs["d1_output_json"]
        c2 = inputs["c2_output_json"]
        research = inputs["research_outputs_json"]
        responses = inputs["questionnaire_responses_json"]

        # Build user prompt
        user_prompt = self._build_user_prompt(
            d1=d1,
            c2=c2,
            research=research,
            responses=responses,
        )

        # Call Opus LLM
        try:
            llm_result = self._call_llm(
                system_prompt=_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                max_tokens=4000,
            )
        except Exception as exc:
            return AgentError(
                error=f"LLM call failed in D2: {exc}",
                agent_id=self.agent_id,
            )

        # Enrich and normalise the output
        output = self._normalise_output(llm_result)

        # Confidence: high if passed, low if blocking issues
        passed = output.get("overall_validation_passed", True)
        blocking_count = len(output.get("blocking_issues", []))
        if passed and blocking_count == 0:
            confidence = 0.92
        elif blocking_count > 0:
            confidence = 0.3
        else:
            confidence = 0.7

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
        d1: dict,
        c2: dict,
        research: dict,
        responses: list,
    ) -> str:
        """Build the D2 validation prompt with all source documents."""
        # Extract company name for the prompt header
        company_name = d1.get("company_canonical_name", c2.get("company_canonical_name", "the prospect"))

        # Build a score cross-reference table for the consistency check
        c2_overall = c2.get("overall_score", "N/A")
        c2_tier = c2.get("tier", "N/A")
        d1_overall = d1.get("scorecard_content", {}).get("overall_score", "N/A")
        d1_tier = d1.get("scorecard_content", {}).get("tier", "N/A")

        c2_dims = c2.get("dimension_scores", {})
        d1_dims = d1.get("scorecard_content", {}).get("dimension_details", [])
        d1_dim_lookup = {d.get("dimension_id"): d.get("score") for d in d1_dims}

        score_table_lines = ["Dimension | C2 score | D1 score | Match?"]
        for dim_key, dim_data in c2_dims.items():
            c2_raw = dim_data.get("raw_score", dim_data.get("questionnaire_score", "N/A"))
            d1_raw = d1_dim_lookup.get(dim_key, "MISSING")
            try:
                match = "YES" if abs(float(c2_raw) - float(d1_raw)) <= 2.0 else "NO -- CHECK"
            except (TypeError, ValueError):
                match = "CANNOT CHECK"
            score_table_lines.append(f"{dim_key} | {c2_raw} | {d1_raw} | {match}")

        score_table = "\n".join(score_table_lines)

        return f"""## Validation Request

Company: {company_name}

## Score Cross-Reference (for consistency check)

C2 overall score: {c2_overall}
D1 scorecard overall score: {d1_overall}
C2 tier: {c2_tier}
D1 scorecard tier: {d1_tier}

{score_table}

---

## D1 Output (the document being validated)

```json
{json.dumps(d1, indent=2, default=str)}
```

---

## C2 Synthesis Output (authoritative source of truth)

```json
{json.dumps(c2, indent=2, default=str)}
```

---

## Research Outputs (B1/B2/B3 — source data for fact grounding)

```json
{json.dumps(research, indent=2, default=str)}
```

---

## Raw Questionnaire Responses

```json
{json.dumps(responses, indent=2, default=str)}
```

---

## Your task

Perform all six validation checks as described in your system prompt:
1. Fact grounding — check every specific claim against source data
2. Internal consistency — check scores, tier, and findings alignment
3. Numerical sanity — check every number has a source
4. Hallucination patterns — flag company-specific facts not in source data
5. Confidence calibration — check D1 confidence matches signal quality
6. Voice and copyright check — check banned vocabulary and em-dash usage

Be thorough. False negatives (missed errors) are worse than false positives (over-flagging).
Set overall_validation_passed to false if ANY blocking issues exist.

Return ONLY valid JSON as specified in your system prompt.
"""

    def _normalise_output(self, llm_result: dict) -> dict:
        """Ensure the validation output has all required fields."""
        # Ensure blocking issues list exists
        if "blocking_issues" not in llm_result:
            llm_result["blocking_issues"] = []

        # Ensure validation_flags is a list
        if "validation_flags" not in llm_result:
            llm_result["validation_flags"] = []

        # Ensure confidence_adjustments is a list
        if "confidence_adjustments" not in llm_result:
            llm_result["confidence_adjustments"] = []

        # Recompute overall_validation_passed from blocking_issues
        has_blocking = any(
            f.get("severity") == "blocking"
            for f in llm_result.get("validation_flags", [])
        ) or len(llm_result.get("blocking_issues", [])) > 0

        llm_result["overall_validation_passed"] = not has_blocking

        # Ensure summary dicts exist
        if "fact_grounding_summary" not in llm_result:
            llm_result["fact_grounding_summary"] = {
                "claims_checked": 0,
                "claims_grounded": 0,
                "claims_ungrounded": 0,
                "ungrounded_claims": [],
            }

        if "internal_consistency_summary" not in llm_result:
            llm_result["internal_consistency_summary"] = {
                "score_consistency_passed": True,
                "tier_consistency_passed": True,
                "findings_consistency_passed": True,
                "quick_wins_consistency_passed": True,
                "inconsistencies_found": [],
            }

        if "voice_check_summary" not in llm_result:
            llm_result["voice_check_summary"] = {
                "voice_passed": True,
                "violations_found": [],
            }

        return llm_result
