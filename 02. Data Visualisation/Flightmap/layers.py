import plotly.graph_objects as go
import pandas as pd
import numpy as np

TRACE_TEXT_COLOR = "yellow"

def plot_all_routes(fig: go.Figure, lats, lons):
    fig.add_trace(
        go.Scattergeo(
            lon=lons,
            lat=lats,
            mode="lines",
            line=dict(width=1, color="cyan"),
            opacity=0.3,
            name="All Routes",
            hoverinfo="skip",
        )
    )
    return fig


def plot_all_airports(fig: go.Figure, airports):
    fig.add_trace(
        go.Scattergeo(
            lon=airports["lon"],
            lat=airports["lat"],
            text=airports["City"].astype(str) + "<br>Total Flights: " + airports["traffic"].astype(int).astype(str),
            mode="markers",
            marker=dict(
                size=airports["size"],
                color="red",
                sizemode="area",
            ),
            name="Airports",
            hovertemplate="%{text}<extra></extra>",
        )
    )
    return fig


def plot_top_k_airports(fig: go.Figure, airports, k: int = 10):
    """Highlight the top-k busiest airports (by total traffic) as large gold markers."""
    top = airports.nlargest(k, "traffic").copy()
    top["label"] = (
        top["airport"].astype(str) + " – " + top["City"].astype(str)
        + "<br>Total Flights: " + top["traffic"].astype(int).astype(str)
    )

    fig.add_trace(
        go.Scattergeo(
            lon=top["lon"],
            lat=top["lat"],
            text=top["label"],
            mode="markers+text",
            textposition="top center",
            textfont=dict(color=TRACE_TEXT_COLOR, size=10),
            marker=dict(
                size=top["size"] * 1.5,
                color="gold",
                sizemode="area",
                line=dict(width=1, color="white")
            ),
            hovertemplate="%{text}<extra>Top Hub</extra>",
            name=f"Top {k} Hubs"
        )
    )
    return fig


def plot_top_k_routes(fig: go.Figure, flightData, airports, k: int = 10):
    """Draw the top-k highest-traffic O-D routes as bright highlighted lines.

    Computes counts from raw flight data so the result is never limited by
    the spaghetti pre-filter applied to the 'all routes' layer.
    """
    # Build O-D counts from raw segment data (same logic as DataLoader._get_flight_legs)
    dep = flightData["segmentsDepartureAirportCodes"].explode().reset_index(drop=True)
    arr = flightData["segmentsArrivalAirportCodes"].explode().reset_index(drop=True)
    legs = pd.DataFrame({"startingAirport": dep, "destinationAirport": arr}).dropna()

    routes = (
        legs.groupby(["startingAirport", "destinationAirport"])
        .size()
        .reset_index(name="count")
    )

    coord = airports[["airport", "lat", "lon"]]
    routes = (
        routes
        .merge(coord.rename(columns={"airport": "startingAirport", "lat": "start_lat", "lon": "start_lon"}),
               on="startingAirport", how="left")
        .merge(coord.rename(columns={"airport": "destinationAirport", "lat": "end_lat", "lon": "end_lon"}),
               on="destinationAirport", how="left")
        .dropna(subset=["start_lat", "end_lat"])
    )

    top = routes.nlargest(k, "count").copy()
    nan_col = np.full(len(top), None)
    lons = np.c_[top["start_lon"].values, top["end_lon"].values, nan_col].ravel()
    lats = np.c_[top["start_lat"].values, top["end_lat"].values, nan_col].ravel()

    # Mid-point hover labels (one per segment, placed at midpoint)
    mid_lons = ((top["start_lon"].values + top["end_lon"].values) / 2)
    mid_lats = ((top["start_lat"].values + top["end_lat"].values) / 2)
    labels = (
        top["startingAirport"].astype(str) + " → " + top["destinationAirport"].astype(str)
        + "<br>Flights: " + top["count"].astype(str)
    )

    fig.add_trace(
        go.Scattergeo(
            lon=lons,
            lat=lats,
            mode="lines",
            line=dict(width=2.5, color="lime"),
            opacity=0.85,
            hoverinfo="skip",
            name=f"Top {k} Routes"
        )
    )

    # Invisible markers at midpoints carry the hover tooltip
    fig.add_trace(
        go.Scattergeo(
            lon=mid_lons,
            lat=mid_lats,
            text=labels,
            mode="markers",
            marker=dict(size=6, color=TRACE_TEXT_COLOR, opacity=0.6),
            hovertemplate="%{text}<extra>Top Route</extra>",
            showlegend=False
        )
    )
    return fig


def plot_top_k_airline_airports(fig: go.Figure, flightData, airports, airline_name: str, k: int = 10):
    """Plot the top-k airports (by number of segments) for a given airline name."""
    import pandas as pd

    # Explode segments so each row = one flight leg + its airline
    dep = flightData["segmentsDepartureAirportCodes"].explode().reset_index(drop=True)
    arr = flightData["segmentsArrivalAirportCodes"].explode().reset_index(drop=True)
    airlines = flightData["segmentsAirlineNames"].explode().reset_index(drop=True)

    seg = pd.DataFrame({
        "startingAirport": dep,
        "destinationAirport": arr,
        "airline": airlines
    }).dropna()

    # Filter to the requested airline (case-insensitive partial match)
    mask = seg["airline"].str.contains(airline_name, case=False, na=False)
    filtered = seg[mask]

    if filtered.empty:
        print(f"No segments found for airline: {airline_name!r}")
        return fig

    traffic = (
        filtered["startingAirport"].value_counts()
        .add(filtered["destinationAirport"].value_counts(), fill_value=0)
    ).reset_index()
    traffic.columns = ["airport", "airline_traffic"]

    top = (
        traffic.nlargest(k, "airline_traffic")
               .merge(airports[["airport", "lat", "lon", "City"]], on="airport", how="left")
               .dropna(subset=["lat", "lon"])
    )

    top["size"] = 5 + top["airline_traffic"] / top["airline_traffic"].max() * 25
    top["label"] = (
        top["airport"].astype(str) + " – " + top["City"].astype(str)
        + "<br>Airline: " + airline_name
        + "<br>Segments: " + top["airline_traffic"].astype(int).astype(str)
    )

    fig.add_trace(
        go.Scattergeo(
            lon=top["lon"],
            lat=top["lat"],
            text=top["label"],
            mode="markers+text",
            textposition="top center",
            textfont=dict(color=TRACE_TEXT_COLOR, size=10),
            marker=dict(
                size=top["size"],
                color="violet",
                sizemode="area",
                line=dict(width=1, color="white")
            ),
            hovertemplate="%{text}<extra>" + airline_name + "</extra>",
            name=f"Top {k} – {airline_name}"
        )
    )
    return fig


# ---------------------------------------------------------------------------
# Haul-type routes  (short / medium / long)
# Buckets: short < 500 mi | medium 500-1500 mi | long > 1500 mi
# ---------------------------------------------------------------------------

_HAUL_BUCKETS = [
    ("Short (<500 mi)",   0,    500,  "deepskyblue"),
    ("Medium (500-1500)", 500,  1500, "orange"),
    ("Long (>1500 mi)",   1500, None, "tomato"),
]

def plot_haul_routes(fig: go.Figure, flightData, airports, haul_filter: str | None = None):
    """
    Draw routes coloured by haul type based on totalTravelDistance.
    One Scattergeo trace per bucket (short / medium / long).
    If haul_filter is given, only that bucket label is plotted.
    """

    # Route-level: group by OD pair, take mean distance and mean fare
    od = (
        flightData.groupby(["startingAirport", "destinationAirport"])
          .agg(avg_distance=("totalTravelDistance", "mean"),
               count=("legId", "count"))
          .reset_index()
    )

    coord = airports[["airport", "lat", "lon"]]
    od = (
        od.merge(coord.rename(columns={"airport": "startingAirport",
                                       "lat": "start_lat", "lon": "start_lon"}),
                 on="startingAirport", how="left")
          .merge(coord.rename(columns={"airport": "destinationAirport",
                                       "lat": "end_lat", "lon": "end_lon"}),
                 on="destinationAirport", how="left")
          .dropna(subset=["start_lat", "end_lat"])
    )

    for label, lo, hi, color in _HAUL_BUCKETS:
        if haul_filter is not None and label != haul_filter:
            continue
        mask = od["avg_distance"] >= lo
        if hi is not None:
            mask &= od["avg_distance"] < hi
        subset = od[mask]
        if subset.empty:
            continue

        nan_col = np.full(len(subset), None)
        lons = np.c_[subset["start_lon"].values, subset["end_lon"].values, nan_col].ravel()
        lats = np.c_[subset["start_lat"].values, subset["end_lat"].values, nan_col].ravel()

        fig.add_trace(
            go.Scattergeo(
                lon=lons,
                lat=lats,
                mode="lines",
                line=dict(width=1, color=color),
                opacity=0.4,
                hoverinfo="skip",
                name=label,
            )
        )
    return fig


# ---------------------------------------------------------------------------
# Top-k layover airports
# ---------------------------------------------------------------------------

def plot_top_k_layover_airports(fig: go.Figure, flightData, airports, k: int = 10):
    """
    Plot the top-k airports most frequently used as layover stops.
    Layover airports are intermediate stops (not the overall origin or destination).
    Only flights with numStops > 0 are considered.
    """
    import pandas as pd

    multi = flightData[flightData["numStops"] > 0].copy()

    # Each segmentsDepartureAirportCodes list looks like [A, B, ...].
    # Intermediate airports = all departure airports except the first one
    # (equiv. all arrival airports except the last one).
    def intermediates(row):
        deps = row["segmentsDepartureAirportCodes"]
        try:
            deps = list(deps)
        except TypeError:
            return []
        if len(deps) > 1:
            return deps[1:]          # skip first (= startingAirport)
        return []

    layover_series = multi.apply(intermediates, axis=1).explode().dropna()
    layover_series = layover_series[layover_series != ""]

    counts = layover_series.value_counts().reset_index()
    counts.columns = ["airport", "layover_count"]

    top = (
        counts.nlargest(k, "layover_count")
              .merge(airports[["airport", "lat", "lon", "City"]], on="airport", how="left")
              .dropna(subset=["lat", "lon"])
    )

    max_c = top["layover_count"].max()
    top["size"] = 8 + top["layover_count"] / max_c * 20
    top["label"] = (
        top["airport"].astype(str) + " – " + top["City"].astype(str)
        + "<br>Layover count: " + top["layover_count"].astype(int).astype(str)
    )

    fig.add_trace(
        go.Scattergeo(
            lon=top["lon"],
            lat=top["lat"],
            text=top["label"],
            mode="markers+text",
            textposition="top center",
            textfont=dict(color="yellow", size=10),
            marker=dict(
                size=top["size"],
                color="yellow",
                sizemode="area",
                line=dict(width=1, color="white"),
            ),
            hovertemplate="%{text}<extra>Layover Hub</extra>",
            name=f"Top {k} Layover Airports",
        )
    )
    return fig


# ---------------------------------------------------------------------------
# Fare vs. average  (distance-bucketed, green-red colour scale)
# ---------------------------------------------------------------------------

# Distance buckets (miles): each tuple = (label, lo, hi)
_DIST_BUCKETS = [
    ("<500",      0,    500),
    ("500-1000",  500,  1000),
    ("1000-1500", 1000, 1500),
    ("1500-2000", 1500, 2000),
    (">2000",     2000, None),
]

# 5-step green → red palette (index 0 = cheapest, 4 = most expensive)
_FARE_COLORS = ["#00c44f", "#7ecf00", "#f5c400", "#f57800", "#e03000"]

_FARE_TIER_LABELS = [
    "Very cheap (< 20th pct)",
    "Cheap (20-40th pct)",
    "Average (40-60th pct)",
    "Expensive (60-80th pct)",
    "Very expensive (> 80th pct)",
]

def plot_fare_vs_avg_routes(fig: go.Figure, flightData, airports, min_flights: int = 30, fare_tier_filter: int | None = None):
    """
    Draw routes coloured on a green-red scale according to whether their
    average fare is below or above the mean fare for their distance bucket.

    Routes with fewer than `min_flights` observations are excluded.
    If fare_tier_filter is given (0-4), only that tier is plotted.
    """
    import numpy as np
    import pandas as pd

    od = (
        flightData.groupby(["startingAirport", "destinationAirport"])
          .agg(
              avg_fare=("totalFare", "mean"),
              avg_distance=("totalTravelDistance", "mean"),
              count=("legId", "count"),
          )
          .reset_index()
    )
    od = od[od["count"] >= min_flights]

    # Assign distance bucket
    def assign_bucket(d):
        for label, lo, hi in _DIST_BUCKETS:
            if d >= lo and (hi is None or d < hi):
                return label
        return _DIST_BUCKETS[-1][0]

    od["bucket"] = od["avg_distance"].apply(assign_bucket)

    # Bucket-level average fare
    bucket_avg = od.groupby("bucket")["avg_fare"].mean().rename("bucket_avg_fare")
    od = od.join(bucket_avg, on="bucket")

    # Relative fare ratio
    od["fare_ratio"] = od["avg_fare"] / od["bucket_avg_fare"]

    # Quantile-bin into 5 colour tiers within each bucket
    od["color_tier"] = (
        od.groupby("bucket")["fare_ratio"]
          .transform(lambda x: pd.qcut(x, q=5, labels=False, duplicates="drop"))
          .fillna(2)
          .astype(int)
    )

    # Merge coordinates
    coord = airports[["airport", "lat", "lon"]]
    od = (
        od.merge(coord.rename(columns={"airport": "startingAirport",
                                       "lat": "start_lat", "lon": "start_lon"}),
                 on="startingAirport", how="left")
          .merge(coord.rename(columns={"airport": "destinationAirport",
                                       "lat": "end_lat", "lon": "end_lon"}),
                 on="destinationAirport", how="left")
          .dropna(subset=["start_lat", "end_lat"])
    )

    for tier in range(5):
        if fare_tier_filter is not None and tier != fare_tier_filter:
            continue
        subset = od[od["color_tier"] == tier]
        if subset.empty:
            continue
        tier_label = _FARE_TIER_LABELS[tier]

        nan_col = np.full(len(subset), None)
        lons = np.c_[subset["start_lon"].values, subset["end_lon"].values, nan_col].ravel()
        lats = np.c_[subset["start_lat"].values, subset["end_lat"].values, nan_col].ravel()

        # Midpoint hover markers
        mid_lons = (subset["start_lon"].values + subset["end_lon"].values) / 2
        mid_lats = (subset["start_lat"].values + subset["end_lat"].values) / 2
        labels = (
            subset["startingAirport"].astype(str) + " → " + subset["destinationAirport"].astype(str)
            + "<br>Avg fare: $" + subset["avg_fare"].round(0).astype(int).astype(str)
            + "<br>Bucket avg: $" + subset["bucket_avg_fare"].round(0).astype(int).astype(str)
            + "<br>Distance bucket: " + subset["bucket"].astype(str)
        )

        color = _FARE_COLORS[tier]

        fig.add_trace(
            go.Scattergeo(
                lon=lons, lat=lats,
                mode="lines",
                line=dict(width=1, color=color),
                opacity=0.5,
                hoverinfo="skip",
                name=tier_label,
                legendgroup=f"fare_tier_{tier}",
            )
        )
        fig.add_trace(
            go.Scattergeo(
                lon=mid_lons, lat=mid_lats,
                text=labels,
                mode="markers",
                marker=dict(size=4, color=color, opacity=0.5),
                hovertemplate="%{text}<extra></extra>",
                showlegend=False,
                legendgroup=f"fare_tier_{tier}",
            )
        )

    return fig


# ---------------------------------------------------------------------------
# Cabin class routes
# ---------------------------------------------------------------------------

_CABIN_COLORS = {
    "economy":         "lightgreen",
    "premium ecomony": "lightblue",
    "business":      "gold",
    "first":         "yellow",
}

CABIN_OPTIONS = list(_CABIN_COLORS.keys())


def plot_cabin_routes(
    fig: go.Figure,
    flightData,
    airports,
    cabin_filter: str | None = None,
    k: int | None = None,
):
    """Draw O-D routes coloured by cabin class.

    Args:
        cabin_filter: one of the keys in _CABIN_COLORS, or None to show all cabins.
        k: if given, show only the top-k O-D pairs by flight count for each cabin.
    """
    coord = airports[["airport", "lat", "lon"]].set_index("airport")
    cabins_to_plot = [cabin_filter] if cabin_filter else list(_CABIN_COLORS.keys())

    for cabin in cabins_to_plot:
        color = _CABIN_COLORS.get(cabin, "white")

        # Rows where at least one segment has this cabin code
        exploded_idx = (
            flightData["segmentsCabinCodes"]
            .explode()
            .astype(str)
            .str.strip()
        )
        has_cabin = exploded_idx[exploded_idx == cabin].index.unique()
        subset = flightData.loc[has_cabin]

        if subset.empty:
            continue

        # Count flights per O-D pair
        od = (
            subset.groupby(["startingAirport", "destinationAirport"])
            .size()
            .reset_index(name="flight_count")
            .sort_values("flight_count", ascending=False)
        )

        if k is not None:
            od = od.head(k)

        od = (
            od.merge(
                coord[["lat", "lon"]].rename(columns={"lat": "start_lat", "lon": "start_lon"}),
                left_on="startingAirport", right_index=True, how="left",
            ).merge(
                coord[["lat", "lon"]].rename(columns={"lat": "end_lat", "lon": "end_lon"}),
                left_on="destinationAirport", right_index=True, how="left",
            ).dropna(subset=["start_lat", "end_lat"])
        )

        if od.empty:
            continue

        legend_label = cabin.title() + (f" (top {k})" if k is not None else "")

        nan_col = np.full(len(od), None)
        route_lons = np.c_[od["start_lon"].values, od["end_lon"].values, nan_col].ravel()
        route_lats = np.c_[od["start_lat"].values, od["end_lat"].values, nan_col].ravel()

        # Route lines
        fig.add_trace(
            go.Scattergeo(
                lon=route_lons, lat=route_lats,
                mode="lines",
                line=dict(width=1.2, color=color),
                opacity=0.4,
                name=legend_label,
                legendgroup=f"cabin_{cabin}",
                hoverinfo="skip",
            )
        )

        # Midpoint hover markers with flight count
        mid_lons = (od["start_lon"].values + od["end_lon"].values) / 2
        mid_lats = (od["start_lat"].values + od["end_lat"].values) / 2
        hover_text = (
            od["startingAirport"].astype(str) + " → " + od["destinationAirport"].astype(str)
            + "<br>Cabin: " + cabin.title()
            + "<br>Flights: " + od["flight_count"].astype(str)
        )
        fig.add_trace(
            go.Scattergeo(
                lon=mid_lons, lat=mid_lats,
                text=hover_text,
                mode="markers",
                marker=dict(size=4, color=color, opacity=0.5),
                hovertemplate="%{text}<extra></extra>",
                showlegend=False,
                legendgroup=f"cabin_{cabin}",
            )
        )

    return fig
