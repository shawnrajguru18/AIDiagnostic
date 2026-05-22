"""
Integration tests for the DXC AI Readiness Diagnostic V0.

Covers:
  - Scoring engine: tier thresholds, dimension scoring, overall scoring
  - Three demo scenario fixtures: MeridianFS, NorthernCare, AurelianTech
  - Radar chart generation
  - Quick wins library: 15-pattern count and Financial Services selection
"""

from __future__ import annotations

import base64
from typing import Any, Dict

import pytest

from src.orchestrator.scoring import compute_all_scores, get_tier
from src.data.fixtures.meridian_fs import MERIDIAN_FS_FIXTURE
from src.data.fixtures.northern_care import NORTHERN_CARE_FIXTURE
from src.data.fixtures.aurelian_tech import AURELIAN_TECH_FIXTURE


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _score_fixture(fixture: Dict[str, Any]) -> Dict[str, Any]:
    """Compute scores for a fixture's questionnaire responses."""
    return compute_all_scores(fixture["responses"])


# ===========================================================================
# TestScoringEngine
# ===========================================================================


class TestScoringEngine:
    """Tests for the scoring engine using the three demo scenario fixtures."""

    # -----------------------------------------------------------------------
    # MeridianFS — Financial Services, Large, ~52 Developing
    # -----------------------------------------------------------------------

    def test_meridian_fs_scores(self):
        """MeridianFS overall score should be ~52 (±5 tolerance) — Developing."""
        result = _score_fixture(MERIDIAN_FS_FIXTURE)

        overall = result["overall_score"]
        tier = result["overall_tier"]
        expected = MERIDIAN_FS_FIXTURE["expected"]

        lo, hi = expected["overall_score_range"]
        assert lo <= overall <= hi, (
            f"MeridianFS overall score {overall} outside expected range [{lo}, {hi}]"
        )
        assert tier == expected["overall_tier"], (
            f"MeridianFS tier {tier!r} != expected {expected['overall_tier']!r}"
        )

    def test_meridian_fs_dimension_scores(self):
        """MeridianFS dimension scores should each be within ±8 of expected mid-point."""
        result = _score_fixture(MERIDIAN_FS_FIXTURE)
        dim_scores = result["dimension_scores"]
        expected = MERIDIAN_FS_FIXTURE["expected"]["dimension_expected"]

        for dim_id, (lo, hi) in expected.items():
            score = dim_scores.get(dim_id, 0)
            assert lo <= score <= hi, (
                f"MeridianFS {dim_id}: score {score:.1f} outside expected range [{lo}, {hi}]"
            )

    # -----------------------------------------------------------------------
    # NorthernCare — Healthcare, Mid-Market, ~38 Emerging
    # -----------------------------------------------------------------------

    def test_northern_care_scores(self):
        """NorthernCare overall score should be ~38 (±5 tolerance) — Emerging."""
        result = _score_fixture(NORTHERN_CARE_FIXTURE)

        overall = result["overall_score"]
        tier = result["overall_tier"]
        expected = NORTHERN_CARE_FIXTURE["expected"]

        lo, hi = expected["overall_score_range"]
        assert lo <= overall <= hi, (
            f"NorthernCare overall score {overall} outside expected range [{lo}, {hi}]"
        )
        assert tier == expected["overall_tier"], (
            f"NorthernCare tier {tier!r} != expected {expected['overall_tier']!r}"
        )

    def test_northern_care_dimension_scores(self):
        """NorthernCare dimension scores should each be within expected range."""
        result = _score_fixture(NORTHERN_CARE_FIXTURE)
        dim_scores = result["dimension_scores"]
        expected = NORTHERN_CARE_FIXTURE["expected"]["dimension_expected"]

        for dim_id, (lo, hi) in expected.items():
            score = dim_scores.get(dim_id, 0)
            assert lo <= score <= hi, (
                f"NorthernCare {dim_id}: score {score:.1f} outside expected range [{lo}, {hi}]"
            )

    # -----------------------------------------------------------------------
    # AurelianTech — Technology, Enterprise, ~68 Established
    # -----------------------------------------------------------------------

    def test_aurelian_tech_scores(self):
        """AurelianTech overall score should be ~68 (±5 tolerance) — Established."""
        result = _score_fixture(AURELIAN_TECH_FIXTURE)

        overall = result["overall_score"]
        tier = result["overall_tier"]
        expected = AURELIAN_TECH_FIXTURE["expected"]

        lo, hi = expected["overall_score_range"]
        assert lo <= overall <= hi, (
            f"AurelianTech overall score {overall} outside expected range [{lo}, {hi}]"
        )
        assert tier == expected["overall_tier"], (
            f"AurelianTech tier {tier!r} != expected {expected['overall_tier']!r}"
        )

    def test_aurelian_tech_dimension_scores(self):
        """AurelianTech dimension scores should each be within expected range."""
        result = _score_fixture(AURELIAN_TECH_FIXTURE)
        dim_scores = result["dimension_scores"]
        expected = AURELIAN_TECH_FIXTURE["expected"]["dimension_expected"]

        for dim_id, (lo, hi) in expected.items():
            score = dim_scores.get(dim_id, 0)
            assert lo <= score <= hi, (
                f"AurelianTech {dim_id}: score {score:.1f} outside expected range [{lo}, {hi}]"
            )

    # -----------------------------------------------------------------------
    # Tier threshold validation (boundary tests)
    # -----------------------------------------------------------------------

    def test_tier_thresholds(self):
        """Tier boundary conditions must be exactly correct per the spec."""
        # Emerging: 0-39
        assert get_tier(0) == "Emerging", "Score 0 must be Emerging"
        assert get_tier(1) == "Emerging"
        assert get_tier(39) == "Emerging", "Score 39 must be Emerging (upper boundary)"
        assert get_tier(39.9) == "Emerging"

        # Developing: 40-59
        assert get_tier(40) == "Developing", "Score 40 must be Developing"
        assert get_tier(40.0) == "Developing"
        assert get_tier(50) == "Developing"
        assert get_tier(59) == "Developing", "Score 59 must be Developing"
        assert get_tier(59.9) == "Developing"

        # Established: 60-79
        assert get_tier(60) == "Established", "Score 60 must be Established"
        assert get_tier(70) == "Established"
        assert get_tier(79) == "Established", "Score 79 must be Established"
        assert get_tier(79.9) == "Established"

        # Leading: 80-100
        assert get_tier(80) == "Leading", "Score 80 must be Leading"
        assert get_tier(90) == "Leading"
        assert get_tier(100) == "Leading", "Score 100 must be Leading"

    def test_tier_returns_string(self):
        """get_tier must always return a string."""
        for score in [0, 25, 39, 40, 55, 59, 60, 75, 79, 80, 95, 100]:
            result = get_tier(score)
            assert isinstance(result, str), f"get_tier({score}) returned {type(result)}"

    def test_compute_all_scores_returns_all_six_dimensions(self):
        """compute_all_scores must return all six dimension keys."""
        expected_dims = {
            "data_foundation",
            "governance_posture",
            "ai_investment_maturity",
            "org_change_readiness",
            "value_pocket_clarity",
            "regulatory_complexity",
        }
        result = compute_all_scores(MERIDIAN_FS_FIXTURE["responses"])
        assert set(result["dimension_scores"].keys()) == expected_dims

    def test_compute_all_scores_scores_in_range(self):
        """All computed scores must be in the 0-100 range."""
        for fixture in [MERIDIAN_FS_FIXTURE, NORTHERN_CARE_FIXTURE, AURELIAN_TECH_FIXTURE]:
            result = compute_all_scores(fixture["responses"])
            assert 0 <= result["overall_score"] <= 100, (
                f"Overall score {result['overall_score']} out of range"
            )
            for dim_id, score in result["dimension_scores"].items():
                assert 0 <= score <= 100, (
                    f"{dim_id} score {score:.1f} out of range [0, 100]"
                )

    def test_empty_responses_produces_zero_scores(self):
        """An empty response list must produce 0.0 for all dimensions."""
        result = compute_all_scores([])
        assert result["overall_score"] == 0.0 or result["overall_score"] == pytest.approx(0.0, abs=0.1)
        for score in result["dimension_scores"].values():
            assert score == pytest.approx(0.0, abs=0.1)

    def test_overall_score_within_dimension_range(self):
        """Overall score must be between the min and max of dimension scores."""
        for fixture in [MERIDIAN_FS_FIXTURE, NORTHERN_CARE_FIXTURE, AURELIAN_TECH_FIXTURE]:
            result = compute_all_scores(fixture["responses"])
            dim_scores = list(result["dimension_scores"].values())
            if not dim_scores:
                continue
            min_dim = min(dim_scores)
            max_dim = max(dim_scores)
            overall = result["overall_score"]
            # Overall must be a weighted average — between min and max (with tolerance)
            assert min_dim - 1 <= overall <= max_dim + 1, (
                f"Overall score {overall} not in range [{min_dim:.1f}, {max_dim:.1f}]"
            )


# ===========================================================================
# TestRadarChart
# ===========================================================================


class TestRadarChart:
    """Tests for the radar chart rendering module."""

    def test_chart_generation_returns_bytes(self):
        """generate_radar_chart must return bytes."""
        from src.rendering.charts import generate_radar_chart

        scores = {
            "data_foundation": 52,
            "governance_posture": 62,
            "ai_investment_maturity": 48,
            "org_change_readiness": 55,
            "value_pocket_clarity": 68,
            "regulatory_complexity": 44,
        }
        result = generate_radar_chart(scores, "Developing")
        assert isinstance(result, bytes), f"Expected bytes, got {type(result)}"
        assert len(result) > 100, "Chart bytes should be non-trivial in size"

    def test_chart_generation_png_format(self):
        """Default output format should produce PNG bytes (starts with PNG magic bytes)."""
        from src.rendering.charts import generate_radar_chart

        scores = {
            "data_foundation": 72,
            "governance_posture": 70,
            "ai_investment_maturity": 75,
            "org_change_readiness": 65,
            "value_pocket_clarity": 73,
            "regulatory_complexity": 58,
        }
        result = generate_radar_chart(scores, "Established", output_format="png")
        # PNG magic bytes: 0x89 0x50 0x4E 0x47
        assert result[:4] == b"\x89PNG", "PNG output must start with PNG magic bytes"

    def test_chart_generation_all_tiers(self):
        """generate_radar_chart must work for all four tier values."""
        from src.rendering.charts import generate_radar_chart

        scores = {dim: 50 for dim in [
            "data_foundation", "governance_posture", "ai_investment_maturity",
            "org_change_readiness", "value_pocket_clarity", "regulatory_complexity"
        ]}

        for tier in ["Emerging", "Developing", "Established", "Leading"]:
            result = generate_radar_chart(scores, tier)
            assert isinstance(result, bytes) and len(result) > 0, (
                f"Chart generation failed for tier {tier!r}"
            )

    def test_get_radar_chart_base64_returns_data_uri(self):
        """get_radar_chart_base64 must return a valid data-URI string."""
        from src.rendering.charts import get_radar_chart_base64

        scores = {
            "data_foundation": 40,
            "governance_posture": 38,
            "ai_investment_maturity": 30,
            "org_change_readiness": 44,
            "value_pocket_clarity": 55,
            "regulatory_complexity": 42,
        }
        result = get_radar_chart_base64(scores, "Emerging")
        assert isinstance(result, str)
        assert result.startswith("data:image/png;base64,"), (
            f"Expected data URI prefix, got: {result[:50]}"
        )
        # Validate the base64 payload is decodable
        b64_payload = result.split(",", 1)[1]
        decoded = base64.b64decode(b64_payload)
        assert len(decoded) > 100, "Decoded chart payload must be non-trivial"

    def test_chart_with_peer_scores(self):
        """generate_radar_chart with peer_scores must return bytes without error."""
        from src.rendering.charts import generate_radar_chart

        scores = {
            "data_foundation": 60,
            "governance_posture": 65,
            "ai_investment_maturity": 55,
            "org_change_readiness": 70,
            "value_pocket_clarity": 68,
            "regulatory_complexity": 50,
        }
        peer_scores = {k: v + 5 for k, v in scores.items()}
        result = generate_radar_chart(scores, "Established", peer_scores=peer_scores)
        assert isinstance(result, bytes) and len(result) > 0

    def test_chart_with_missing_dimension_scores(self):
        """generate_radar_chart must handle missing dimension keys gracefully (default to 0)."""
        from src.rendering.charts import generate_radar_chart

        # Only provide 3 of 6 dimensions
        partial_scores = {
            "data_foundation": 50,
            "governance_posture": 60,
            "ai_investment_maturity": 45,
        }
        result = generate_radar_chart(partial_scores, "Developing")
        assert isinstance(result, bytes) and len(result) > 0


# ===========================================================================
# TestQuickWinsLibrary
# ===========================================================================


class TestQuickWinsLibrary:
    """Tests for the Quick Wins pattern library."""

    def test_library_has_15_patterns(self):
        """The quick wins library must contain exactly 15 patterns."""
        from src.data.quick_wins import QUICK_WIN_PATTERNS

        assert len(QUICK_WIN_PATTERNS) == 15, (
            f"Expected 15 quick win patterns, found {len(QUICK_WIN_PATTERNS)}"
        )

    def test_all_patterns_have_required_fields(self):
        """Every quick win pattern must have all required fields."""
        from src.data.quick_wins import QUICK_WIN_PATTERNS

        required_fields = [
            "pattern_id",
            "name",
            "one_line_description",
            "prerequisites",
            "expected_outcomes",
            "implementation_effort",
            "timeline_to_value_weeks",
            "applicable_industries",
            "applicable_sizes",
            "disqualifying_conditions",
        ]

        for pattern in QUICK_WIN_PATTERNS:
            pid = pattern.get("pattern_id", "UNKNOWN")
            for field in required_fields:
                assert field in pattern, (
                    f"Pattern {pid} is missing required field {field!r}"
                )
                assert pattern[field] is not None, (
                    f"Pattern {pid} field {field!r} must not be None"
                )

    def test_pattern_ids_are_unique(self):
        """All pattern_ids in the library must be unique."""
        from src.data.quick_wins import QUICK_WIN_PATTERNS

        ids = [p["pattern_id"] for p in QUICK_WIN_PATTERNS]
        assert len(ids) == len(set(ids)), (
            f"Duplicate pattern_ids detected: {[x for x in ids if ids.count(x) > 1]}"
        )

    def test_pattern_qw_001_exists(self):
        """QW-001 must exist in the library (required by MeridianFS fixture)."""
        from src.data.quick_wins import QUICK_WIN_PATTERNS

        ids = {p["pattern_id"] for p in QUICK_WIN_PATTERNS}
        assert "QW-001" in ids, "Pattern QW-001 must exist in the library"

    def test_pattern_qw_005_exists(self):
        """QW-005 must exist in the library (required by MeridianFS fixture)."""
        from src.data.quick_wins import QUICK_WIN_PATTERNS

        ids = {p["pattern_id"] for p in QUICK_WIN_PATTERNS}
        assert "QW-005" in ids, "Pattern QW-005 must exist in the library"

    def test_pattern_qw_012_exists(self):
        """QW-012 must exist in the library (required by MeridianFS fixture)."""
        from src.data.quick_wins import QUICK_WIN_PATTERNS

        ids = {p["pattern_id"] for p in QUICK_WIN_PATTERNS}
        assert "QW-012" in ids, "Pattern QW-012 must exist in the library"

    def test_meridian_fs_quick_wins_selection(self):
        """QW-001, QW-005, and QW-012 must appear in candidates for FS Large Enterprise.

        MeridianFS is a Financial Services, Large prospect. All three patterns
        are expected to be eligible candidates (even if not ranked 1-2-3 by the
        automated selector — their eligibility is what this test verifies).
        """
        from src.data.quick_wins import get_quick_wins_for_prospect

        # get_quick_wins_for_prospect filters by industry and size band
        candidates = get_quick_wins_for_prospect("Financial Services", "Large")
        candidate_ids = {c["pattern_id"] for c in candidates}

        # QW-001, QW-005, and QW-012 should all qualify for FS Large
        for pid in ["QW-001", "QW-005", "QW-012"]:
            assert pid in candidate_ids, (
                f"Pattern {pid} not in quick win candidates for Financial Services / Large. "
                f"Candidates: {sorted(candidate_ids)}"
            )

    def test_implementation_effort_values(self):
        """All implementation_effort values must be 'low', 'medium', or 'high'."""
        from src.data.quick_wins import QUICK_WIN_PATTERNS

        valid = {"low", "medium", "high"}
        for pattern in QUICK_WIN_PATTERNS:
            effort = pattern.get("implementation_effort")
            assert effort in valid, (
                f"Pattern {pattern['pattern_id']}: invalid implementation_effort {effort!r}"
            )

    def test_timeline_to_value_is_positive_int(self):
        """All timeline_to_value_weeks values must be positive integers."""
        from src.data.quick_wins import QUICK_WIN_PATTERNS

        for pattern in QUICK_WIN_PATTERNS:
            weeks = pattern.get("timeline_to_value_weeks")
            assert isinstance(weeks, int) and weeks > 0, (
                f"Pattern {pattern['pattern_id']}: invalid timeline_to_value_weeks {weeks!r}"
            )

    def test_get_quick_wins_for_prospect_filters_correctly(self):
        """get_quick_wins_for_prospect must not return industry-specific patterns for wrong industry."""
        from src.data.quick_wins import get_quick_wins_for_prospect, QUICK_WIN_PATTERNS

        # Get Healthcare patterns for a Financial Services prospect
        fs_candidates = get_quick_wins_for_prospect("Financial Services", "Large")
        fs_ids = {c["pattern_id"] for c in fs_candidates}

        # Healthcare-specific patterns should not appear for Financial Services
        hls_only = [
            p for p in QUICK_WIN_PATTERNS
            if p["applicable_industries"] == ["Healthcare & Life Sciences"]
        ]
        for pattern in hls_only:
            assert pattern["pattern_id"] not in fs_ids, (
                f"Healthcare-only pattern {pattern['pattern_id']} incorrectly included "
                f"in Financial Services candidates"
            )


# ===========================================================================
# TestFixtureIntegrity
# ===========================================================================


class TestFixtureIntegrity:
    """Validates the structure and consistency of demo fixture data."""

    def test_all_fixtures_have_required_keys(self):
        """Each fixture must have 'prospect', 'responses', and 'expected' keys."""
        for name, fixture in [
            ("meridian_fs", MERIDIAN_FS_FIXTURE),
            ("northern_care", NORTHERN_CARE_FIXTURE),
            ("aurelian_tech", AURELIAN_TECH_FIXTURE),
        ]:
            assert "prospect" in fixture, f"{name}: missing 'prospect' key"
            assert "responses" in fixture, f"{name}: missing 'responses' key"
            assert "expected" in fixture, f"{name}: missing 'expected' key"

    def test_fixtures_have_non_empty_responses(self):
        """Each fixture must have at least 10 questionnaire responses."""
        for name, fixture in [
            ("meridian_fs", MERIDIAN_FS_FIXTURE),
            ("northern_care", NORTHERN_CARE_FIXTURE),
            ("aurelian_tech", AURELIAN_TECH_FIXTURE),
        ]:
            responses = fixture["responses"]
            assert len(responses) >= 10, (
                f"{name}: expected >= 10 responses, found {len(responses)}"
            )

    def test_fixture_responses_have_question_ids(self):
        """All responses in every fixture must have a question_id field."""
        for name, fixture in [
            ("meridian_fs", MERIDIAN_FS_FIXTURE),
            ("northern_care", NORTHERN_CARE_FIXTURE),
            ("aurelian_tech", AURELIAN_TECH_FIXTURE),
        ]:
            for i, response in enumerate(fixture["responses"]):
                assert "question_id" in response, (
                    f"{name} response[{i}] missing 'question_id'"
                )

    def test_fixture_responses_cover_all_six_dimensions(self):
        """Each fixture must cover all six diagnostic dimensions."""
        expected_dims = {
            "data_foundation",
            "governance_posture",
            "ai_investment_maturity",
            "org_change_readiness",
            "value_pocket_clarity",
            "regulatory_complexity",
        }
        for name, fixture in [
            ("meridian_fs", MERIDIAN_FS_FIXTURE),
            ("northern_care", NORTHERN_CARE_FIXTURE),
            ("aurelian_tech", AURELIAN_TECH_FIXTURE),
        ]:
            covered = {r["dimension_id"] for r in fixture["responses"] if "dimension_id" in r}
            assert covered == expected_dims, (
                f"{name}: missing dimensions {expected_dims - covered}"
            )

    def test_fixture_expected_tiers_are_valid(self):
        """Expected tiers in fixture 'expected' dicts must be valid tier names."""
        valid_tiers = {"Emerging", "Developing", "Established", "Leading"}
        for name, fixture in [
            ("meridian_fs", MERIDIAN_FS_FIXTURE),
            ("northern_care", NORTHERN_CARE_FIXTURE),
            ("aurelian_tech", AURELIAN_TECH_FIXTURE),
        ]:
            tier = fixture["expected"].get("overall_tier")
            assert tier in valid_tiers, (
                f"{name}: invalid expected tier {tier!r}"
            )

    def test_scenarios_have_different_tiers(self):
        """The three demo scenarios should span at least two different tiers."""
        tiers = set()
        for fixture in [MERIDIAN_FS_FIXTURE, NORTHERN_CARE_FIXTURE, AURELIAN_TECH_FIXTURE]:
            tiers.add(fixture["expected"]["overall_tier"])
        assert len(tiers) >= 2, (
            f"Expected at least 2 different tiers across demo scenarios, got: {tiers}"
        )
