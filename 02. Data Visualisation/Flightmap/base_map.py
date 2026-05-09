import plotly.graph_objects as go

def create_base_map():
    fig = go.Figure()
    fig.update_layout(template="plotly_dark")

    fig.update_layout(
        title="US Flight Network (Segment-Level)",
        title_x=0.5,
        geo=dict(
            scope="usa",
            showland=True,
            landcolor="black",
            countrycolor="black"
        ),
        showlegend=False
    )

    return fig