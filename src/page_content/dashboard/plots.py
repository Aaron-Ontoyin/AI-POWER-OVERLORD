"""
This module contains the functions to create the plots for the dashboard
"""

import plotly.graph_objects as go
import pandas as pd

from .schemas import Plots, DashboardData


def create_consumption_patterns_fig(data: pd.DataFrame) -> go.Figure:
    data.index = pd.to_datetime(data.index)
    df_long = data.reset_index().melt(
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


def create_trend_analysis_fig(data: pd.DataFrame) -> go.Figure:
    return create_consumption_patterns_fig(data)


def create_freq_analysis_fig(data: pd.DataFrame) -> go.Figure:
    return create_consumption_patterns_fig(data)


def create_anomaly_fig(data: pd.DataFrame) -> go.Figure:
    return create_consumption_patterns_fig(data)


def get_plots(data: DashboardData) -> Plots:
    return Plots(
        num_transformers=data.num_transformers,
        num_meters=data.num_meters,
        consump_ptrns_dict=create_consumption_patterns_fig(
            data.consumption_pattern_df
        ).to_dict(),
        trend_analysis_dict=create_trend_analysis_fig(data.trend_analysis_df).to_dict(),
        freq_analysis_dict=create_freq_analysis_fig(data.freq_analysis_df).to_dict(),
        anomaly_dict=create_anomaly_fig(data.anomaly_df).to_dict(),
    )


def text_plot(text: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text=text,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=14, color="orange"),
    )
    fig.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False))
    return fig
