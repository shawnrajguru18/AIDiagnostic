"""Agent A3 - Question Personalization Agent.

Selects and personalises diagnostic questions from the pool based on the
prospect's inferred persona, company context, and industry.  Applies
persona-variant text and computes ordered positions.

Also exposes ``apply_skip_logic`` for adaptive filtering during questionnaire
completion (called by the API layer as the respondent submits answers).
"""

import json
import time
import uuid
from typing import Any

from src.config import settings
from src.agents.base import AgentResult, AgentError, BaseAgent
from src.data.questionnaire import get_question_pool


_SYSTEM_PROMPT = """You are a question personalisation assistant for the DXC AI Readiness Diagnostic. Your job is to select and adapt the most relevant diagnostic questions for a specific prospect, based on their persona, industry, and company context.

You will receive:
1. A prospect's persona (P1, P2, or P3) and company context
2. A question pool (JSON array of question objects)

Your task:
1. Select the most relevant questions for this persona and context. Aim for 12–18 questions total.
2. Apply persona_variant_text where available — replace the default question_text with the persona-specific variant.
3. Order the questions logically: start with higher-level strategic questions, progress to operational detail. Respect dimension groupings (Q1.x = Data Foundation, Q2.x = Governance, Q3.x = AI Investment, Q4.x = Change Readiness, Q5.x = Value Pockets, Q6.x = Regulatory).
4. Include at least 2 questions from each of the 6 dimensions.
5. Prioritise questions tagged for the prospect's persona, but include universal questions (persona_tags: null) as well.
6. Preserve the original question_id, dimension_id, question_type, weight, options, scale_anchors, max_chars, and skip_logic exactly as provided.
7. Add an ordered_position integer (1-based) to each selected question.
8. Add a rendered_text field containing the final adapted question text (after applying persona variant if applicable).
9. Add a skip_logic_dependencies field (array of question_ids that this question depends on — empty array if none).

Return ONLY structured JSON with this structure:
{
  "questionnaire_id": "<uuid4>",
  "persona": "<P1|P2|P3>",
  "selection_rationale": "<1-2 sentence explanation of the selection strategy>",
  "estimated_completion_minutes": <integer>,
  "selected_questions": [
    {
      "question_id": "<string>",
      "ordered_position": <integer>,
      "dimension_id": "<string>",
      "rendered_text": "<string — final question text after persona adaptation>",
      "question_type": "<string>",
      "weight": <float>,
      "options": <array or null>,
      "scale_anchors": <array or null>,
      "max_chars": <integer or null>,
      "helper_text": <string or null>,
      "skip_logic": <object or null>,
      "skip_logic_dependencies": []
    }
  ]
}

Do not include any question not present in the provided pool. Do not invent new question_ids."""


class A3QuestionsAgent(BaseAgent):
    """Agent A3: Question Personalization."""

    agent_id = "A3_questions"
    model = settings.model_sonnet
    latency_budget_seconds = 45

    # ------------------------------------------------------------------
    # Core run method
    # ------------------------------------------------------------------

    def run(self, inputs: dict) -> AgentResult:
        """Select and personalise questions for a prospect.

        Args:
            inputs: dict with keys:
                - persona_data (dict): output .data from A2PersonaAgent.run()
                - company_context (dict): output .data from A1IntakeAgent.run()
                - question_pool (list, optional): if omitted, the default pool
                  is loaded from src.data.questionnaire

        Returns:
            AgentResult whose .data matches the A3 output schema
            (PersonalizedQuestionnaire structure).
        """
        start = time.time()

        persona_data: dict = inputs.get("persona_data") or {}
        company_context: dict = inputs.get("company_context") or {}

        persona = persona_data.get("assigned_persona", "P2")
        if persona not in ("P1", "P2", "P3"):
            persona = "P2"

        # Load question pool
        question_pool: list = inputs.get("question_pool") or get_question_pool()

        # Extract company details from A1 normalised output
        normalized: dict = company_context.get("normalized") or company_context
        company_name = normalized.get("company_canonical_name", "the prospect company")
        industry_label = normalized.get("company_industry_label", "")
        size_band = normalized.get("company_size_band_estimate", "unknown")
        hq_country = normalized.get("company_hq_country", "")
        prospect_role = normalized.get("prospect_role", persona_data.get("prospect_role", ""))

        # Build LLM prompt
        context_block = (
            f"Persona: {persona}\n"
            f"Company: {company_name}\n"
            f"Industry: {industry_label}\n"
            f"Size band: {size_band}\n"
            f"HQ country: {hq_country}\n"
            f"Prospect role: {prospect_role}\n"
            f"Persona reasoning: {persona_data.get('reasoning', '')}\n"
            f"Primary concerns: {json.dumps(persona_data.get('primary_concerns', []))}"
        )

        user_prompt = (
            f"Personalise the diagnostic questionnaire for the following prospect:\n\n"
            f"{context_block}\n\n"
            f"Question pool (JSON):\n"
            f"{json.dumps(question_pool, indent=2)}\n\n"
            f"Return only the JSON structure as specified."
        )

        try:
            llm_result = self._call_llm(_SYSTEM_PROMPT, user_prompt, max_tokens=4096)
        except Exception as exc:
            return AgentError(
                error=f"LLM question personalisation failed: {exc}",
                agent_id=self.agent_id,
            )

        # ---- Normalise output ----
        questionnaire_id = str(uuid.uuid4())
        llm_result["questionnaire_id"] = questionnaire_id
        llm_result.setdefault("persona", persona)
        llm_result.setdefault("selection_rationale", "")
        llm_result.setdefault("selected_questions", [])
        llm_result.setdefault("estimated_completion_minutes", 10)

        # Ensure each selected question has skip_logic_dependencies
        for q in llm_result.get("selected_questions", []):
            q.setdefault("skip_logic_dependencies", [])
            q.setdefault("rendered_text", q.get("question_text", ""))

        total_questions = len(llm_result.get("selected_questions", []))

        # Build the PersonalizedQuestionnaire-compatible output
        output = {
            "questionnaire_id": questionnaire_id,
            "prospect_id": company_context.get("prospect_id", ""),
            "persona": persona,
            "questions": llm_result.get("selected_questions", []),
            "total_questions": total_questions,
            "estimated_minutes": llm_result.get("estimated_completion_minutes", 10),
            "selection_rationale": llm_result.get("selection_rationale", ""),
        }

        # Confidence based on pool coverage: ratio of selected to total available
        pool_size = len(question_pool) or 1
        coverage = min(total_questions / pool_size, 1.0)
        numeric_confidence = max(0.5, min(0.95, 0.6 + coverage * 0.35))

        return AgentResult(
            data=output,
            confidence=numeric_confidence,
            latency_ms=self._elapsed_ms(start),
            agent_id=self.agent_id,
        )

    # ------------------------------------------------------------------
    # Adaptive skip logic
    # ------------------------------------------------------------------

    @staticmethod
    def apply_skip_logic(responses: dict, questions: list) -> list:
        """Filter questions to skip based on responses received so far.

        This is called by the API layer during an in-progress questionnaire
        to determine which questions should be presented next.

        Args:
            responses: dict mapping question_id -> selected_option (str) or
                       list of selected_option_ids (list[str]) for multi-select.
            questions: the ordered list of PersonalizedQuestion dicts (from
                       the questionnaire's `questions` field).

        Returns:
            Filtered list of question dicts, with skipped questions removed.
            The ordering of the remaining questions is preserved.
        """
        # Collect all question_ids that should be skipped
        skip_targets: set[str] = set()

        for question in questions:
            skip_logic: dict | None = question.get("skip_logic")
            if not skip_logic:
                continue

            q_id = question.get("question_id", "")
            response = responses.get(q_id)
            if response is None:
                continue  # Not yet answered — do not skip based on this

            # Normalise to a list for uniform handling
            if isinstance(response, str):
                answered_options = [response]
            elif isinstance(response, list):
                answered_options = response
            else:
                answered_options = [str(response)]

            # Evaluate each condition in skip_logic
            # Format: { "<option_id>": { "skip_to": "<qid>", "reason": "..." } }
            for option_id, action in skip_logic.items():
                if option_id in answered_options:
                    skip_target = action.get("skip_to") if isinstance(action, dict) else None
                    if skip_target:
                        # Skip all questions between current position and skip_target
                        current_pos = question.get("ordered_position", 0)
                        for candidate in questions:
                            candidate_pos = candidate.get("ordered_position", 0)
                            candidate_id = candidate.get("question_id", "")
                            # Skip questions that come after current but before skip_target
                            if (
                                candidate_pos > current_pos
                                and candidate_id != skip_target
                                and not _is_at_or_after(candidate_id, skip_target, questions)
                            ):
                                skip_targets.add(candidate_id)

        return [q for q in questions if q.get("question_id") not in skip_targets]


def _is_at_or_after(question_id: str, target_id: str, questions: list) -> bool:
    """Return True if question_id appears at or after target_id in the ordered list."""
    seen_target = False
    for q in questions:
        qid = q.get("question_id", "")
        if qid == target_id:
            seen_target = True
        if seen_target and qid == question_id:
            return True
    return False
