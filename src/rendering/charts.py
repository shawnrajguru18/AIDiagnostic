"""
Radar chart generator for the DXC AI Readiness Diagnostic.
Produces a hexagonal (6-axis) radar chart using matplotlib.
"""

import base64
import io
from typing import Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DIMENSION_LABELS = [
    "Data Foundation",
    "Governance Posture",
    "AI Investment\nMaturity",
    "Org Change\nReadiness",
    "Value-Pocket\nClarity",
    "Regulatory\nComplexity",
]

# Keys must match the DimensionId literals from schemas.py
DIMENSION_KEYS = [
    "data_foundation",
    "governance_posture",
    "ai_investment_maturity",
    "org_change_readiness",
    "value_pocket_clarity",
    "regulatory_complexity",
]

TIER_COLORS = {
    "Emerging": "#FFC982",
    "Developing": "#FFAE41",
    "Established": "#A1E6FF",
    "Leading": "#4995FF",
}

_BACKGROUND_COLOR = "#FFFFFF"
_GRID_COLOR = "#CCCCCC"
_LABEL_COLOR = "#0E1020"
_ANNOTATION_COLOR = "#3D3F50"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _scores_to_array(scores: dict) -> np.ndarray:
    """Extract ordered score array from a scores dict, defaulting missing keys to 0."""
    return np.array([float(scores.get(key, 0)) for key in DIMENSION_KEYS])


def _polar_to_xy(angles: np.ndarray, radii: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    x = radii * np.cos(angles)
    y = radii * np.sin(angles)
    return x, y


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def generate_radar_chart(
    scores: dict,
    overall_tier: str,
    peer_scores: Optional[dict] = None,
    output_format: str = "png",
) -> bytes:
    """Generate a hexagonal radar chart.

    Args:
        scores:        Dimension scores keyed by DimensionId string, values 0-100.
        overall_tier:  One of "Emerging", "Developing", "Established", "Leading".
        peer_scores:   Optional peer benchmark scores (same key format). Drawn as
                       a dashed outline for V0.5+.
        output_format: "png" or "svg".

    Returns:
        Raw bytes of the rendered chart image.
    """
    n = len(DIMENSION_KEYS)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    # Close the polygon
    angles_closed = np.append(angles, angles[0])

    tier_color = TIER_COLORS.get(overall_tier, TIER_COLORS["Developing"])

    fig = plt.figure(figsize=(6, 6), facecolor=_BACKGROUND_COLOR)
    ax = fig.add_subplot(111, polar=True)
    ax.set_facecolor(_BACKGROUND_COLOR)

    # ---- Grid rings at 25, 50, 75, 100 ----------------------------------------
    ring_levels = [25, 50, 75, 100]
    for ring in ring_levels:
        ring_vals = np.full(n + 1, ring / 100.0)
        ax.plot(
            angles_closed,
            ring_vals,
            color=_GRID_COLOR,
            linewidth=0.8,
            linestyle="-",
            zorder=1,
        )
        # Ring label at the top (angle = π/2)
        ax.text(
            np.pi / 2,
            ring / 100.0 + 0.03,
            str(ring),
            ha="center",
            va="center",
            fontsize=7,
            color=_GRID_COLOR,
            zorder=2,
        )

    # ---- Spoke lines (axes) -------------------------------------------------------
    for angle in angles:
        ax.plot(
            [angle, angle],
            [0, 1.0],
            color=_GRID_COLOR,
            linewidth=0.8,
            zorder=1,
        )

    # ---- Prospect polygon ---------------------------------------------------------
    values = _scores_to_array(scores) / 100.0
    values_closed = np.append(values, values[0])

    ax.fill(
        angles_closed,
        values_closed,
        color=tier_color,
        alpha=0.35,
        zorder=3,
    )
    ax.plot(
        angles_closed,
        values_closed,
        color=tier_color,
        linewidth=2.2,
        zorder=4,
    )

    # Score annotations at each vertex
    for i, (angle, val) in enumerate(zip(angles, values)):
        score_int = int(round(scores.get(DIMENSION_KEYS[i], 0)))
        # Offset radially outward a little
        r_ann = val + 0.07
        r_ann = min(r_ann, 1.13)
        ax.text(
            angle,
            r_ann,
            str(score_int),
            ha="center",
            va="center",
            fontsize=9,
            fontweight="bold",
            color=tier_color,
            zorder=6,
        )

    # ---- Peer scores (dashed outline) --------------------------------------------
    if peer_scores:
        peer_vals = _scores_to_array(peer_scores) / 100.0
        peer_vals_closed = np.append(peer_vals, peer_vals[0])
        ax.plot(
            angles_closed,
            peer_vals_closed,
            color="#888888",
            linewidth=1.4,
            linestyle="--",
            zorder=5,
            label="Peer average",
        )

    # ---- Axis labels -------------------------------------------------------------
    ax.set_xticks(angles)
    ax.set_xticklabels([])  # We draw our own

    label_padding = 1.28
    for i, (angle, label) in enumerate(zip(angles, DIMENSION_LABELS)):
        ha = "center"
        # Adjust horizontal alignment based on position
        x_component = np.cos(angle)
        if x_component > 0.3:
            ha = "left"
        elif x_component < -0.3:
            ha = "right"

        ax.text(
            angle,
            label_padding,
            label,
            ha=ha,
            va="center",
            fontsize=8.5,
            fontweight="semibold",
            color=_LABEL_COLOR,
            multialignment="center",
            zorder=7,
        )

    # ---- Cosmetics ---------------------------------------------------------------
    ax.set_ylim(0, 1.0)
    ax.set_yticks([])
    ax.spines["polar"].set_visible(False)

    # Origin dot
    ax.plot(0, 0, "o", color=tier_color, markersize=4, zorder=8)

    plt.tight_layout(pad=0.5)

    buf = io.BytesIO()
    fmt = output_format.lower()
    if fmt == "svg":
        fig.savefig(buf, format="svg", bbox_inches="tight", facecolor=_BACKGROUND_COLOR)
    else:
        fig.savefig(
            buf,
            format="png",
            dpi=150,
            bbox_inches="tight",
            facecolor=_BACKGROUND_COLOR,
        )
    plt.close(fig)
    buf.seek(0)
    return buf.read()


def get_radar_chart_base64(scores: dict, overall_tier: str) -> str:
    """Return a base64-encoded PNG string suitable for embedding in HTML.

    The returned string is prefixed with the data-URI scheme so it can be
    dropped directly into an <img src="..."> attribute.
    """
    png_bytes = generate_radar_chart(scores, overall_tier, output_format="png")
    b64 = base64.b64encode(png_bytes).decode("utf-8")
    return f"data:image/png;base64,{b64}"
