#!/usr/bin/env python3
"""
Run the DXC AI Readiness Diagnostic demo scenarios.

Usage:
    python run_demo.py [scenario]

    scenario: meridian_fs | northern_care | aurelian_tech (default: meridian_fs)

The script runs the full lightweight diagnostic pipeline on the selected
demo fixture and prints a structured JSON summary to stdout.

For investor-day demos: the output includes overall score, tier, dimension
breakdown, top 3 findings, recommended next step, and quick wins.
"""

from __future__ import annotations

import asyncio
import json
import sys
from datetime import datetime
from typing import Any, Dict


VALID_SCENARIOS = ("meridian_fs", "northern_care", "aurelian_tech")


def _print_usage():
    print(
        "Usage: python run_demo.py [scenario]\n"
        f"  scenario: {' | '.join(VALID_SCENARIOS)} (default: meridian_fs)\n"
    )


def _pretty_print_result(result: Dict[str, Any]) -> None:
    """Print a human-readable summary of the diagnostic result."""
    print("\n" + "=" * 70)
    print("  DXC AI READINESS DIAGNOSTIC — RESULTS")
    print("=" * 70)
    print(f"  Company:      {result.get('company_name', 'Unknown')}")
    print(f"  Scenario:     {result.get('scenario', 'N/A')}")
    print(f"  Generated:    {result.get('assessment_date', datetime.utcnow().strftime('%B %d, %Y'))}")
    print()
    print(f"  OVERALL SCORE:  {result.get('overall_score', 0)} / 100")
    print(f"  TIER:           {result.get('overall_tier', 'Unknown')}")
    print()

    # Dimension breakdown
    dim_scores = result.get("dimension_scores", {})
    if dim_scores:
        print("  DIMENSION SCORES:")
        dim_names = {
            "data_foundation": "Data Foundation",
            "governance_posture": "Governance Posture",
            "ai_investment_maturity": "AI Investment Maturity",
            "org_change_readiness": "Org Change Readiness",
            "value_pocket_clarity": "Value-Pocket Clarity",
            "regulatory_complexity": "Regulatory Complexity",
        }
        for dim_id, score in dim_scores.items():
            label = dim_names.get(dim_id, dim_id)
            bar = "█" * int(score / 5) + "░" * (20 - int(score / 5))
            print(f"    {label:<30} {score:>3}  [{bar}]")

    print()

    # Findings
    findings = result.get("findings", [])
    if findings:
        print("  KEY FINDINGS:")
        for i, finding in enumerate(findings[:4], 1):
            headline = finding.get("headline", finding.get("narrative", ""))
            print(f"    {i}. {headline}")

    print()

    # Recommended next step
    next_step = result.get("recommended_next_step", {})
    if next_step:
        print("  RECOMMENDED NEXT STEP:")
        print(f"    {next_step.get('title', '')}")
        desc = next_step.get("description", "")
        if desc:
            # Wrap at 65 chars
            words = desc.split()
            line = "    "
            for word in words:
                if len(line) + len(word) > 68:
                    print(line)
                    line = "    " + word + " "
                else:
                    line += word + " "
            if line.strip():
                print(line)

    print()

    # Quick wins
    quick_wins = result.get("quick_wins", [])
    if quick_wins:
        print("  90-DAY QUICK WINS:")
        for qw in quick_wins[:3]:
            name = qw.get("name", "")
            weeks = qw.get("timeline_weeks", "?")
            print(f"    • {name} ({weeks}w)")

    print()
    print("=" * 70)
    print()


async def run_lightweight_demo(scenario: str) -> Dict[str, Any]:
    """Run the demo using the scoring engine directly (no LLM calls required).

    This is the lightweight path for demos without API keys. It uses the
    fixture questionnaire responses and the deterministic scoring engine
    to produce a complete structured output.
    """
    from src.orchestrator.scoring import (
        compute_all_scores,
        get_tier_colour,
        DIMENSION_DISPLAY_NAMES,
    )
    from src.data.quick_wins import get_quick_wins_for_prospect, QUICK_WIN_PATTERNS
    from src.rendering.charts import get_radar_chart_base64

    fixture_map = {
        "meridian_fs": ("src.data.fixtures.meridian_fs", "MERIDIAN_FS_FIXTURE"),
        "northern_care": ("src.data.fixtures.northern_care", "NORTHERN_CARE_FIXTURE"),
        "aurelian_tech": ("src.data.fixtures.aurelian_tech", "AURELIAN_TECH_FIXTURE"),
    }

    module_name, fixture_name = fixture_map[scenario]
    module = __import__(module_name, fromlist=[fixture_name])
    fixture = getattr(module, fixture_name)

    prospect = fixture["prospect"]
    responses = fixture["responses"]
    company_name = prospect["company_name"]
    industry = prospect.get("industry", "Other")
    size_band = prospect.get("size_band", "Large")

    # Compute scores
    scoring = compute_all_scores(responses)
    dim_scores = scoring["dimension_scores"]
    overall_score = scoring["overall_score"]
    overall_tier = scoring["overall_tier"]
    dim_tiers = scoring["dimension_tiers"]

    # Build dimension list
    dim_list = [
        {
            "name": DIMENSION_DISPLAY_NAMES.get(dim_id, dim_id),
            "score": round(score),
            "tier": dim_tiers.get(dim_id, "Developing"),
            "tier_color": get_tier_colour(dim_tiers.get(dim_id, "Developing"))["hex"],
            "dimension_id": dim_id,
        }
        for dim_id, score in dim_scores.items()
    ]

    # Generate findings (deterministic, no LLM)
    findings = []
    sorted_dims = sorted(dim_scores.items(), key=lambda x: x[1])
    for dim_id, score in sorted_dims[:4]:
        tier = dim_tiers.get(dim_id, "Developing")
        findings.append({
            "dimension_id": dim_id,
            "headline": (
                f"{DIMENSION_DISPLAY_NAMES.get(dim_id, dim_id)} — "
                f"scored {score:.0f} ({tier}): "
                + ("requires focused investment to accelerate." if score < 60 else "strong foundation for AI deployment.")
            ),
            "finding_type": "gap" if score < 60 else "strength",
        })

    # Select quick wins
    candidates = get_quick_wins_for_prospect(industry, size_band)
    if not candidates:
        candidates = [p for p in QUICK_WIN_PATTERNS if "All" in p.get("applicable_industries", [])]

    def _candidate_score(p):
        effort = {"low": 3, "medium": 2, "high": 1}.get(p.get("implementation_effort", "medium"), 2)
        timeline = max(0, (16 - p.get("timeline_to_value_weeks", 12)) / 16 * 3)
        return effort + timeline

    quick_wins = sorted(candidates, key=_candidate_score, reverse=True)[:3]
    qw_out = [
        {
            "pattern_id": qw["pattern_id"],
            "name": qw["name"],
            "one_line_description": qw["one_line_description"],
            "rank": i + 1,
            "timeline_weeks": qw.get("timeline_to_value_weeks", 12),
            "implementation_effort": qw.get("implementation_effort", "medium"),
            "prerequisites": qw.get("prerequisites", [])[:3],
            "expected_outcomes": qw.get("expected_outcomes", [])[:2],
        }
        for i, qw in enumerate(quick_wins)
    ]

    # Next step
    if overall_tier == "Emerging":
        next_step = {
            "title": "Data Foundation Readiness Assessment",
            "description": "A focused 30-day engagement to map the data estate and produce a prioritised readiness roadmap.",
        }
    elif overall_tier == "Developing":
        next_step = {
            "title": "AI Potential Review (APR) Discovery Session",
            "description": "A two-day structured engagement to validate findings, map priority value pockets, and build a 90-day roadmap.",
        }
    elif overall_tier == "Established":
        next_step = {
            "title": "AI Scale-Up Roadmap Workshop",
            "description": "A two-day executive workshop to identify the next AI value pockets and define the path from Established to Leading.",
        }
    else:
        next_step = {
            "title": "AI Leadership Partnership Engagement",
            "description": "An executive briefing and co-innovation workshop on frontier AI capabilities.",
        }

    # Radar chart
    print(f"  Generating radar chart for {company_name}...")
    radar_b64 = get_radar_chart_base64(dim_scores, overall_tier)

    assessment_date = datetime.utcnow().strftime("%B %d, %Y")

    return {
        "scenario": scenario,
        "company_name": company_name,
        "assessment_date": assessment_date,
        "overall_score": round(overall_score),
        "overall_tier": overall_tier,
        "tier_color": get_tier_colour(overall_tier)["hex"],
        "dimension_scores": {k: round(v) for k, v in dim_scores.items()},
        "dimension_tiers": dim_tiers,
        "dimension_list": dim_list,
        "findings": findings,
        "quick_wins": qw_out,
        "recommended_next_step": next_step,
        "radar_chart_b64_preview": radar_b64[:80] + "...[truncated]",
        "radar_chart_size_bytes": len(radar_b64),
        "generated_at": datetime.utcnow().isoformat(),
        "pipeline_mode": "lightweight_scoring_only",
        "note": "Lightweight demo — no LLM API calls. Run with ANTHROPIC_API_KEY for full AI-generated content.",
    }


async def main() -> None:
    # Parse scenario argument
    scenario = sys.argv[1].lower() if len(sys.argv) > 1 else "meridian_fs"

    if scenario in ("--help", "-h", "help"):
        _print_usage()
        sys.exit(0)

    if scenario not in VALID_SCENARIOS:
        print(f"Error: Unknown scenario {scenario!r}")
        _print_usage()
        sys.exit(1)

    print(f"\n  DXC AI Readiness Diagnostic — Demo Runner")
    print(f"  Running scenario: {scenario}")
    print(f"  Mode: lightweight (scoring engine only, no LLM calls)\n")

    try:
        result = await run_lightweight_demo(scenario)
        _pretty_print_result(result)

        # Also write clean JSON output
        output_path = f"/tmp/diagnostic_demo_{scenario}.json"
        safe_result = {k: v for k, v in result.items() if k != "radar_chart_b64_preview"}
        with open(output_path, "w") as f:
            json.dump(safe_result, f, indent=2, default=str)
        print(f"  Full JSON output written to: {output_path}")

    except Exception as exc:
        print(f"Error running demo scenario {scenario!r}: {exc}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
