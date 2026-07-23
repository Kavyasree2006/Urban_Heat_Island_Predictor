"""
GIS Charts
"""

import plotly.express as px


def hotspot_map(df):

    return px.scatter_mapbox(
        df,
        lat="Latitude",
        lon="Longitude",
        color="Heat Risk",
        size="Heat Risk Score",
        hover_name="City Name",
        zoom=2,
        height=700,
        mapbox_style="carto-positron"
    )


def geo_map(df):

    return px.scatter_geo(
        df,
        lat="Latitude",
        lon="Longitude",
        color="Heat Risk",
        size="Heat Risk Score",
        hover_name="City Name"
    )


def kmeans_scatter(df):

    return px.scatter(
        df,
        x="Longitude",
        y="Latitude",
        color=df["KMeans Cluster"].astype(str),
        size="Heat Risk Score",
        hover_name="City Name",
        template="plotly_white"
    )


def dbscan_scatter(df):

    return px.scatter(
        df,
        x="Longitude",
        y="Latitude",
        color=df["DBSCAN Cluster"].astype(str),
        size="Heat Risk Score",
        hover_name="City Name",
        template="plotly_white"
    )