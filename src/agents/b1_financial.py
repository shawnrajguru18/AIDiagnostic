"""Agent B1 - Company Financial Research Agent.

Retrieves and synthesises financial intelligence for a prospect company.
For US-listed companies it queries the SEC EDGAR API directly; for private
or non-US companies it falls back to LLM-only synthesis with a note about
data limitations.

Latency budget: 5 minutes (V0 cap; full budget is 30 min per Companion 04).
"""

import json
import time
import uuid
from typing import Any, Optional

import httpx

from src.config import settings
from src.agents.base import AgentResult, AgentError, BaseAgent


_SYSTEM_PROMPT = """You are a company financial research assistant for the DXC AI Readiness Diagnostic. Your job is to synthesise available financial intelligence about a prospect company and identify signals relevant to AI readiness and investment capacity.

You will receive company identifying information and, where available, extracts from SEC EDGAR filings (10-K and 10-Q).

From this information, extract and infer:
1. Revenue scale and employee count (use ranges if exact figures are unavailable)
2. Recent M&A activity, strategic partnerships, or divestiture events
3. AI and digital transformation signals — look for mentions of AI, machine learning, generative AI, digital transformation, cloud migration, data platform investments
4. CapEx trend — is the company investing more or less over recent periods?
5. Any signals about technology investment appetite

If SEC EDGAR data is available: ground your analysis in the actual filing content.
If SEC EDGAR data is not available (private company or non-US entity): use your training knowledge, clearly noting this is inferred from public sources, not filed data.

Return ONLY structured JSON. No explanation outside the JSON structure.

Return JSON with exactly this structure:
{
  "research_id": "<uuid4>",
  "research_status": "<complete|partial|limited_public_data>",
  "data_source": "<sec_edgar|llm_inference|mixed>",
  "ticker": "<string or null>",
  "cik": "<string or null>",
  "revenue_usd_millions": <float or null>,
  "revenue_range_label": "<string or null — e.g. '$1B–$5B'>",
  "employee_count": <integer or null>,
  "employee_range_label": "<string or null>",
  "recent_ma_events": [
    {
      "event_type": "<merger|acquisition|divestiture|ipo|partnership>",
      "description": "<string>",
      "date": "<YYYY-MM or null>",
      "value_usd_millions": <float or null>,
      "counterparty": "<string or null>"
    }
  ],
  "ai_mentions_in_filings": <integer>,
  "ai_investment_signals": ["<signal text>"],
  "capex_trend": "<increasing|stable|decreasing|unknown>",
  "digital_transformation_signals": ["<signal text>"],
  "notes": "<any caveats about data quality or source limitations>",
  "sources": [
    {
      "source_type": "<sec_filing|news|press_release|web>",
      "url": "<string or null>",
      "title": "<string or null>",
      "published_date": "<YYYY-MM-DD or null>",
      "relevance_score": <float 0.0-1.0>
    }
  ],
  "confidence": "<high|medium|low>"
}"""


# ---------------------------------------------------------------------------
# SEC EDGAR helpers
# ---------------------------------------------------------------------------

_EDGAR_SEARCH_URL = "https://efts.sec.gov/LATEST/search-index"
_EDGAR_SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
_EDGAR_COMPANY_SEARCH_URL = "https://www.sec.gov/cgi-bin/browse-edgar"

_EDGAR_HEADERS = {
    "User-Agent": "DXC-AI-Diagnostic research@dxc.com",
    "Accept": "application/json",
}

# V0 timeout per external call (seconds)
_HTTP_TIMEOUT = 15
# Max chars of filing text to send to LLM
_FILING_EXCERPT_MAX_CHARS = 6000
# V0 total elapsed budget before returning partial results (seconds)
_AGENT_TIMEOUT_SECONDS = 300


def _search_edgar_company(company_name: str, ticker: Optional[str]) -> Optional[dict]:
    """Search SEC EDGAR for a company by ticker or name.

    Returns a dict with at least {"cik": str, "name": str} or None if not found.
    """
    try:
        with httpx.Client(timeout=_HTTP_TIMEOUT, headers=_EDGAR_HEADERS) as client:
            # Prefer ticker lookup (more reliable)
            if ticker:
                resp = client.get(
                    _EDGAR_COMPANY_SEARCH_URL,
                    params={"action": "getcompany", "company": ticker, "type": "10-K",
                            "dateb": "", "owner": "include", "count": "5",
                            "search_text": "", "output": "atom"},
                )
                if resp.status_code == 200:
                    # Parse minimal CIK from atom feed
                    cik = _extract_cik_from_atom(resp.text)
                    if cik:
                        return {"cik": cik, "name": company_name}

            # Fall back to full-text search
            resp = client.get(
                "https://efts.sec.gov/LATEST/search-index",
                params={
                    "q": f'"{company_name}"',
                    "dateRange": "custom",
                    "startdt": "2022-01-01",
                    "forms": "10-K",
                    "hits.hits.total.value": "1",
                },
            )
            if resp.status_code == 200:
                data = resp.json()
                hits = data.get("hits", {}).get("hits", [])
                if hits:
                    source = hits[0].get("_source", {})
                    entity_id = source.get("entity_id") or source.get("file_num", "")
                    return {"cik": entity_id, "name": company_name}
    except Exception:
        pass
    return None


def _extract_cik_from_atom(atom_text: str) -> Optional[str]:
    """Minimal regex-free CIK extraction from SEC EDGAR atom feed."""
    import re
    match = re.search(r"CIK=(\d+)", atom_text)
    return match.group(1).zfill(10) if match else None


def _fetch_company_submissions(cik: str) -> Optional[dict]:
    """Fetch company submission metadata from SEC EDGAR."""
    try:
        url = _EDGAR_SUBMISSIONS_URL.format(cik=cik.zfill(10))
        with httpx.Client(timeout=_HTTP_TIMEOUT, headers=_EDGAR_HEADERS) as client:
            resp = client.get(url)
            if resp.status_code == 200:
                return resp.json()
    except Exception:
        pass
    return None


def _fetch_recent_filing_text(cik: str, form_type: str = "10-K") -> Optional[str]:
    """Fetch a short excerpt from the most recent 10-K or 10-Q filing via EDGAR search."""
    try:
        with httpx.Client(timeout=_HTTP_TIMEOUT, headers=_EDGAR_HEADERS) as client:
            resp = client.get(
                _EDGAR_SEARCH_URL,
                params={
                    "q": f"artificial intelligence machine learning digital transformation",
                    "dateRange": "custom",
                    "startdt": "2023-01-01",
                    "forms": form_type,
                    "entity": cik,
                },
            )
            if resp.status_code != 200:
                return None
            data = resp.json()
            hits = data.get("hits", {}).get("hits", [])
            if not hits:
                return None
            # Return the display_date_filed and entity info along with excerpt
            first = hits[0].get("_source", {})
            excerpt_parts = [
                f"Filing: {first.get('form_type', form_type)}",
                f"Filed: {first.get('file_date', 'unknown')}",
                f"Entity: {first.get('entity_name', '')}",
                f"Description: {first.get('file_description', '')}",
            ]
            return "\n".join(excerpt_parts)
    except Exception:
        return None


def _extract_financials_from_submissions(subs: dict) -> dict:
    """Pull financial context from EDGAR submission metadata."""
    result: dict = {}

    # Company basics
    result["company_name"] = subs.get("name", "")
    result["ticker"] = (subs.get("tickers") or [""])[0] or None
    result["cik"] = subs.get("cik", "")
    result["sic_description"] = subs.get("sicDescription", "")
    result["business_address"] = subs.get("addresses", {}).get("business", {})

    # Recent filings summary
    filings = subs.get("filings", {}).get("recent", {})
    forms = filings.get("form", [])
    dates = filings.get("filingDate", [])
    accessions = filings.get("accessionNumber", [])

    annual_filings = [
        {"form": f, "date": d, "accession": a}
        for f, d, a in zip(forms, dates, accessions)
        if f in ("10-K", "10-K/A")
    ]
    result["recent_10k_filings"] = annual_filings[:3]

    quarterly_filings = [
        {"form": f, "date": d, "accession": a}
        for f, d, a in zip(forms, dates, accessions)
        if f in ("10-Q", "10-Q/A")
    ]
    result["recent_10q_filings"] = quarterly_filings[:4]

    return result


# ---------------------------------------------------------------------------
# Agent class
# ---------------------------------------------------------------------------

class B1FinancialAgent(BaseAgent):
    """Agent B1: Company Financial Research."""

    agent_id = "B1_financial"
    model = settings.model_sonnet
    latency_budget_seconds = 300  # 5-minute V0 cap

    def run(self, inputs: dict) -> AgentResult:
        """Research the prospect company's financial profile.

        Args:
            inputs: dict with keys:
                - company_canonical_name (str, required)
                - company_ticker (str, optional)
                - company_lei (str, optional)
                - company_hq_country (str, optional)
                - company_industry_label (str, optional)
                - prospect_id (str, optional)

        Returns:
            AgentResult whose .data matches the B1 output schema (FinancialResearch).
        """
        start = time.time()

        company_name = (inputs.get("company_canonical_name") or "").strip()
        if not company_name:
            return AgentError(
                error="company_canonical_name is required for B1 financial research",
                agent_id=self.agent_id,
            )

        ticker = (inputs.get("company_ticker") or "").strip() or None
        hq_country = (inputs.get("company_hq_country") or "").strip()
        industry_label = (inputs.get("company_industry_label") or "").strip()
        prospect_id = (inputs.get("prospect_id") or "").strip()

        edgar_context: dict = {}
        filing_excerpt: Optional[str] = None
        data_source = "llm_inference"
        sources: list = []

        # ---- Attempt SEC EDGAR lookup (US companies only) ----
        is_us_company = hq_country.upper() in ("US", "USA", "UNITED STATES", "")
        if is_us_company and self._elapsed_ms(start) / 1000 < _AGENT_TIMEOUT_SECONDS - 30:
            try:
                company_info = _search_edgar_company(company_name, ticker)
                if company_info and company_info.get("cik"):
                    cik = company_info["cik"]
                    subs = _fetch_company_submissions(cik)
                    if subs:
                        edgar_context = _extract_financials_from_submissions(subs)
                        data_source = "sec_edgar"
                        sources.append({
                            "source_type": "sec_filing",
                            "url": f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}",
                            "title": f"SEC EDGAR filings — {company_name}",
                            "published_date": None,
                            "relevance_score": 0.9,
                        })

                    # Fetch AI-keyword excerpt from recent filing
                    if self._elapsed_ms(start) / 1000 < _AGENT_TIMEOUT_SECONDS - 30:
                        filing_excerpt = _fetch_recent_filing_text(cik, "10-K")
                        if not filing_excerpt:
                            filing_excerpt = _fetch_recent_filing_text(cik, "10-Q")
            except Exception as edgar_exc:
                # Non-fatal: fall back to LLM-only
                edgar_context["edgar_error"] = str(edgar_exc)

        # ---- Build LLM synthesis prompt ----
        edgar_block = (
            f"SEC EDGAR data:\n{json.dumps(edgar_context, indent=2)}"
            if edgar_context
            else "SEC EDGAR data: not available (private company or non-US entity)"
        )
        filing_block = (
            f"Recent filing AI/digital excerpt:\n{filing_excerpt[:_FILING_EXCERPT_MAX_CHARS]}"
            if filing_excerpt
            else "Filing excerpt: not available"
        )

        user_prompt = f"""Synthesise financial and strategic intelligence for the following company for the DXC AI Readiness Diagnostic:

Company: {company_name}
Ticker: {ticker or "unknown"}
Industry: {industry_label or "unknown"}
HQ country: {hq_country or "unknown"}

{edgar_block}

{filing_block}

Data source used: {data_source}

Return only the JSON structure as specified in your system prompt. Set research_status to:
- "complete" if you have SEC EDGAR data and filing excerpts
- "partial" if you have EDGAR metadata but no filing excerpts
- "limited_public_data" if no EDGAR data was found

Fill all numeric fields you can infer; use null for truly unknown values."""

        try:
            llm_result = self._call_llm(_SYSTEM_PROMPT, user_prompt, max_tokens=2048)
        except Exception as exc:
            return AgentError(
                error=f"LLM financial synthesis failed: {exc}",
                agent_id=self.agent_id,
            )

        # ---- Normalise output ----
        llm_result["research_id"] = str(uuid.uuid4())
        llm_result["prospect_id"] = prospect_id
        llm_result.setdefault("data_source", data_source)
        llm_result.setdefault("research_status", "limited_public_data")
        llm_result.setdefault("ticker", ticker)
        llm_result.setdefault("cik", edgar_context.get("cik"))
        llm_result.setdefault("revenue_usd_millions", None)
        llm_result.setdefault("revenue_range_label", None)
        llm_result.setdefault("employee_count", None)
        llm_result.setdefault("employee_range_label", None)
        llm_result.setdefault("recent_ma_events", [])
        llm_result.setdefault("ai_mentions_in_filings", 0)
        llm_result.setdefault("ai_investment_signals", [])
        llm_result.setdefault("capex_trend", "unknown")
        llm_result.setdefault("digital_transformation_signals", [])
        llm_result.setdefault("notes", "")
        llm_result.setdefault("confidence", "medium")

        # Merge sources
        existing_sources = llm_result.get("sources", [])
        merged_sources = sources + [
            s for s in existing_sources
            if s.get("url") not in {x.get("url") for x in sources}
        ]
        llm_result["sources"] = merged_sources

        confidence_map = {"high": 0.85, "medium": 0.55, "low": 0.3}
        numeric_confidence = confidence_map.get(llm_result.get("confidence", "medium"), 0.55)

        # Boost confidence if we have real EDGAR data
        if data_source == "sec_edgar":
            numeric_confidence = min(numeric_confidence + 0.15, 0.95)

        return AgentResult(
            data=llm_result,
            confidence=numeric_confidence,
            latency_ms=self._elapsed_ms(start),
            agent_id=self.agent_id,
        )
