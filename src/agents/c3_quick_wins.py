"""Agent C3 - Quick Wins Identification Agent.

Identifies the 2-3 highest-priority quick-win AI use cases for the prospect,
drawing from the DXC Quick Wins Library and calibrating selections against the
prospect's readiness profile from C2 and tech stack from B3.

Pre-filters the library by industry and size before calling the LLM, so the
model focuses on selection rationale and prospect-specific framing rather than
catalogue browsing.

Model: claude-opus-4-7 (selection requires nuanced cross-signal reasoning)
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict, List

from src.config import settings
from src.agents.base import AgentResult, AgentError, BaseAgent
from src.data.quick_wins import get_quick_wins_for_prospect


_SYSTEM_PROMPT = """You are the Quick Wins Identification Agent (C3) for the DXC AI Readiness Diagnostic.

Your job is to select the 2-3 best quick-win AI use cases for a specific prospect and frame them with enough specificity that the DXC account team can walk in and have a credible conversation about each one.

## What you receive

- The prospect's readiness profile (C2 output): overall score, dimension scores, tier, and findings
- The prospect's tech stack (B3 output): platforms detected, cloud maturity, existing AI tools
- The prospect's industry process mapping (C1 output): applicable processes and priority ranking
- A pre-filtered set of Quick Win candidate patterns: already filtered for this prospect's industry and size band

## Selection rules

1. **Select exactly 2-3 quick wins.** No more, no fewer.

2. **Prerequisite check required for each candidate**: For every candidate you consider, explicitly assess whether each of its prerequisites is met, likely met, uncertain, or likely not met. If a candidate has one or more prerequisites that are likely not met, deprioritise it unless it is otherwise compelling.

3. **Do not select a quick win with a disqualifying condition that applies to this prospect.**

4. **Prioritise wins that address the prospect's weakest scoreable dimension** (lowest dimension score from C2), unless that dimension has prerequisites not met.

5. **Diversity of dimension coverage**: Try to select quick wins that address different dimensions when possible.

6. **Always include at least one Tier 1 universal quick win** (applicable_industries = "All") unless no universal patterns were provided.

7. **Rank order your selections**: rank 1 = highest value/feasibility combination for this specific prospect.

## Framing rules

Each selected quick win must be framed specifically for this prospect. Generic descriptions are not acceptable.

- Reference the prospect's actual tech stack where relevant: "Given your detected SAP S/4HANA deployment..."
- Reference their dimension score: "Given your Governance score of 42..."
- Reference their industry: "For a mid-market insurer like..."
- Provide a concrete estimated ROI narrative where peer examples support it — do not invent numbers not in the pattern data.

## Output format

Return ONLY valid JSON. No explanatory text outside the JSON.

```json
{
  "selected_quick_wins": [
    {
      "pattern_id": "<pattern_id from candidate list>",
      "name": "<pattern name>",
      "one_line_description": "<prospect-specific version of the one-liner>",
      "rank": <1|2|3>,
      "selection_rationale": "<2-3 sentences: why this pattern, why now, why this prospect>",
      "prerequisite_checks": [
        {
          "prerequisite": "<prerequisite text>",
          "met": <true|false|null for uncertain>,
          "evidence": "<specific evidence from B3, C2, or prospect profile>"
        }
      ],
      "all_prerequisites_met": <true|false>,
      "estimated_timeline_weeks": <int>,
      "estimated_roi_narrative": "<1-2 sentences based on peer examples, or null if insufficient data>",
      "dxc_practice_owner": "<relevant DXC practice>"
    }
  ],
  "total_candidates_evaluated": <int — number of pre-filtered candidates provided>,
  "selection_rationale_summary": "<2-3 sentences explaining the overall selection logic>",
  "patterns_excluded_rationale": "<brief explanation of why top candidates were excluded if relevant>"
}
```

## Voice rules

- Be specific, not generic. Reference the prospect by name.
- No em-dashes. Use commas or semicolons instead.
- Avoid: leverage (as verb), unlock, harness, transform, holistic, robust, paradigm.
- Use "use" not "utilize". Use "help" not "facilitate".
- Write for a senior audience. Direct and confident tone.
"""


class C3QuickWinsAgent(BaseAgent):
    """Agent C3: Quick Wins Identification.

    Filters the Quick Wins Library for the prospect's industry and size band,
    then uses the Opus LLM to select and frame 2-3 wins with prospect-specific
    rationale and prerequisite checks.
    """

    agent_id = "C3_quick_wins"
    model = settings.model_opus
    latency_budget_seconds = 90

    def run(self, inputs: dict) -> AgentResult:
        """Identify the top 2-3 quick wins for the prospect.

        Args:
            inputs: dict with keys:
                - company_canonical_name (str, required)
                - company_industry_label (str, required)
                - company_size_band_estimate (str, required)
                - primary_persona (str, required — P1|P2|P3)
                - c2_output_json (dict, required — synthesis output)
                - b3_output_json (dict, required — tech stack output)
                - c1_output_json (dict, required — industry library mapping)

        Returns:
            AgentResult whose .data matches the C3 QuickWinsOutput structure.
        """
        start = time.time()

        required = [
            "company_canonical_name",
            "company_industry_label",
            "company_size_band_estimate",
            "primary_persona",
            "c2_output_json",
            "b3_output_json",
            "c1_output_json",
        ]
        missing = [k for k in required if k not in inputs or inputs[k] is None]
        if missing:
            return AgentError(
                error=f"C3 missing required inputs: {missing}",
                agent_id=self.agent_id,
            )

        company_name = inputs["company_canonical_name"]
        industry = inputs["company_industry_label"]
        size_band = inputs["company_size_band_estimate"]
        persona = inputs["primary_persona"]
        c2 = inputs["c2_output_json"]
        b3 = inputs["b3_output_json"]
        c1 = inputs["c1_output_json"]

        # --- Step 1: Filter quick wins library ---
        # Normalise size band from intake output format to library format
        normalised_size = self._normalise_size_band(size_band)
        try:
            candidates = get_quick_wins_for_prospect(
                industry_label=industry,
                size_band=normalised_size,
            )
        except Exception as exc:
            return AgentError(
                error=f"Quick wins library filtering failed: {exc}",
                agent_id=self.agent_id,
            )

        if not candidates:
            # Fallback: no candidates after filtering — return minimal output
            output = {
                "selected_quick_wins": [],
                "total_candidates_evaluated": 0,
                "selection_rationale_summary": (
                    f"No pre-filtered quick win candidates matched {company_name}'s "
                    f"industry ({industry}) and size band ({size_band}). "
                    "Manual assessment recommended."
                ),
                "patterns_excluded_rationale": "No candidates passed industry and size band filter.",
            }
            return AgentResult(
                data=output,
                confidence=0.4,
                latency_ms=self._elapsed_ms(start),
                agent_id=self.agent_id,
            )

        # --- Step 2: Build LLM prompt ---
        user_prompt = self._build_user_prompt(
            company_name=company_name,
            industry=industry,
            size_band=normalised_size,
            persona=persona,
            c2=c2,
            b3=b3,
            c1=c1,
            candidates=candidates,
        )

        # --- Step 3: LLM selection ---
        try:
            llm_result = self._call_llm(
                system_prompt=_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                max_tokens=4000,
            )
        except Exception as exc:
            return AgentError(
                error=f"LLM call failed in C3: {exc}",
                agent_id=self.agent_id,
            )

        # --- Step 4: Enrich output ---
        output = {
            "selected_quick_wins": llm_result.get("selected_quick_wins", []),
            "total_candidates_evaluated": len(candidates),
            "selection_rationale_summary": llm_result.get("selection_rationale_summary", ""),
            "patterns_excluded_rationale": llm_result.get("patterns_excluded_rationale", ""),
            "company_canonical_name": company_name,
            "industry": industry,
        }

        # Confidence based on number of candidates and prerequisite coverage
        wins = output["selected_quick_wins"]
        all_prereqs_met = all(w.get("all_prerequisites_met", True) for w in wins)
        confidence = 0.85 if (len(wins) >= 2 and all_prereqs_met) else 0.65

        return AgentResult(
            data=output,
            confidence=confidence,
            latency_ms=self._elapsed_ms(start),
            agent_id=self.agent_id,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _normalise_size_band(self, size_band: str) -> str:
        """Map A1 output size band labels to library size band labels."""
        mapping = {
            "mid-market": "Mid-Market",
            "mid_market": "Mid-Market",
            "midmarket": "Mid-Market",
            "large": "Large",
            "global": "Enterprise",
            "enterprise": "Enterprise",
            "smb": "SMB",
            "small": "SMB",
            "unknown": "Mid-Market",  # default fallback
        }
        return mapping.get(size_band.lower().strip(), "Large")

    def _build_user_prompt(
        self,
        company_name: str,
        industry: str,
        size_band: str,
        persona: str,
        c2: dict,
        b3: dict,
        c1: dict,
        candidates: list,
    ) -> str:
        """Construct the user prompt for C3."""
        persona_descriptions = {
            "P1": "Strategic / Executive — frame quick wins in terms of competitive advantage and strategic risk reduction",
            "P2": "Technical / Operational — frame in terms of workflow improvement, system integration, and operational friction",
            "P3": "Financial / CFO — frame in terms of cost savings, ROI, and payback period",
        }
        persona_desc = persona_descriptions.get(persona, persona)

        # Extract key signals from C2 to guide selection
        overall_score = c2.get("overall_score", "N/A")
        overall_tier = c2.get("tier", "N/A")
        dim_scores = c2.get("dimension_scores", {})

        # Find weakest dimension
        weakest_dim = None
        weakest_score = 101.0
        for dim_key, dim_data in dim_scores.items():
            raw = dim_data.get("raw_score", dim_data.get("questionnaire_score", 100.0))
            if raw < weakest_score:
                weakest_score = raw
                weakest_dim = dim_key

        # Tech stack summary
        platforms = b3.get("platforms_detected", [])
        platform_names = [p.get("platform_name", "") for p in platforms[:5]]
        existing_ai = b3.get("existing_ai_tools", [])
        cloud_maturity = b3.get("cloud_maturity", "unknown")

        return f"""## Prospect Profile

Company: {company_name}
Industry: {industry}
Size band: {size_band}
Primary persona: {persona} — {persona_desc}

---

## C2 Synthesis Summary

Overall score: {overall_score}/100
Overall tier: {overall_tier}
Weakest dimension: {weakest_dim} (score: {weakest_score:.1f})

Dimension scores summary:
```json
{json.dumps({k: v.get("raw_score", v.get("questionnaire_score", "N/A")) for k, v in dim_scores.items()}, indent=2)}
```

Key findings from C2:
```json
{json.dumps(c2.get("findings", []), indent=2, default=str)}
```

---

## Technology Stack (B3)

Cloud maturity: {cloud_maturity}
Platforms detected: {", ".join(platform_names) if platform_names else "none detected"}
Existing AI tools: {", ".join(existing_ai) if existing_ai else "none detected"}

Full B3 output:
```json
{json.dumps(b3, indent=2, default=str)}
```

---

## Industry Process Mapping (C1)

Top applicable processes for {company_name}:
```json
{json.dumps(c1.get("applicable_processes", [])[:5], indent=2, default=str)}
```

---

## Pre-Filtered Quick Win Candidates

The following {len(candidates)} patterns have been pre-filtered for {company_name}'s industry ({industry}) and size band ({size_band}). Select 2-3 from this list only.

```json
{json.dumps(candidates, indent=2)}
```

---

## Your task

1. Evaluate all {len(candidates)} candidates above.
2. Check prerequisites for each against what you know about {company_name} from B3 and C2.
3. Reject any candidate with a disqualifying condition that applies to {company_name}.
4. Select 2-3 with the best combination of value potential and prerequisite feasibility.
5. Frame each selection specifically for {company_name} — reference their tech stack, dimension scores, and industry context.
6. Rank them (1 = best for this prospect).

Return ONLY valid JSON as specified in your system prompt.
"""
