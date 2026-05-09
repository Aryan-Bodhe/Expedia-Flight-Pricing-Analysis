"""
views.py
--------
Provides per-layer figure builders consumed by the Dash app in main.py.
"""

from __future__ import annotations

import plotly.graph_objects as go

from map.layers import (
    plot_all_routes,
    plot_all_airports,
    plot_top_k_airports,
    plot_top_k_routes,
    plot_top_k_airline_airports,
    plot_haul_routes,
    plot_top_k_layover_airports,
    plot_fare_vs_avg_routes,
    plot_cabin_routes,
    _HAUL_BUCKETS,
    _FARE_TIER_LABELS,
    CABIN_OPTIONS,
)

# ---------------------------------------------------------------------------
# Layer metadata — consumed by main.py to build the sidebar
# Each entry: (layer_id, display_label, uses_k, uses_airline, uses_haul, uses_fare_tier)
# ---------------------------------------------------------------------------

# Each tuple: (layer_id, display_label, uses_k, uses_airline, uses_haul, uses_fare_tier, uses_cabin)
LAYER_META: list[tuple[str, str, bool, bool, bool, bool, bool]] = [
    ("all_routes",       "All Routes",       False, False, False, False, False),
    ("top_hubs",         "Top Hubs",         True,  False, False, False, False),
    ("top_routes",       "Top Routes",       True,  False, False, False, False),
    ("airline_airports", "Airline Airports", True,  True,  False, False, False),
    ("haul_routes",      "Haul Types",       False, False, True,  False, False),
    ("layover_hubs",     "Layover Hubs",     True,  False, False, False, False),
    ("fare_vs_avg",      "Fare vs Average",  False, False, False, True,  False),
    ("cabin_routes",     "Cabin Class",      True,  False, False, False, True),
]

# Exported option lists for sidebar dropdowns
HAUL_OPTIONS      = [label for label, _, _, _ in _HAUL_BUCKETS]
FARE_TIER_OPTIONS = _FARE_TIER_LABELS
# Re-export so main.py only imports from views
CABIN_OPTIONS     = CABIN_OPTIONS


# ---------------------------------------------------------------------------
# Shared geo layout applied to every figure
# ---------------------------------------------------------------------------

def _apply_geo_layout(fig: go.Figure, title: str) -> None:
    fig.update_layout(
        template="plotly_dark",
        title=dict(text=title, x=0.5, font=dict(size=16, color="white")),
        geo=dict(
            scope="usa",
            showland=True,
            landcolor="#1a1a1a",
            showlakes=True,
            lakecolor="#0d1b2a",
            showcoastlines=True,
            coastlinecolor="rgba(255,255,255,0.2)",
            showframe=False,
        ),
        showlegend=True,
        legend=dict(
            x=1.0, y=1.0,
            bgcolor="rgba(0,0,0,0.6)",
            font=dict(color="white", size=11),
        ),
        margin=dict(t=50, b=0, l=0, r=0),
        paper_bgcolor="#111",
        plot_bgcolor="#111",
        autosize=True,
    )


# ---------------------------------------------------------------------------
# Per-layer figure builder
# ---------------------------------------------------------------------------

def build_layer_fig(
    layer_id: str,
    df,
    airports,
    routes,
    lats,
    lons,
    *,
    k: int = 10,
    airline: str = "Delta",
    haul_filter: str | None = None,
    fare_tier_filter: int | None = None,
    cabin_filter: str | None = None,
    title: str = "US Flight Network",
) -> go.Figure:
    """
    Build and return a figure. Routes are always added first (lower z-order)
    so airports render on top in dense areas.
    """
    fig = go.Figure()

    if layer_id == "all_routes":
        plot_all_routes(fig, lats, lons)                   # routes first
        plot_all_airports(fig, airports)                    # airports on top
        _apply_geo_layout(fig, f"{title} — All Routes")

    elif layer_id == "top_hubs":
        plot_all_airports(fig, airports)
        plot_top_k_airports(fig, airports, k)              # hubs drawn above base airports
        _apply_geo_layout(fig, f"{title} — Top {k} Hubs")

    elif layer_id == "top_routes":
        # Only the highlighted top-k routes — no "all routes" underneath
        plot_top_k_routes(fig, df, airports, k)            # routes first
        plot_all_airports(fig, airports)                    # airports on top
        _apply_geo_layout(fig, f"{title} — Top {k} Routes")

    elif layer_id == "airline_airports":
        plot_all_airports(fig, airports)                             # base airports first
        plot_top_k_airline_airports(fig, df, airports, airline, k)  # airline markers on top
        _apply_geo_layout(fig, f"{title} — {airline}: Top {k} Airports")

    elif layer_id == "haul_routes":
        haul_label = haul_filter or "All"
        plot_haul_routes(fig, df, airports, haul_filter=haul_filter)  # routes first
        plot_all_airports(fig, airports)                               # airports on top
        _apply_geo_layout(fig, f"{title} — Haul Types ({haul_label})")

    elif layer_id == "layover_hubs":
        plot_all_airports(fig, airports)                    # base airports first
        plot_top_k_layover_airports(fig, df, airports, k)  # layover hubs on top
        _apply_geo_layout(fig, f"{title} — Top {k} Layover Airports")

    elif layer_id == "fare_vs_avg":
        tier_label = _FARE_TIER_LABELS[fare_tier_filter] if fare_tier_filter is not None else "All"
        plot_fare_vs_avg_routes(fig, df, airports, fare_tier_filter=fare_tier_filter)  # routes first
        plot_all_airports(fig, airports)                                                # airports on top
        _apply_geo_layout(fig, f"{title} — Fare vs Average ({tier_label})")

    elif layer_id == "cabin_routes":
        cabin_label = cabin_filter.title() if cabin_filter else "All Cabins"
        k_label = f", top {k}" if k else ""
        plot_cabin_routes(fig, df, airports, cabin_filter=cabin_filter, k=k)  # routes first
        plot_all_airports(fig, airports)                                        # airports on top
        _apply_geo_layout(fig, f"{title} — Cabin Class ({cabin_label}{k_label})")

    else:
        plot_all_airports(fig, airports)
        _apply_geo_layout(fig, title)

    return fig
