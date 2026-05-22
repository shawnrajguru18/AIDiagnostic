"""
PDF renderer for the DXC AI Readiness Diagnostic V0.
Uses WeasyPrint + Jinja2 to generate print-quality PDFs for:
  1. The one-page Scorecard
  2. The Quick Wins Memo
  3. The Findings Appendix (5-8 pages)
"""

from __future__ import annotations

import os
from typing import Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import CSS, HTML

# ---------------------------------------------------------------------------
# Template directory — two levels up from this file: project_root/templates/
# ---------------------------------------------------------------------------

TEMPLATES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "templates")
)

# ---------------------------------------------------------------------------
# Jinja2 environment (shared)
# ---------------------------------------------------------------------------

_jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(["html", "xml"]),
)

# ---------------------------------------------------------------------------
# Brand constants injected into every template context
# ---------------------------------------------------------------------------

_BRAND = {
    "color_canvas": "#F6F3F0",
    "color_midnight": "#0E1020",
    "color_body": "#3D3F50",
    "color_peach": "#FFC982",
    "color_gold": "#FFAE41",
    "color_sky": "#A1E6FF",
    "color_true_blue": "#4995FF",
    "color_royal": "#004AAC",
    "tier_colors": {
        "Emerging": "#FFC982",
        "Developing": "#FFAE41",
        "Established": "#A1E6FF",
        "Leading": "#4995FF",
    },
}


def _render_html(template_name: str, context: dict) -> str:
    """Render a Jinja2 template to an HTML string."""
    template = _jinja_env.get_template(template_name)
    full_context = {**_BRAND, **context}
    return template.render(**full_context)


def _html_to_pdf(html_string: str) -> bytes:
    """Convert an HTML string to PDF bytes via WeasyPrint."""
    document = HTML(string=html_string, base_url=TEMPLATES_DIR)
    return document.write_pdf()


def _save_pdf(pdf_bytes: bytes, output_path: Optional[str]) -> None:
    """Optionally write PDF bytes to disk."""
    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "wb") as fh:
            fh.write(pdf_bytes)


# ---------------------------------------------------------------------------
# Public rendering functions
# ---------------------------------------------------------------------------


def render_scorecard_pdf(
    scorecard_data: dict,
    radar_chart_b64: str,
    output_path: Optional[str] = None,
) -> bytes:
    """Render the one-page AI Readiness Scorecard PDF.

    Args:
        scorecard_data: Dict expected to contain at minimum:
            - company_name (str)
            - assessment_date (str, formatted)
            - overall_score (int/float)
            - overall_tier (str)
            - tier_color (str, hex)
            - dimension_scores (list of dicts with keys: name, score, tier, tier_color)
            - findings (list of dicts with keys: number, headline)
            - recommended_next_step (dict with keys: title, description)
            - quick_wins_items (list of str)
        radar_chart_b64: Data-URI string ("data:image/png;base64,...") for <img src>.
        output_path: Optional filesystem path to write the PDF.

    Returns:
        Raw PDF bytes.
    """
    context = {**scorecard_data, "radar_chart_b64": radar_chart_b64}
    html = _render_html("scorecard.html", context)
    pdf_bytes = _html_to_pdf(html)
    _save_pdf(pdf_bytes, output_path)
    return pdf_bytes


def render_quick_wins_memo_pdf(
    memo_data: dict,
    output_path: Optional[str] = None,
) -> bytes:
    """Render the one-page Quick Wins Memo PDF.

    Args:
        memo_data: Dict expected to contain at minimum:
            - company_name (str)
            - intro_paragraph (str)
            - pattern_cards (list of dicts with keys: pattern_name, description,
              what_it_does, prerequisites, expected_outcome, timeline)
            - footer_contact (str)
        output_path: Optional filesystem path to write the PDF.

    Returns:
        Raw PDF bytes.
    """
    html = _render_html("quick_wins_memo.html", memo_data)
    pdf_bytes = _html_to_pdf(html)
    _save_pdf(pdf_bytes, output_path)
    return pdf_bytes


def render_findings_appendix_pdf(
    appendix_data: dict,
    output_path: Optional[str] = None,
) -> bytes:
    """Render the 5-8 page Findings Appendix PDF.

    Args:
        appendix_data: Dict expected to contain at minimum:
            - company_name (str)
            - assessment_date (str)
            - methodology_note (str)
            - dimension_details (list of 6 dicts, one per dimension)
            - sources_consulted (list of str)
        output_path: Optional filesystem path to write the PDF.

    Returns:
        Raw PDF bytes.
    """
    html = _render_html("findings_appendix.html", appendix_data)
    pdf_bytes = _html_to_pdf(html)
    _save_pdf(pdf_bytes, output_path)
    return pdf_bytes


def render_all_artifacts(d1_output: dict, radar_chart_b64: str) -> dict:
    """Render all three PDF artifacts from a complete D1/synthesis output dict.

    ``d1_output`` is expected to be the combined pipeline output containing
    scorecard_data, quick_wins_memo_data, and findings_appendix_data sub-keys,
    or a flat dict that can be decomposed by this function.

    Returns:
        {
            "scorecard_pdf": <bytes>,
            "quick_wins_pdf": <bytes>,
            "findings_pdf": <bytes>,
        }
    """
    # Support both nested and flat layouts
    scorecard_data = d1_output.get("scorecard_data") or d1_output
    memo_data = d1_output.get("quick_wins_memo_data") or d1_output
    appendix_data = d1_output.get("findings_appendix_data") or d1_output

    scorecard_pdf = render_scorecard_pdf(scorecard_data, radar_chart_b64)
    quick_wins_pdf = render_quick_wins_memo_pdf(memo_data)
    findings_pdf = render_findings_appendix_pdf(appendix_data)

    return {
        "scorecard_pdf": scorecard_pdf,
        "quick_wins_pdf": quick_wins_pdf,
        "findings_pdf": findings_pdf,
    }
