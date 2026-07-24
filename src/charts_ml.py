"""
Machine Learning Charts
"""

import plotly.express as px
import plotly.graph_objects as go


def feature_importance_chart(df):

    return px.bar(
        df.sort_values("Importance"),
        x="Importance",
        y="Feature",
        orientation="h",
        color="Importance",
        template="plotly_white"
    )


def actual_vs_predicted(df):

    fig=go.Figure()

    fig.add_trace(
        go.Scatter(
            y=df["Temperature (°C)"],
            mode="lines",
            name="Actual"
        )
    )

    fig.add_trace(
        go.Scatter(
            y=df["Predicted Temperature"],
            mode="lines",
            name="Predicted"
        )
    )

    return fig


def actual_vs_predicted_scatter(df):

    fig=px.scatter(
        df,
        x="Temperature (°C)",
        y="Predicted Temperature",
        trendline="ols",
        template="plotly_white"
    )

    fig.add_shape(
        type="line",
        x0=df["Temperature (°C)"].min(),
        y0=df["Temperature (°C)"].min(),
        x1=df["Temperature (°C)"].max(),
        y1=df["Temperature (°C)"].max(),
        line=dict(color="red",dash="dash")
    )

    return fig


def residual_plot(df):

    residual=df["Temperature (°C)"]-df["Predicted Temperature"]

    return px.histogram(
        x=residual,
        nbins=25,
        template="plotly_white",
        title="Residual Error Distribution"
    )
  
