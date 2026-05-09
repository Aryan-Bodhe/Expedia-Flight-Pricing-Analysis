"""
map/main.py
-----------
Dash server — left sidebar for layer selection + parameters, right panel for the map.

Run with:
    python map/main.py

URL:
    http://flightmap.local:8050
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dash
from dash import dcc, html, Input, Output, State, callback

from map.dataloader import DataLoader
from map.views import build_layer_fig, LAYER_META, HAUL_OPTIONS, FARE_TIER_OPTIONS, CABIN_OPTIONS

# ---------------------------------------------------------------------------
# Load data once at startup
# ---------------------------------------------------------------------------

print("Loading data…")
loader              = DataLoader()
airports            = loader.get_airports()
routes, lats, lons  = loader.get_routes(filter_spaghetti=90)
df                  = loader.flight_data
print("Data loaded.")

# Unique airline names from the segments column
_airlines = sorted(set(
    str(a) for a in df["segmentsAirlineNames"].explode().dropna()
    if str(a).strip()
))

# ---------------------------------------------------------------------------
# Sets derived from LAYER_META
# ---------------------------------------------------------------------------

_USES_K          = {lid for lid, _, uk, *_       in LAYER_META if uk}
_USES_AIRLINE    = {lid for lid, _, _uk, ua, *_   in LAYER_META if ua}
_USES_HAUL       = {lid for lid, _, _uk, _ua, uh, *_ in LAYER_META if uh}
_USES_FARE_TIER  = {lid for lid, _, _uk, _ua, _uh, uft, *_ in LAYER_META if uft}
_USES_CABIN      = {lid for lid, _, _uk, _ua, _uh, _uft, uc in LAYER_META if uc}

# ---------------------------------------------------------------------------
# Dash app
# ---------------------------------------------------------------------------

app = dash.Dash(__name__, title="US Flight Network")

# ---- Shared styles ---------------------------------------------------------

_SB = {"backgroundColor": "#1a1a2e"}

SIDEBAR_STYLE = {
    **_SB,
    "width": "270px",
    "minWidth": "270px",
    "height": "100vh",
    "padding": "20px 16px",
    "display": "flex",
    "flexDirection": "column",
    "overflowY": "auto",
    "boxSizing": "border-box",
    "borderRight": "1px solid #2e2e4e",
}

SECTION_HEADER = {
    "color": "#7878aa",
    "fontSize": "10px",
    "fontWeight": "700",
    "letterSpacing": "1.4px",
    "textTransform": "uppercase",
    "marginBottom": "6px",
    "marginTop": "18px",
}

PARAM_LABEL = {
    "color": "#9999bb",
    "fontSize": "11px",
    "marginBottom": "4px",
    "marginTop": "12px",
}

INPUT_STYLE = {
    "width": "100%",
    "backgroundColor": "#252545",
    "color": "#fff",
    "border": "1px solid #3e3e6e",
    "borderRadius": "6px",
    "padding": "6px 10px",
    "fontSize": "13px",
    "boxSizing": "border-box",
}

DROPDOWN_STYLE = {
    "backgroundColor": "#252545",
    "color": "#fff",
    "border": "none",
}

APPLY_BUTTON = {
    "width": "100%",
    "backgroundColor": "#4a6cf7",
    "color": "white",
    "border": "none",
    "borderRadius": "8px",
    "padding": "10px",
    "fontSize": "14px",
    "fontWeight": "600",
    "cursor": "pointer",
    "marginTop": "20px",
    "letterSpacing": "0.5px",
}

# ---- Layout ----------------------------------------------------------------

app.layout = html.Div(
    style={"display": "flex", "height": "100vh", "backgroundColor": "#111",
           "fontFamily": "'Inter', 'Segoe UI', sans-serif"},
    children=[

        # ---- Left sidebar --------------------------------------------------
        html.Div(style=SIDEBAR_STYLE, children=[

            html.Div("Flight Network", style={
                "color": "#fff", "fontSize": "18px", "fontWeight": "700",
                "marginBottom": "2px",
            }),
            html.Div("US segment-level analysis", style={
                "color": "#555577", "fontSize": "12px",
            }),

            html.Div("Layer", style=SECTION_HEADER),

            dcc.RadioItems(
                id="layer-radio",
                options=[
                    {"label": html.Span(label, style={"fontSize": "13px"}), "value": lid}
                    for lid, label, *_ in LAYER_META
                ],
                value="all_routes",
                labelStyle={
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "8px",
                    "padding": "7px 10px",
                    "borderRadius": "6px",
                    "cursor": "pointer",
                    "color": "#ccccee",
                },
                inputStyle={"accentColor": "#4a6cf7"},
                style={"display": "flex", "flexDirection": "column", "gap": "1px"},
            ),

            html.Div("Parameters", style=SECTION_HEADER),

            # k ---
            html.Div(id="k-wrapper", children=[
                html.Div("Top-K", style=PARAM_LABEL),
                dcc.Input(
                    id="k-input", type="number", value=10, min=1, max=100, step=1,
                    style=INPUT_STYLE, debounce=True,
                ),
            ]),

            # airline dropdown ---
            html.Div(id="airline-wrapper", style={"display": "none"}, children=[
                html.Div("Airline", style=PARAM_LABEL),
                dcc.Dropdown(
                    id="airline-dropdown",
                    options=[{"label": a, "value": a} for a in _airlines],
                    value=_airlines[0] if _airlines else "Delta",
                    clearable=False,
                    style={"fontSize": "13px"},
                ),
            ]),

            # haul type dropdown ---
            html.Div(id="haul-wrapper", style={"display": "none"}, children=[
                html.Div("Haul type", style=PARAM_LABEL),
                dcc.Dropdown(
                    id="haul-dropdown",
                    options=[{"label": h, "value": h} for h in HAUL_OPTIONS],
                    value=HAUL_OPTIONS[0],
                    clearable=False,
                    style={"fontSize": "13px"},
                ),
            ]),

            # fare tier dropdown ---
            html.Div(id="fare-wrapper", style={"display": "none"}, children=[
                html.Div("Fare tier", style=PARAM_LABEL),
                dcc.Dropdown(
                    id="fare-dropdown",
                    options=[{"label": t, "value": i} for i, t in enumerate(FARE_TIER_OPTIONS)],
                    value=0,
                    clearable=False,
                    style={"fontSize": "13px"},
                ),
            ]),

            # cabin class dropdown ---
            html.Div(id="cabin-wrapper", style={"display": "none"}, children=[
                html.Div("Cabin class", style=PARAM_LABEL),
                dcc.Dropdown(
                    id="cabin-dropdown",
                    options=[{"label": c.title(), "value": c} for c in CABIN_OPTIONS],
                    value=CABIN_OPTIONS[0],
                    clearable=False,
                    style={"fontSize": "13px"},
                ),
            ]),

            html.Button("Apply", id="apply-btn", n_clicks=0, style=APPLY_BUTTON),

            html.Div(id="status-text", style={
                "color": "#666688", "fontSize": "11px", "marginTop": "10px",
                "textAlign": "center",
            }),
        ]),

        # ---- Map panel -----------------------------------------------------
        html.Div(
            style={"flex": "1", "height": "100vh", "overflow": "hidden"},
            children=[
                dcc.Graph(
                    id="flight-map",
                    figure=build_layer_fig(
                        "all_routes", df, airports, routes, lats, lons,
                        title="US Flight Network",
                    ),
                    style={"height": "100vh"},
                    config={
                        "displayModeBar": True,
                        "scrollZoom": True,
                        "displaylogo": False,
                        "modeBarButtonsToRemove": ["select2d", "lasso2d"],
                    },
                )
            ],
        ),
    ],
)

# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------

@callback(
    Output("k-wrapper",       "style"),
    Output("airline-wrapper", "style"),
    Output("haul-wrapper",    "style"),
    Output("fare-wrapper",    "style"),
    Output("cabin-wrapper",   "style"),
    Input("layer-radio", "value"),
)
def toggle_param_visibility(layer_id):
    show = {"display": "block"}
    hide = {"display": "none"}
    return (
        show if layer_id in _USES_K         else hide,
        show if layer_id in _USES_AIRLINE   else hide,
        show if layer_id in _USES_HAUL      else hide,
        show if layer_id in _USES_FARE_TIER else hide,
        show if layer_id in _USES_CABIN     else hide,
    )


@callback(
    Output("flight-map",  "figure"),
    Output("status-text", "children"),
    Input("apply-btn", "n_clicks"),
    State("layer-radio",      "value"),
    State("k-input",          "value"),
    State("airline-dropdown", "value"),
    State("haul-dropdown",    "value"),
    State("fare-dropdown",    "value"),
    State("cabin-dropdown",   "value"),
    prevent_initial_call=True,
)
def update_map(_, layer_id, k, airline, haul, fare_tier, cabin):
    k          = int(k or 10)
    airline    = (airline or (_airlines[0] if _airlines else "Delta")).strip()
    fare_tier  = int(fare_tier) if fare_tier is not None else None

    fig = build_layer_fig(
        layer_id, df, airports, routes, lats, lons,
        k                = k,
        airline          = airline,
        haul_filter      = haul  if layer_id in _USES_HAUL      else None,
        fare_tier_filter = fare_tier if layer_id in _USES_FARE_TIER else None,
        cabin_filter     = cabin if layer_id in _USES_CABIN     else None,
        title            = "US Flight Network",
    )

    layer_label = next(label for lid, label, *_ in LAYER_META if lid == layer_id)
    parts = [f"Showing: {layer_label}"]
    if layer_id in _USES_K:         parts.append(f"k={k}")
    if layer_id in _USES_AIRLINE:   parts.append(f"airline={airline!r}")
    if layer_id in _USES_HAUL:      parts.append(f"haul={haul!r}")
    if layer_id in _USES_FARE_TIER: parts.append(f"tier={FARE_TIER_OPTIONS[fare_tier]!r}")
    if layer_id in _USES_CABIN:     parts.append(f"cabin={cabin!r}")

    return fig, "  |  ".join(parts)


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    _PORT = 8050
    print("\nStarting Dash server. \nClient: http://flightmap.local:8050\n")
    app.run(debug=False, host="0.0.0.0", port=_PORT)

    print("\nServer terminated successfully.")
