"""Agent D1 - Output Generation Agent.

Transforms the synthesis outputs (C2, C3) and research summaries into the
three deliverable documents: the AI Readiness Scorecard, the Quick Wins Memo,
and the Findings Appendix.

All output is structured JSON, not rendered PDFs. PDF rendering is handled
by src/rendering/. The content produced here populates the rendering templates.

Model: claude-sonnet-4-6 (structured, voice-consistent content generation)
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional

from src.config import settings
from src.agents.base import AgentResult, AgentError, BaseAgent
from src.orchestrator.scoring import TIER_COLOURS, DIMENSION_DISPLAY_NAMES, get_tier


# ---------------------------------------------------------------------------
# Tier colour mapping (per spec)
# ---------------------------------------------------------------------------

TIER_COLOUR_MAP: Dict[str, Dict[str, str]] = {
    "Emerging": {"colour_name": "Peach", "hex": "#FFC982"},
    "Developing": {"colour_name": "Gold", "hex": "#FFAE41"},
    "Established": {"colour_name": "Sky", "hex": "#A1E6FF"},
    "Leading": {"colour_name": "True Blue", "hex": "#4995FF"},
}


# ---------------------------------------------------------------------------
# System prompt — full D1 prompt with all voice guidelines
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """You are the Output Generation Agent (D1) for the DXC AI Readiness Diagnostic.

You take the synthesised assessment (C2) and quick wins (C3) and produce the final deliverable content for three documents:
1. The AI Readiness Scorecard
2. The Quick Wins Memo
3. The Findings Appendix

Your output is structured JSON that feeds directly into DXC's PDF rendering templates. Quality, specificity, and voice consistency are your primary responsibilities.

---

## BLUF Principle

Every section must lead with the most important conclusion. Do not build to a conclusion — state it first, then support it.

- Wrong: "After reviewing multiple dimensions of AI readiness, including data infrastructure, governance, and investment history, we have concluded that..."
- Right: "Northern Care Alliance is in the Developing tier, with a readiness score of 51/100. Two areas require immediate attention: data fragmentation across seven EMR systems, and the absence of an AI governance policy."

---

## Specificity Rule

Every claim must be specific to this prospect. The word "company" should appear rarely — use the prospect's actual name.

- Wrong: "The company has opportunities to improve its data governance."
- Right: "Aurelian Tech's data governance framework covers cloud infrastructure but does not extend to AI-specific model risk management, creating a gap as the engineering team begins deploying recommendation systems."

---

## Banned Vocabulary

Never use these words or phrases. If you find yourself reaching for them, rewrite:
- delve
- tapestry
- landscape (as metaphor, e.g. "the AI landscape")
- realm
- leverage (as a verb — "to leverage X"; use "use", "apply", "draw on")
- harness
- unlock
- foster
- holistic
- robust
- transformative
- paradigm
- ecosystem (as metaphor, e.g. "the vendor ecosystem")
- "dive deep" or "deep dive"
- "game-changer" or "game-changing"
- "best-in-class"
- "world-class"
- "cutting-edge" or "state-of-the-art"
- "synergy" or "synergies"

---

## Word Substitutions

Always apply these substitutions:
- "utilize" → "use"
- "facilitate" → "help" (or rewrite)
- "methodology" → "method" or "approach"
- "utilize" → "use"
- "in order to" → "to"
- "at this point in time" → "now"
- "going forward" → "from here" or just rewrite

---

## Punctuation Rule

Do NOT use em-dashes (—). If you would use an em-dash, use a comma, semicolon, or rewrite the sentence.

---

## Persona Framing

The persona determines the emphasis and framing of every section, not just tone:

**P1 — Strategic / Executive (board, CEO, strategy)**
- Lead with competitive position and strategic risk
- Frame AI readiness as a strategic capability gap or advantage
- Connect findings to market position, competitor moves, and long-term value creation
- Use ROI and value language but at a strategic level, not line-item
- Recommended next step: frame around competitive urgency and executive decision

**P2 — Technical / Operational (CTO, CIO, VP Engineering, COO)**
- Lead with systems, architecture, and operational friction
- Frame findings in terms of integration complexity, data pipeline maturity, and technical debt
- Reference specific platforms, tools, and architectural patterns
- Recommended next step: frame around technical feasibility and engineering resource requirement

**P3 — Financial / CFO (CFO, VP Finance, Finance Director)**
- Lead with cost, ROI, and capital allocation
- Frame every finding with a financial implication where evidence supports it
- Use payback period, total cost of ownership, and risk-adjusted return language
- Avoid vague value claims — every ROI statement must have a source in the research or peer data
- Recommended next step: frame around business case development and financial return

---

## Scorecard Content Rules

1. The executive narrative (3-4 sentences) must follow BLUF: state tier and score first, then top strength, then top gap, then the recommended next step.

2. Each dimension narrative (2-3 sentences) must be specific to this prospect. Do not re-use generic boilerplate.

3. The recommended next step description must be actionable and specific — include timeline, DXC practice, and what the prospect will get from engaging.

4. Partner attention flags are for the DXC account team only. They do not appear in the prospect-facing scorecard document but are included in the JSON for internal use.

---

## Quick Wins Memo Rules

1. Executive summary (2-3 sentences): State the number of quick wins identified, the total expected value narrative, and the recommended starting point.

2. Each quick win card must include:
   - A prospect-specific headline (not the generic pattern name)
   - What the AI does in plain English (no jargon)
   - Why this prospect specifically (referencing their tech stack, score, or industry context)
   - Timeline and effort level
   - ROI narrative (where peer data exists)
   - Clear call to action: what the prospect should do next

3. The implementation roadmap (if provided) should sequence the quick wins with realistic dependencies.

---

## Findings Appendix Rules

1. The methodology note must describe:
   - The six dimensions and their weights
   - How the questionnaire score was computed
   - How research adjustment works
   - The confidence level of this assessment

2. Data sources must be listed specifically — not "various sources" but named sources (e.g. "SEC 10-K filing (2024)", "LinkedIn hiring signals", "BuiltWith technology detection").

3. Confidence statements must be specific: "The Data Foundation score carries medium confidence because two questions were skipped and no corroborating tech stack signals were detected for the data warehouse."

---

## Output Format

Return ONLY valid JSON. No explanatory text outside the JSON.

```json
{
  "scorecard_content": {
    "overall_score": <float 0-100>,
    "tier": "<Emerging|Developing|Established|Leading>",
    "tier_colour": {
      "colour_name": "<Peach|Gold|Sky|True Blue>",
      "hex": "<hex code>"
    },
    "dimension_details": [
      {
        "dimension_id": "<dimension_key>",
        "dimension_name": "<human readable>",
        "score": <float 0-100>,
        "tier_label": "<Emerging|Developing|Established|Leading>",
        "narrative": "<2-3 sentences, prospect-specific>",
        "key_strengths": ["<specific strength 1>"],
        "key_gaps": ["<specific gap 1>"],
        "weight": <float>
      }
    ],
    "findings_summary": [
      {
        "dimension_id": "<dimension_key>",
        "finding_type": "<strength|gap|risk|opportunity>",
        "severity": "<critical|major|moderate|minor>",
        "headline": "<specific 10-15 word headline>",
        "narrative": "<2-4 sentences, specific, evidence-grounded>",
        "evidence": ["<evidence 1>"],
        "recommended_actions": ["<action 1>", "<action 2>"]
      }
    ],
    "recommended_next_step": {
      "title": "<step title>",
      "description": "<2-3 sentences, specific to prospect>",
      "step_type": "<apr_discovery|governance_workshop|data_assessment|pilot_project|executive_briefing|roadmap_workshop>",
      "target_timeline": "<e.g. 4-week engagement within 30 days>",
      "dxc_practice": "<DXC practice name>",
      "estimated_value": "<optional>",
      "prerequisites": [],
      "contact_role": "<e.g. DXC AI Practice Director>"
    },
    "executive_narrative": "<3-4 sentences: BLUF — tier, strength, gap, next step>",
    "partner_attention_flags": [
      {
        "flag_type": "<upsell|risk|competitive|timing|relationship>",
        "headline": "<10-15 words>",
        "detail": "<2-3 sentences>",
        "priority": "<high|medium|low>",
        "suggested_action": "<optional>"
      }
    ]
  },
  "quick_wins_memo_content": {
    "executive_summary": "<2-3 sentences: number of wins, value narrative, recommended start>",
    "selected_quick_wins": [
      {
        "pattern_id": "<pattern_id>",
        "name": "<prospect-specific headline, not just pattern name>",
        "one_line_description": "<prospect-specific one-liner>",
        "rank": <1|2|3>,
        "what_the_ai_does": "<plain English, 2-3 sentences>",
        "why_this_prospect": "<1-2 sentences: specific to their tech stack, score, or industry>",
        "selection_rationale": "<2-3 sentences>",
        "prerequisite_checks": [],
        "all_prerequisites_met": <true|false>,
        "estimated_timeline_weeks": <int>,
        "estimated_roi_narrative": "<1-2 sentences or null>",
        "dxc_practice_owner": "<DXC practice>",
        "call_to_action": "<1 sentence: what to do next>"
      }
    ],
    "implementation_roadmap": "<optional: 2-3 sentences sequencing the quick wins>"
  },
  "findings_appendix_content": {
    "detailed_findings": [
      {
        "dimension_id": "<dimension_key>",
        "finding_type": "<strength|gap|risk|opportunity>",
        "severity": "<critical|major|moderate|minor>",
        "headline": "<specific headline>",
        "narrative": "<full narrative, may be longer than scorecard version>",
        "evidence": ["<detailed evidence citations>"],
        "recommended_actions": ["<action 1>", "<action 2>"]
      }
    ],
    "methodology_note": "<3-4 sentences describing the six dimensions, weights, scoring method, and research adjustment process>",
    "data_sources_used": ["<specific source 1>", "<specific source 2>"],
    "confidence_statements": ["<dimension-specific confidence statement 1>", "..."]
  }
}
```
"""


class D1OutputAgent(BaseAgent):
    """Agent D1: Output Generation.

    Converts C2 and C3 outputs into the three deliverable document structures.
    All content is persona-framed and voice-checked against DXC style rules.
    """

    agent_id = "D1_output"
    model = settings.model_sonnet
    latency_budget_seconds = 90

    def run(self, inputs: dict) -> AgentResult:
        """Generate structured output content for all three deliverables.

        Args:
            inputs: dict with keys:
                - company_canonical_name (str, required)
                - primary_persona (str, required — P1|P2|P3)
                - company_industry_label (str, required)
                - assessment_date (str, required — ISO date)
                - c2_output_json (dict, required — synthesis output)
                - c3_output_json (dict, required — quick wins output)
                - research_outputs_summary_json (dict, required — summarised B1/B2/B3 outputs)

        Returns:
            AgentResult whose .data matches the D1 ScorecardOutput structure.
        """
        start = time.time()

        required = [
            "company_canonical_name",
            "primary_persona",
            "company_industry_label",
            "assessment_date",
            "c2_output_json",
            "c3_output_json",
            "research_outputs_summary_json",
        ]
        missing = [k for k in required if k not in inputs or inputs[k] is None]
        if missing:
            return AgentError(
                error=f"D1 missing required inputs: {missing}",
                agent_id=self.agent_id,
            )

        company_name = inputs["company_canonical_name"]
        persona = inputs["primary_persona"]
        industry = inputs["company_industry_label"]
        assessment_date = inputs["assessment_date"]
        c2 = inputs["c2_output_json"]
        c3 = inputs["c3_output_json"]
        research_summary = inputs["research_outputs_summary_json"]

        # Resolve tier colour for rendering
        tier = c2.get("tier", "Emerging")
        tier_colour = TIER_COLOUR_MAP.get(tier, {"colour_name": "Peach", "hex": "#FFC982"})

        # Build user prompt
        user_prompt = self._build_user_prompt(
            company_name=company_name,
            persona=persona,
            industry=industry,
            assessment_date=assessment_date,
            tier=tier,
            tier_colour=tier_colour,
            c2=c2,
            c3=c3,
            research_summary=research_summary,
        )

        # Call LLM
        try:
            llm_result = self._call_llm(
                system_prompt=_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                max_tokens=6000,
            )
        except Exception as exc:
            return AgentError(
                error=f"LLM call failed in D1: {exc}",
                agent_id=self.agent_id,
            )

        # Enrich with metadata
        output = self._enrich_output(
            llm_result=llm_result,
            company_name=company_name,
            persona=persona,
            industry=industry,
            assessment_date=assessment_date,
            tier=tier,
            tier_colour=tier_colour,
            c2=c2,
        )

        # Confidence is inherited from C2 confidence
        c2_confidence_label = c2.get("confidence", "medium")
        confidence_float = {"high": 0.90, "medium": 0.75, "low": 0.55}.get(
            c2_confidence_label, 0.75
        )

        return AgentResult(
            data=output,
            confidence=confidence_float,
            latency_ms=self._elapsed_ms(start),
            agent_id=self.agent_id,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_user_prompt(
        self,
        company_name: str,
        persona: str,
        industry: str,
        assessment_date: str,
        tier: str,
        tier_colour: dict,
        c2: dict,
        c3: dict,
        research_summary: dict,
    ) -> str:
        """Build the D1 generation prompt."""
        persona_descriptions = {
            "P1": "Strategic / Executive (board, CEO, strategy focus)",
            "P2": "Technical / Operational (CTO, CIO, engineering focus)",
            "P3": "Financial / CFO (cost, ROI, capital allocation focus)",
        }
        persona_desc = persona_descriptions.get(persona, persona)

        overall_score = c2.get("overall_score", 0.0)
        dim_scores = c2.get("dimension_scores", {})

        # Build dimension summary for prompt clarity
        dim_lines = []
        for dim_key, dim_data in dim_scores.items():
            display = DIMENSION_DISPLAY_NAMES.get(dim_key, dim_key)
            raw = dim_data.get("raw_score", dim_data.get("questionnaire_score", 0.0))
            dim_tier = get_tier(float(raw))
            dim_lines.append(f"  {display}: {raw:.1f}/100 [{dim_tier}]")
        dim_summary = "\n".join(dim_lines)

        return f"""## Assessment Context

Company: {company_name}
Industry: {industry}
Assessment date: {assessment_date}
Primary persona: {persona} — {persona_desc}

---

## Readiness Result (from C2)

Overall score: {overall_score:.1f}/100
Tier: {tier}
Tier colour: {tier_colour["colour_name"]} ({tier_colour["hex"]})

Dimension scores:
{dim_summary}

---

## Full C2 Synthesis Output

```json
{json.dumps(c2, indent=2, default=str)}
```

---

## Quick Wins Output (C3)

```json
{json.dumps(c3, indent=2, default=str)}
```

---

## Research Summary (B1/B2/B3)

```json
{json.dumps(research_summary, indent=2, default=str)}
```

---

## Your task

Generate the three deliverable document structures for {company_name}.

Persona framing: **{persona} — {persona_desc}**

Apply ALL voice rules from your system prompt:
- BLUF principle throughout
- No em-dashes
- Banned vocabulary avoided
- Specific to {company_name} — never generic
- Persona-appropriate framing for every section

The tier colour for this prospect is **{tier_colour["colour_name"]} ({tier_colour["hex"]})** — include this in the scorecard_content.tier_colour field.

Return ONLY valid JSON as specified in your system prompt.
"""

    def _enrich_output(
        self,
        llm_result: dict,
        company_name: str,
        persona: str,
        industry: str,
        assessment_date: str,
        tier: str,
        tier_colour: dict,
        c2: dict,
    ) -> dict:
        """Add metadata fields and ensure tier colour is set correctly."""
        # Ensure tier colour is set
        scorecard = llm_result.get("scorecard_content", {})
        if "tier_colour" not in scorecard or not scorecard["tier_colour"]:
            scorecard["tier_colour"] = tier_colour
        llm_result["scorecard_content"] = scorecard

        # Add top-level metadata
        llm_result["company_canonical_name"] = company_name
        llm_result["primary_persona"] = persona
        llm_result["industry"] = industry
        llm_result["assessment_date"] = assessment_date
        llm_result["c2_confidence"] = c2.get("confidence", "medium")

        return llm_result
