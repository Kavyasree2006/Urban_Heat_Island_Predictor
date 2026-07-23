"""
EDA Charts
"""

import plotly.express as px


def temperature_distribution(df):

    return px.histogram(
        df,
        x="Temperature (°C)",
        nbins=30,
        template="plotly_white",
        title="Temperature Distribution"
    )


def scatter_chart(df, x, y, color=None):

    return px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        template="plotly_white"
    )


def box_plot(df, x, y):

    return px.box(
        df,
        x=x,
        y=y,
        color=x,
        template="plotly_white"
    )


def pie_chart(df, column):

    counts = df[column].value_counts().reset_index()

    counts.columns=[column,"Count"]

    return px.pie(
        counts,
        names=column,
        values="Count",
        hole=.45
    )


def correlation_heatmap(df):

    corr=df.select_dtypes(include="number").corr()

    return px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        title="Correlation Heatmap"
    )