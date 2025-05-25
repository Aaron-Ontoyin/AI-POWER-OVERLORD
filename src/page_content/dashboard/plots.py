"""
This module contains the functions to create the plots for the dashboard
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go


df = pd.DataFrame(
    {
        "T1": np.sin(np.arange(0, 10, 0.1)),
        "T2": np.cos(np.arange(0, 10, 0.1)),
        "T3": np.tan(np.arange(0, 10, 0.1)),
    },
    index=pd.date_range(start="2024-01-01", periods=100, freq="D"),
)


def create_consumption_patterns_fig():
    df.index = pd.to_datetime(df.index)
    df_long = df.reset_index().melt(
        id_vars="index", var_name="transformer", value_name="consumption"
    )
    df_long.rename(columns={"index": "timestamp"}, inplace=True)

    df_total = df_long.groupby("timestamp")["consumption"].sum().reset_index()

    fig = go.Figure()

    transformers = df_long["transformer"].unique()

    for t in transformers:
        fig.add_trace(
            go.Scatter(
                x=df_long[df_long["transformer"] == t]["timestamp"],
                y=df_long[df_long["transformer"] == t]["consumption"],
                mode="lines",
                name=t,
            )
        )

    latest_time = df_total["timestamp"].max()
    latest_total = df_total[df_total["timestamp"] == latest_time]["consumption"].values[
        0
    ]

    fig.add_annotation(
        x=latest_time,
        y=latest_total,
        text=f"Total: {latest_total:.2f} kWh",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40,
        font=dict(size=14, color="green"),
        bgcolor="rgba(255,255,255,0.8)",
    )

    fig.update_layout(
        title="Transformer Consumption Over Time",
        xaxis_title="Time",
        yaxis_title="Consumption (kWh)",
        template="plotly_white",
        legend_title="Transformer",
        font=dict(family="Arial", size=12),
        hovermode="x unified",
        transition_duration=500,
    )
    return fig
