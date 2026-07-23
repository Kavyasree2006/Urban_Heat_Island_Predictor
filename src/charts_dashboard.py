"""
Dashboard Charts
"""

import plotly.graph_objects as go


def heat_gauge(score):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "Average Heat Risk Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#d62728"},
                "steps": [
                    {"range": [0,25], "color":"#2ecc71"},
                    {"range": [25,50], "color":"#f1c40f"},
                    {"range": [50,75], "color":"#e67e22"},
                    {"range": [75,100], "color":"#e74c3c"},
                ]
            }
        )
    )

    fig.update_layout(template="plotly_white")

    return fig