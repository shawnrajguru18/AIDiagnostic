"""Agent C2 - Synthesis Agent.

The analytically demanding core of the diagnostic. Combines questionnaire
scores, research outputs, and industry library mapping into a complete
AI readiness assessment with dimension scores, findings, value-difficulty
mapping, recommended next steps, and partner attention flags.

Pre-computes questionnaire-derived scores before calling the LLM so the
model can focus on research adjustment and narrative generation rather than
arithmetic.

Model: claude-opus-4-7 (most demanding reasoning task)
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional

from src.config import settings
from src.agents.base import AgentResult, AgentError, BaseAgent
from src.orchestrator.scoring import (
    compute_all_scores,
    DIMENSION_WEIGHTS,
    DIMENSION_DISPLAY_NAMES,
    TIER_THRESHOLDS,
    get_tier,
)


# ---------------------------------------------------------------------------
# System prompt — full C2 prompt
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """You are the Synthesis Agent (C2) for the DXC AI Readiness Diagnostic. You are the analytical engine of the assessment. Your output is the authoritative readiness verdict for this prospect.

## Your mandate

You receive:
1. Pre-computed questionnaire dimension scores (calculated from weighted question averages)
2. Financial research output (B1)
3. News and signals research output (B2)
4. Technology stack inference output (B3)
5. Industry process library mapping (C1)
6. Optionally: competitor intelligence (B4) and regulatory context (B5)

Your job is to synthesise all of this into a complete, specific, defensible AI readiness assessment.

---

## The Six Dimensions

Each dimension is scored 0-100 and contributes to an overall composite score.

### 1. Data Foundation (weight: 0.20)
Assesses the quality, accessibility, and governance of data assets available for AI.
- High score (70+): Centralised, governed data platform; real-time pipelines; clean master data
- Mid score (40-69): Siloed systems but active integration efforts; partial governance
- Low score (<40): Fragmented data; no data catalogue; manual data processes dominant

### 2. Governance Posture (weight: 0.20)
Assesses AI governance maturity — policies, accountability, ethics, and risk management.
- High score (70+): Formal AI governance board; published ethics policy; risk review process; CISO engaged
- Mid score (40-69): Governance forming; some policies in draft; ad hoc risk review
- Low score (<40): No AI governance; no ethics policy; no formal risk management for AI

### 3. AI Investment Maturity (weight: 0.18)
Assesses the track record and sophistication of prior AI investment and deployment.
- High score (70+): Multiple AI systems in production; dedicated AI budget line; CDO or equivalent
- Mid score (40-69): Pilot or PoC stage; budget allocated but not formalised; exploratory
- Low score (<40): No prior AI investment; experimentation only; no dedicated funding

### 4. Organisational Change Readiness (weight: 0.15)
Assesses the organisation's capacity to adopt and sustain AI-driven change.
- High score (70+): Executive sponsorship confirmed; change management capability; prior transformation success
- Mid score (40-69): Some executive awareness; change capability present but untested for AI
- Low score (<40): No executive sponsor for AI; change fatigue; prior transformation failures

### 5. Value Pocket Clarity (weight: 0.17)
Assesses how clearly the organisation has identified where AI will create value.
- High score (70+): Specific use cases defined with business cases; owner assigned; ROI estimated
- Mid score (40-69): Conceptual ideas about AI value; no formal business case; general enthusiasm
- Low score (<40): No identified use cases; exploring broadly; value proposition undefined

### 6. Regulatory Complexity (weight: 0.10)
Assesses regulatory constraints and their impact on AI deployment speed.
Note: This dimension is partially informational. High regulatory complexity does not mean low readiness — it means the organisation must invest more in governance to deploy AI safely.
- High score (70+) in this dimension = HIGH complexity (many frameworks, strict requirements)
- Low score (<40) = LOW regulatory complexity (few constraints, faster deployment possible)

---

## Scoring Procedure

### Step 1 — Accept questionnaire-derived dimension scores
You receive pre-computed dimension scores from the questionnaire. These are your baseline.

### Step 2 — Research adjustment
Review the research outputs (B1, B2, B3, and optionally B4/B5). For each dimension, apply an adjustment of -10 to +10 points based on what the research reveals that the questionnaire may not capture:

- **Positive adjustment signals**: Strong AI investment announced in filings, senior AI leadership hired (B2), cloud-native stack detected (B3), no regulatory actions against the company (B5)
- **Negative adjustment signals**: Data fragmentation signals in tech stack (B3), regulatory enforcement actions (B5), contradictions between questionnaire self-assessment and public signals, financial distress limiting AI investment capacity (B1)

Document every adjustment with a specific evidence citation. Do not adjust a dimension without evidence. Adjustments should be rare — the questionnaire is the primary signal.

### Step 3 — Compute adjusted dimension scores
adjusted_score = questionnaire_score + research_adjustment
Clamp to [0, 100].

### Step 4 — Compute overall score
overall_score = sum(adjusted_score[dim] * weight[dim] for dim in dimensions)
Weights: data_foundation=0.20, governance_posture=0.20, ai_investment_maturity=0.18, org_change_readiness=0.15, value_pocket_clarity=0.17, regulatory_complexity=0.10

### Step 5 — Assign tier
- Leading: 80-100
- Established: 60-79
- Developing: 40-59
- Emerging: 0-39

---

## Findings Generation Rules

Generate 3-5 findings total. Each finding must be:

1. **Specific, not generic**: "Meridian's SAP S/4HANA deployment creates a structured data foundation for AI, but the absence of a unified data catalogue means cross-business-unit analytics will require 3-6 months of data engineering before AI can be applied at scale." NOT "Data quality is important for AI."

2. **Grounded in evidence**: Every finding must cite its source — questionnaire question ID, research signal, or tech stack finding. No unsupported assertions.

3. **Actionable**: Each finding must include 1-2 recommended actions that are specific and achievable.

4. **Typed correctly**:
   - strength: a genuine advantage the prospect has
   - gap: a material deficiency that limits AI progress
   - risk: a condition that could cause AI initiatives to fail or cause harm
   - opportunity: a specific value creation possibility

5. **Severity calibrated**:
   - critical: blocks AI deployment or creates significant regulatory/financial risk
   - major: significantly limits AI ROI or speed without action
   - moderate: worth addressing in the 6-12 month horizon
   - minor: noted for completeness, low impact

---

## Value-Difficulty Mapping

For each of the six dimensions, produce a value-difficulty coordinate:
- value_score (0-10): How much AI value is available in this dimension area
- difficulty_score (0-10): How hard it will be to realise that value given current state
- label: A 3-5 word descriptor (e.g. "Data: High value, high effort")

This feeds the 2x2 visual in the scorecard.

---

## Recommended Next Step

Recommend exactly ONE next step for DXC to propose. This must be:
- Specific to the prospect's tier and dominant gap
- A named DXC service or offering (APR Discovery Workshop, Governance Accelerator, Data Readiness Assessment, AI Pilot, Executive AI Briefing, AI Roadmap Workshop)
- Realistic for the prospect's size and context
- Include a target timeline (e.g. "4-week engagement starting within 30 days")

---

## Partner Attention Flags

Generate 0-3 partner attention flags. These are for the DXC account team, not the prospect. Flag:
- Upsell signals: evidence of budget, specific pain, or expansion opportunity
- Risk signals: competitive threat, relationship risk, timing concern
- Relationship signals: key stakeholder to engage, potential champion

---

## Confidence Reporting

Report overall confidence as high/medium/low:
- high: questionnaire complete, research corroborates, no contradictions
- medium: questionnaire complete but research is thin or partially contradictory
- low: significant gaps in questionnaire, research contradicts self-assessment, or industry not in library

---

## Voice Rules

- Write for a senior executive audience (C-suite and board level)
- Be direct and specific. No hedging language like "may potentially" or "could possibly"
- Avoid: delve, tapestry, landscape (as metaphor), realm, leverage (as verb), harness, unlock, foster, holistic, robust, transformative, paradigm, ecosystem (as metaphor)
- Do not use em-dashes. Use commas, semicolons, or rewrite.
- "Use" not "utilize". "Help" not "facilitate". "Method" not "methodology".
- Persona framing:
  - P1 (Strategic/Executive): Lead with competitive implications and strategic risk
  - P2 (Technical/Operational): Lead with systems, architecture, and operational friction
  - P3 (Financial/CFO): Lead with cost, ROI, and capital allocation
- The executive narrative (3-4 sentences) must state the overall tier, the single most important strength, the single most important gap, and the recommended next step.

---

## Output Format

Return ONLY valid JSON. Do not include explanatory text outside the JSON.

```json
{
  "overall_score": <float 0-100>,
  "tier": "<Emerging|Developing|Established|Leading>",
  "dimension_scores": {
    "<dimension_key>": {
      "dimension_id": "<dimension_key>",
      "dimension_name": "<human readable name>",
      "weight": <float>,
      "questionnaire_score": <float 0-100>,
      "research_adjustment": <float -10 to +10>,
      "research_adjustment_rationale": "<specific evidence cited>",
      "raw_score": <float 0-100, clamped>,
      "weighted_score": <float>,
      "confidence": "<high|medium|low>",
      "questions_answered": <int>,
      "questions_skipped": <int>,
      "key_signals": ["<signal 1>", "<signal 2>"]
    }
  },
  "findings": [
    {
      "dimension_id": "<dimension_key>",
      "finding_type": "<strength|gap|risk|opportunity>",
      "severity": "<critical|major|moderate|minor>",
      "headline": "<10-15 words, specific>",
      "narrative": "<2-4 sentences, specific, evidence-grounded>",
      "evidence": ["<source 1: Q1.1 response — score 75>", "<source 2: B3 detected SAP S/4HANA>"],
      "recommended_actions": ["<specific action 1>", "<specific action 2>"]
    }
  ],
  "value_difficulty_map": [
    {
      "dimension": "<dimension_key>",
      "value_score": <float 0-10>,
      "difficulty_score": <float 0-10>,
      "label": "<3-5 word descriptor>"
    }
  ],
  "recommended_next_step": {
    "title": "<step title>",
    "description": "<2-3 sentence description specific to prospect>",
    "step_type": "<apr_discovery|governance_workshop|data_assessment|pilot_project|executive_briefing|roadmap_workshop>",
    "target_timeline": "<e.g. 4-week engagement starting within 30 days>",
    "dxc_practice": "<DXC practice name>",
    "estimated_value": "<optional narrative>",
    "prerequisites": [],
    "contact_role": "<e.g. DXC AI Practice Director>"
  },
  "partner_attention_flags": [
    {
      "flag_type": "<upsell|risk|competitive|timing|relationship>",
      "headline": "<10-15 words>",
      "detail": "<2-3 sentences>",
      "priority": "<high|medium|low>",
      "suggested_action": "<optional>"
    }
  ],
  "executive_narrative": "<3-4 sentences: tier, top strength, top gap, recommended next step>",
  "confidence": "<high|medium|low>"
}
```
"""


# ---------------------------------------------------------------------------
# Standalone scoring function (per specification)
# ---------------------------------------------------------------------------


def compute_questionnaire_scores(responses: list) -> dict:
    """Compute questionnaire-derived dimension scores from raw responses.

    This is a standalone function so it can be called independently of the
    agent (e.g. for testing or pre-computation in the orchestrator).

    Args:
        responses: List of response dicts compatible with QuestionResponse schema.
                   Each dict must have at minimum:
                   - question_id: str
                   - score: int | float | None
                   - skipped: bool (optional, defaults to False)

    Returns:
        dict matching the output of src.orchestrator.scoring.compute_all_scores:
        {
            "dimension_scores": {dimension_key: float},
            "overall_score": float,
            "overall_tier": str,
            "dimension_tiers": {dimension_key: str},
            "dimension_weights": {dimension_key: float},
            "questions_answered_per_dimension": {dimension_key: int},
            "questions_skipped_per_dimension": {dimension_key: int},
        }
    """
    return compute_all_scores(responses)


# ---------------------------------------------------------------------------
# Agent class
# ---------------------------------------------------------------------------


class C2SynthesisAgent(BaseAgent):
    """Agent C2: Core Synthesis and Scoring.

    Pre-computes questionnaire scores, then calls the Opus LLM to apply
    research adjustments, generate findings, and produce the complete
    SynthesisOutput structure.
    """

    agent_id = "C2_synthesis"
    model = settings.model_opus
    latency_budget_seconds = 120

    def run(self, inputs: dict) -> AgentResult:
        """Execute the synthesis pipeline.

        Args:
            inputs: dict with keys:
                - company_canonical_name (str, required)
                - primary_persona (str, required — P1|P2|P3)
                - company_industry_label (str, required)
                - questionnaire_responses_json (list, required — list of response dicts)
                - b1_output_json (dict, required — financial research output)
                - b2_output_json (dict, required — news research output)
                - b3_output_json (dict, required — tech stack inference output)
                - c1_output_json (dict, required — industry library mapping output)
                - b4_output_json (dict, optional — competitor intelligence output)
                - b5_output_json (dict, optional — regulatory context output)

        Returns:
            AgentResult whose .data matches the C2 SynthesisOutput structure.
        """
        start = time.time()

        # --- Validate required inputs ---
        required = [
            "company_canonical_name",
            "primary_persona",
            "company_industry_label",
            "questionnaire_responses_json",
            "b1_output_json",
            "b2_output_json",
            "b3_output_json",
            "c1_output_json",
        ]
        missing = [k for k in required if k not in inputs or inputs[k] is None]
        if missing:
            return AgentError(
                error=f"C2 missing required inputs: {missing}",
                agent_id=self.agent_id,
            )

        company_name = inputs["company_canonical_name"]
        persona = inputs["primary_persona"]
        industry = inputs["company_industry_label"]
        responses = inputs["questionnaire_responses_json"]
        b1 = inputs["b1_output_json"]
        b2 = inputs["b2_output_json"]
        b3 = inputs["b3_output_json"]
        c1 = inputs["c1_output_json"]
        b4 = inputs.get("b4_output_json") or {}
        b5 = inputs.get("b5_output_json") or {}

        # --- Step 1: Pre-compute questionnaire scores ---
        try:
            questionnaire_scores = compute_questionnaire_scores(responses)
        except Exception as exc:
            return AgentError(
                error=f"Questionnaire score computation failed: {exc}",
                agent_id=self.agent_id,
            )

        # --- Step 2: Build user prompt ---
        user_prompt = self._build_user_prompt(
            company_name=company_name,
            persona=persona,
            industry=industry,
            questionnaire_scores=questionnaire_scores,
            responses=responses,
            b1=b1,
            b2=b2,
            b3=b3,
            c1=c1,
            b4=b4,
            b5=b5,
        )

        # --- Step 3: Call Opus LLM ---
        # Scale token budget by model tier
        if self.model == settings.model_haiku:
            max_tok = 3000
        elif self.model == settings.model_sonnet:
            max_tok = 5000
        else:
            max_tok = 8000
        try:
            llm_result = self._call_llm(
                system_prompt=_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                max_tokens=max_tok,
            )
        except Exception as exc:
            return AgentError(
                error=f"LLM call failed in C2: {exc}",
                agent_id=self.agent_id,
            )

        # --- Step 4: Enrich output with computed metadata ---
        output = self._enrich_output(
            llm_result=llm_result,
            questionnaire_scores=questionnaire_scores,
            company_name=company_name,
        )

        confidence_label = output.get("confidence", "medium")
        confidence_float = {"high": 0.9, "medium": 0.7, "low": 0.5}.get(
            confidence_label, 0.7
        )

        return AgentResult(
            data=output,
            confidence=confidence_float,
            latency_ms=self._elapsed_ms(start),
            agent_id=self.agent_id,
        )

    # ------------------------------------------------------------------
    # Prompt construction
    # ------------------------------------------------------------------

    def _build_user_prompt(
        self,
        company_name: str,
        persona: str,
        industry: str,
        questionnaire_scores: dict,
        responses: list,
        b1: dict,
        b2: dict,
        b3: dict,
        c1: dict,
        b4: dict,
        b5: dict,
    ) -> str:
        """Construct the synthesis user prompt with all inputs."""
        persona_descriptions = {
            "P1": "Strategic / Executive (board and C-suite focus: competitive position, strategic risk, long-term value)",
            "P2": "Technical / Operational (CTO, CIO, engineering focus: systems, architecture, operational change)",
            "P3": "Financial / CFO (cost, ROI, capital allocation, payback period focus)",
        }
        persona_desc = persona_descriptions.get(persona, persona)

        dim_score_lines = []
        for dim, score in questionnaire_scores["dimension_scores"].items():
            display = DIMENSION_DISPLAY_NAMES.get(dim, dim)
            weight = DIMENSION_WEIGHTS[dim]
            tier = questionnaire_scores["dimension_tiers"].get(dim, "")
            answered = questionnaire_scores["questions_answered_per_dimension"].get(dim, 0)
            skipped = questionnaire_scores["questions_skipped_per_dimension"].get(dim, 0)
            dim_score_lines.append(
                f"  {display} (weight {weight:.0%}): {score:.1f}/100 [{tier}] "
                f"— {answered} answered, {skipped} skipped"
            )

        dim_scores_text = "\n".join(dim_score_lines)
        overall_q_score = questionnaire_scores["overall_score"]
        overall_q_tier = questionnaire_scores["overall_tier"]

        return f"""## Prospect

Company: {company_name}
Industry: {industry}
Primary persona: {persona} — {persona_desc}

---

## Pre-Computed Questionnaire Dimension Scores

These scores are computed from weighted question averages. They are your baseline before research adjustment.

{dim_scores_text}

Questionnaire overall score (before research adjustment): {overall_q_score:.1f}/100 [{overall_q_tier}]

---

## Raw Questionnaire Responses

```json
{json.dumps(responses, indent=2, default=str)}
```

---

## Financial Research Output (B1)

```json
{json.dumps(b1, indent=2, default=str)}
```

---

## News & Signals Research Output (B2)

```json
{json.dumps(b2, indent=2, default=str)}
```

---

## Technology Stack Inference Output (B3)

```json
{json.dumps(b3, indent=2, default=str)}
```

---

## Industry Process Library Mapping (C1)

```json
{json.dumps(c1, indent=2, default=str)}
```

---

## Competitor Intelligence Output (B4)

```json
{json.dumps(b4 if b4 else {"status": "not_available"}, indent=2, default=str)}
```

---

## Regulatory Context Output (B5)

```json
{json.dumps(b5 if b5 else {"status": "not_available"}, indent=2, default=str)}
```

---

## Your task

1. Review the questionnaire dimension scores above.
2. For each dimension, determine whether the research outputs (B1-B5) warrant an adjustment of -10 to +10 points. Cite specific evidence for any adjustment.
3. Compute adjusted scores and the overall composite score.
4. Generate 3-5 specific, evidence-grounded findings.
5. Produce the value-difficulty map.
6. Recommend exactly one next step.
7. Generate 0-3 partner attention flags for the DXC account team.
8. Write a 3-4 sentence executive narrative framed for {persona} persona.

Remember: every claim must be grounded in the data provided. Do not invent facts about {company_name}.

Return ONLY valid JSON as specified in your system prompt.
"""

    # ------------------------------------------------------------------
    # Output enrichment
    # ------------------------------------------------------------------

    def _enrich_output(
        self,
        llm_result: dict,
        questionnaire_scores: dict,
        company_name: str,
    ) -> dict:
        """Add questionnaire score metadata to the LLM output."""
        # Ensure questionnaire scores are embedded for downstream agents
        llm_result["questionnaire_scores"] = questionnaire_scores
        llm_result["company_canonical_name"] = company_name

        # Validate and clamp overall_score
        overall = float(llm_result.get("overall_score", questionnaire_scores["overall_score"]))
        overall = max(0.0, min(100.0, overall))
        llm_result["overall_score"] = round(overall, 1)

        # Ensure tier is consistent with score
        if "tier" not in llm_result or not llm_result["tier"]:
            llm_result["tier"] = get_tier(overall)

        return llm_result
