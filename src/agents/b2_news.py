"""Agent B2 - Company News Research Agent.

Searches NewsAPI.org for recent news about the prospect company and synthesises
AI-related signals, competitive dynamics, and regulatory mentions into the B2
output schema.

If ``settings.news_api_key`` is empty or invalid, the agent falls back to a
stub response with research_status: "limited_public_data" and a note about the
missing API key.
"""

import json
import time
import uuid
from datetime import date, timedelta
from typing import Any, Optional

import httpx

from src.config import settings
from src.agents.base import AgentResult, AgentError, BaseAgent


_SYSTEM_PROMPT = """You are a company news research assistant for the DXC AI Readiness Diagnostic. Your job is to analyse recent news articles about a prospect company and extract signals relevant to AI readiness, competitive position, and regulatory exposure.

You will receive a list of news articles (title, description, URL, published date) retrieved from a news search API.

From this information, extract and categorise:
1. AI investment signals — announcements of AI spending, model deployments, AI partnerships, GenAI pilots
2. AI leadership hire signals — appointment of Chief AI Officers, AI VPs, data science leaders
3. AI product launch signals — new AI-powered products, features, or services
4. Regulatory action signals — fines, investigations, compliance announcements, data breaches
5. Competitor move signals — rival companies announcing AI initiatives that create competitive pressure
6. Partnership signals — strategic alliances, ecosystem plays, joint ventures
7. Risk event signals — financial distress, restructuring, major litigation, supply chain events

Also identify:
- Any competitor company names mentioned frequently alongside the prospect
- Any regulatory frameworks or government bodies mentioned
- An overall narrative about the company's AI posture (1–2 sentences)

If no articles are provided (API key missing or no results), acknowledge the limitation and return a minimal but valid structure with research_status: "limited_public_data".

Return ONLY structured JSON. No explanation outside the JSON structure.

Return JSON with exactly this structure:
{
  "research_id": "<uuid4>",
  "research_status": "<complete|partial|limited_public_data>",
  "total_articles_reviewed": <integer>,
  "ai_signals": [
    {
      "signal_id": "<uuid4>",
      "headline": "<string>",
      "summary": "<string — 1-2 sentences>",
      "url": "<string or null>",
      "published_date": "<YYYY-MM-DD or null>",
      "signal_type": "<ai_investment|ai_leadership_hire|ai_product_launch|regulatory_action|competitor_move|partnership|risk_event>",
      "sentiment": "<positive|neutral|negative>",
      "relevance_score": <float 0.0-1.0>
    }
  ],
  "competitor_mentions": ["<company name>"],
  "regulatory_mentions": ["<framework or body name>"],
  "overall_ai_narrative": "<string or null>",
  "sources": [
    {
      "source_type": "news",
      "url": "<string or null>",
      "title": "<string>",
      "published_date": "<YYYY-MM-DD or null>",
      "relevance_score": <float 0.0-1.0>
    }
  ],
  "notes": "<any caveats about data quality or coverage gaps>",
  "confidence": "<high|medium|low>"
}"""


# ---------------------------------------------------------------------------
# NewsAPI helpers
# ---------------------------------------------------------------------------

_NEWSAPI_BASE = "https://newsapi.org/v2/everything"
_HTTP_TIMEOUT = 15
_MAX_ARTICLES_TO_LLM = 20  # cap to stay within token budget
_AI_KEYWORDS = (
    "artificial intelligence OR \"machine learning\" OR \"generative AI\" "
    "OR \"large language model\" OR \"digital transformation\" OR \"AI strategy\""
)


def _search_newsapi(
    company_name: str,
    api_key: str,
    from_date: str,
    to_date: str,
    page_size: int = 30,
) -> Optional[list]:
    """Query NewsAPI.org and return a list of article dicts, or None on failure."""
    query = f'"{company_name}" AND ({_AI_KEYWORDS})'
    try:
        with httpx.Client(timeout=_HTTP_TIMEOUT) as client:
            resp = client.get(
                _NEWSAPI_BASE,
                params={
                    "q": query,
                    "from": from_date,
                    "to": to_date,
                    "language": "en",
                    "sortBy": "relevancy",
                    "pageSize": page_size,
                    "apiKey": api_key,
                },
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == "ok":
                    return data.get("articles", [])
            # Log status without raising — caller handles None
    except Exception:
        pass
    return None


def _format_articles_for_llm(articles: list) -> str:
    """Serialise a capped list of articles into a compact text block for the LLM."""
    capped = articles[:_MAX_ARTICLES_TO_LLM]
    lines = []
    for i, article in enumerate(capped, start=1):
        lines.append(
            f"[{i}] {article.get('publishedAt', 'unknown date')[:10]} | "
            f"{article.get('title', '(no title)')} | "
            f"{article.get('description', '(no description)')[:200]} | "
            f"URL: {article.get('url', '')}"
        )
    return "\n".join(lines) if lines else "(no articles)"


# ---------------------------------------------------------------------------
# Agent class
# ---------------------------------------------------------------------------

class B2NewsAgent(BaseAgent):
    """Agent B2: Company News Research."""

    agent_id = "B2_news"
    model = settings.model_sonnet
    latency_budget_seconds = 120

    def run(self, inputs: dict) -> AgentResult:
        """Research recent news and AI signals for the prospect company.

        Args:
            inputs: dict with keys:
                - company_canonical_name (str, required)
                - company_industry_label (str, optional)
                - date_24_months_ago (str, optional) — ISO date "YYYY-MM-DD";
                  defaults to 24 months before today
                - today (str, optional) — ISO date "YYYY-MM-DD"; defaults to today
                - prospect_id (str, optional)

        Returns:
            AgentResult whose .data matches the B2 output schema (NewsResearch).
        """
        start = time.time()

        company_name = (inputs.get("company_canonical_name") or "").strip()
        if not company_name:
            return AgentError(
                error="company_canonical_name is required for B2 news research",
                agent_id=self.agent_id,
            )

        industry_label = (inputs.get("company_industry_label") or "").strip()
        prospect_id = (inputs.get("prospect_id") or "").strip()

        # Date range
        today_str: str = inputs.get("today") or date.today().isoformat()
        from_str: str = inputs.get("date_24_months_ago") or (
            date.today() - timedelta(days=730)
        ).isoformat()

        api_key: str = settings.news_api_key or ""
        articles: Optional[list] = None
        articles_block = "(no articles — NewsAPI key not configured)"

        # ---- Attempt NewsAPI fetch ----
        if api_key:
            articles = _search_newsapi(company_name, api_key, from_str, today_str)
            if articles is not None:
                articles_block = _format_articles_for_llm(articles)
            else:
                articles_block = "(NewsAPI request failed — possible network error or invalid key)"
        else:
            articles_block = (
                "(NewsAPI key not configured — using LLM training knowledge only. "
                "Set NEWS_API_KEY in environment to enable live news retrieval.)"
            )

        # ---- Build LLM synthesis prompt ----
        user_prompt = f"""Analyse recent news and AI signals for the following company for the DXC AI Readiness Diagnostic:

Company: {company_name}
Industry: {industry_label or "unknown"}
Date range searched: {from_str} to {today_str}
Total articles retrieved: {len(articles) if articles is not None else 0}

Articles:
{articles_block}

Return only the JSON structure as specified in your system prompt.

If no articles were retrieved, set research_status to "limited_public_data" and use your training knowledge about this company to populate what you can, noting the limitation in the "notes" field.
If articles were retrieved, set research_status to "complete" (or "partial" if the coverage seems incomplete)."""

        try:
            llm_result = self._call_llm(_SYSTEM_PROMPT, user_prompt, max_tokens=3000)
        except Exception as exc:
            return AgentError(
                error=f"LLM news synthesis failed: {exc}",
                agent_id=self.agent_id,
            )

        # ---- Normalise output ----
        llm_result["research_id"] = str(uuid.uuid4())
        llm_result["prospect_id"] = prospect_id
        llm_result.setdefault("research_status", "limited_public_data" if not api_key else "complete")
        llm_result.setdefault("total_articles_reviewed", len(articles) if articles else 0)
        llm_result.setdefault("ai_signals", [])
        llm_result.setdefault("competitor_mentions", [])
        llm_result.setdefault("regulatory_mentions", [])
        llm_result.setdefault("overall_ai_narrative", None)
        llm_result.setdefault("sources", [])
        llm_result.setdefault("notes", "" if api_key else "NewsAPI key not configured; results based on LLM training knowledge only.")
        llm_result.setdefault("confidence", "low" if not api_key else "medium")

        # Ensure each ai_signal has a signal_id
        for signal in llm_result.get("ai_signals", []):
            signal.setdefault("signal_id", str(uuid.uuid4()))

        confidence_map = {"high": 0.85, "medium": 0.6, "low": 0.3}
        numeric_confidence = confidence_map.get(llm_result.get("confidence", "medium"), 0.6)

        # Boost if we got real articles
        if articles:
            numeric_confidence = min(numeric_confidence + 0.1, 0.9)

        return AgentResult(
            data=llm_result,
            confidence=numeric_confidence,
            latency_ms=self._elapsed_ms(start),
            agent_id=self.agent_id,
        )
