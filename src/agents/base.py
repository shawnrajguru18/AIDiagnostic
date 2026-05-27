import anthropic
import json
import re
import time
import uuid
from typing import Any, Optional

from src.config import settings


class AgentResult:
    """Successful result from an agent run."""

    def __init__(self, data: dict, confidence: float, latency_ms: int, agent_id: str):
        self.data = data
        self.confidence = confidence
        self.latency_ms = latency_ms
        self.agent_id = agent_id
        self.success = True
        self.error = None

    def __repr__(self) -> str:
        return (
            f"AgentResult(agent_id={self.agent_id!r}, success={self.success}, "
            f"confidence={self.confidence}, latency_ms={self.latency_ms})"
        )


class AgentError(AgentResult):
    """Error result from an agent run."""

    def __init__(self, error: str, agent_id: str):
        self.data = {}
        self.confidence = 0.0
        self.latency_ms = 0
        self.agent_id = agent_id
        self.success = False
        self.error = error

    def __repr__(self) -> str:
        return f"AgentError(agent_id={self.agent_id!r}, error={self.error!r})"


class BaseAgent:
    """Abstract base class for all diagnostic agents."""

    agent_id: str = "base"
    model: str = settings.model_sonnet
    latency_budget_seconds: int = 60

    def __init__(self):
        key = settings.anthropic_api_key
        if key and key.startswith("sk-ant-si-"):
            self.client = anthropic.Anthropic(auth_token=key)
        else:
            self.client = anthropic.Anthropic(api_key=key)

    # ------------------------------------------------------------------
    # LLM helpers
    # ------------------------------------------------------------------

    def _call_llm(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
    ) -> dict:
        """Call Claude and return the parsed JSON response.

        Raises:
            ValueError: if the LLM response cannot be parsed as JSON.
            anthropic.APIError: for any upstream API error.
        """
        message = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        raw_content = message.content[0].text if message.content else ""
        return self._parse_json_response(raw_content)

    def _parse_json_response(self, content: str) -> dict:
        """Extract JSON from an LLM response.

        Handles raw JSON as well as JSON wrapped inside markdown code fences
        (```json ... ``` or ``` ... ```).
        """
        # Strip leading/trailing whitespace
        text = content.strip()

        # Try to extract from markdown code block first
        fence_match = re.search(
            r"```(?:json)?\s*\n([\s\S]*?)\n```",
            text,
            re.IGNORECASE,
        )
        if fence_match:
            text = fence_match.group(1).strip()

        # Attempt direct JSON parse
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try to find the outermost JSON object in the string as a fallback
        obj_match = re.search(r"\{[\s\S]*\}", text)
        if obj_match:
            try:
                return json.loads(obj_match.group())
            except json.JSONDecodeError:
                pass

        # Last resort: find first { and try incremental truncation to find valid JSON
        brace_start = text.find("{")
        if brace_start != -1:
            candidate = text[brace_start:]
            # Walk back from end to find outermost closing brace
            for end in range(len(candidate), 0, -1):
                if candidate[end - 1] == "}":
                    try:
                        return json.loads(candidate[:end])
                    except json.JSONDecodeError:
                        continue

        raise ValueError(
            f"Could not parse JSON from LLM response. Raw content (first 500 chars): "
            f"{content[:500]}"
        )

    # ------------------------------------------------------------------
    # Timing helper
    # ------------------------------------------------------------------

    @staticmethod
    def _elapsed_ms(start: float) -> int:
        """Return elapsed milliseconds since *start* (as returned by time.time())."""
        return int((time.time() - start) * 1000)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def run(self, inputs: dict) -> AgentResult:
        """Execute the agent.  Must be overridden by subclasses."""
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement run(inputs)."
        )
