"""
Plotly Chart Factory — Customer Churn Intelligence Platform
All charts use a consistent design system.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Optional

# ---- Design Tokens ----
COLORS = ["#2563EB", "#22C55E", "#F59E0B", "#EF4444",
           "#8B5CF6", "#0EA5E9", "#EC4899", "#14B8A6"]
FONT_DISPLAY = "Space Grotesk"
FONT_BODY    = "Inter"


def _base_layout(title: str = "", height: int = 360, show_legend: bool = True) -> dict:
    """Return the standard layout dict for all charts."""
    return dict(
        title=dict(
            text=title,
            font=dict(family=FONT_DISPLAY, size=14, color="#0F172A"),
            x=0, xanchor="left",
        ),
        paper_bgcolor="white",
        plot_bgcolor="rgba(248,250,252,0.6)",
        font=dict(family=FONT_BODY, size=11, color="#475569"),
        margin=dict(l=10, r=10, t=40 if title else 20, b=10),
        height=height,
        showlegend=show_legend,
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(0,0,0,0)",
            font=dict(size=11),
        ),
        xaxis=dict(
            showgrid=True, gridcolor="#F1F5F9",
            showline=False, linecolor="#E2E8F0",
            tickfont=dict(size=10, color="#94A3B8"),
        ),
        yaxis=dict(
            showgrid=True, gridcolor="#F1F5F9",
            showline=False, linecolor="#E2E8F0",
            tickfont=dict(size=10, color="#94A3B8"),
        ),
        hoverlabel=dict(
            bgcolor="#0F172A",
            bordercolor="#1E293B",
            font=dict(color="white", size=12, family=FONT_BODY),
        ),
    )


def gauge_chart(value: float, title: str = "Churn Probability", max_val: float = 100) -> go.Figure:
    """Radial gauge for prediction probability."""
    if value >= 60:
        bar_color = "#EF4444"
        steps = [
            dict(range=[0, 40],   color="#F0FDF4"),
            dict(range=[40, 65],  color="#FFFBEB"),
            dict(range=[65, 100], color="#FEF2F2"),
        ]
    elif value >= 40:
        bar_color = "#F59E0B"
        steps = [
            dict(range=[0, 40],   color="#F0FDF4"),
            dict(range=[40, 65],  color="#FFFBEB"),
            dict(range=[65, 100], color="#FEF2F2"),
        ]
    else:
        bar_color = "#22C55E"
        steps = [
            dict(range=[0, 40],   color="#F0FDF4"),
            dict(range=[40, 65],  color="#FFFBEB"),
            dict(range=[65, 100], color="#FEF2F2"),
        ]

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        number=dict(
            suffix="%",
            font=dict(family=FONT_DISPLAY, size=28, color="#0F172A"),
        ),
        delta=dict(
            reference=50,
            relative=False,
            decreasing=dict(color="#22C55E"),
            increasing=dict(color="#EF4444"),
            font=dict(size=12),
        ),
        title=dict(text=title, font=dict(family=FONT_DISPLAY, size=13, color="#475569")),
        gauge=dict(
            axis=dict(
                range=[0, max_val],
                tickwidth=1,
                tickcolor="#CBD5E1",
                tickfont=dict(size=9, color="#94A3B8"),
            ),
            bar=dict(color=bar_color, thickness=0.28),
            bgcolor="white",
            borderwidth=0,
            steps=steps,
            threshold=dict(
                line=dict(color="#475569", width=2),
                thickness=0.75,
                value=50,
            ),
        ),
    ))
    fig.update_layout(
        paper_bgcolor="white",
        font=dict(family=FONT_BODY),
        margin=dict(l=20, r=20, t=40, b=10),
        height=260,
    )
    return fig


def roc_curve_chart(fpr: list, tpr: list, auc: float) -> go.Figure:
    """ROC curve chart."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=fpr, y=tpr,
        mode="lines",
        name=f"XGBoost (AUC = {auc:.3f})",
        line=dict(color="#2563EB", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(37,99,235,0.06)",
        hovertemplate="FPR: %{x:.3f}<br>TPR: %{y:.3f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        mode="lines",
        name="Random (AUC = 0.5)",
        line=dict(color="#94A3B8", width=1.5, dash="dash"),
        hoverinfo="skip",
    ))
    layout = _base_layout("ROC Curve", height=370)
    layout["xaxis"]["title"] = dict(text="False Positive Rate", font=dict(size=11))
    layout["yaxis"]["title"] = dict(text="True Positive Rate", font=dict(size=11))
    layout["xaxis"]["range"] = [0, 1]
    layout["yaxis"]["range"] = [0, 1.02]
    fig.update_layout(**layout)
    return fig


def confusion_matrix_chart(cm: list, labels: list = None) -> go.Figure:
    """Confusion matrix heatmap."""
    if labels is None:
        labels = ["Not Churn", "Churn"]
    cm_arr = np.array(cm)
    total = cm_arr.sum()
    text = [[f"<b>{v}</b><br>{v/total*100:.1f}%" for v in row] for row in cm_arr]

    fig = go.Figure(go.Heatmap(
        z=cm_arr,
        x=labels,
        y=labels,
        text=text,
        texttemplate="%{text}",
        textfont=dict(size=14, family=FONT_DISPLAY),
        colorscale=[[0, "#EFF6FF"], [1, "#1D4ED8"]],
        showscale=False,
        hovertemplate="Actual: %{y}<br>Predicted: %{x}<br>Count: %{z}<extra></extra>",
    ))
    layout = _base_layout("Confusion Matrix", height=370, show_legend=False)
    layout["xaxis"]["title"] = "Predicted"
    layout["yaxis"]["title"] = "Actual"
    fig.update_layout(**layout)
    return fig


def shap_bar_chart(features: list, values: list, title: str = "Global Feature Importance") -> go.Figure:
    """Horizontal bar chart for SHAP global importance."""
    sorted_pairs = sorted(zip(values, features), key=lambda x: x[0])
    vals, feats = zip(*sorted_pairs) if sorted_pairs else ([], [])
    colors = ["#2563EB" if v >= 0 else "#EF4444" for v in vals]

    fig = go.Figure(go.Bar(
        x=list(vals),
        y=list(feats),
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        hovertemplate="%{y}: %{x:.4f}<extra></extra>",
    ))
    layout = _base_layout(title, height=max(350, len(feats) * 28))
    layout["yaxis"]["showgrid"] = False
    layout["xaxis"]["title"] = "Mean |SHAP Value|"
    layout["showlegend"] = False
    fig.update_layout(**layout)
    return fig


def shap_waterfall_chart(base_value: float, shap_values: list,
                          feature_names: list, feature_values: list) -> go.Figure:
    """SHAP waterfall chart for local explanation."""
    # Sort by absolute SHAP value, top 12
    pairs = sorted(zip(shap_values, feature_names, feature_values),
                   key=lambda x: abs(x[0]), reverse=True)[:12]
    sv, fn, fv = zip(*pairs) if pairs else ([], [], [])

    labels = [f"{n}<br><span style='font-size:9px;color:#94A3B8'>{v:.3f}</span>"
              for n, v in zip(fn, fv)]
    colors = ["#EF4444" if v > 0 else "#2563EB" for v in sv]

    fig = go.Figure(go.Bar(
        y=labels,
        x=list(sv),
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        hovertemplate="%{y}: %{x:.4f}<extra></extra>",
    ))
    fig.add_vline(x=0, line_width=1, line_color="#CBD5E1")
    layout = _base_layout("Local SHAP Explanation (Waterfall)",
                          height=max(380, len(sv) * 34), show_legend=False)
    layout["xaxis"]["title"] = "SHAP Value (impact on model output)"
    layout["yaxis"]["showgrid"] = False
    fig.update_layout(**layout)
    return fig


def bar_chart(x, y, title: str = "", color: str = "#2563EB",
              xaxis_title: str = "", yaxis_title: str = "", height: int = 360) -> go.Figure:
    """Generic vertical bar chart."""
    fig = go.Figure(go.Bar(
        x=x, y=y,
        marker=dict(color=color, line=dict(width=0)),
        hovertemplate="%{x}: %{y}<extra></extra>",
    ))
    layout = _base_layout(title, height=height)
    layout["xaxis"]["title"] = xaxis_title
    layout["yaxis"]["title"] = yaxis_title
    layout["showlegend"] = False
    fig.update_layout(**layout)
    return fig


def horizontal_bar_chart(y, x, title: str = "", colors=None, height: int = 360) -> go.Figure:
    """Generic horizontal bar chart."""
    if colors is None:
        colors = COLORS[0]
    fig = go.Figure(go.Bar(
        y=y, x=x,
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        hovertemplate="%{y}: %{x}<extra></extra>",
    ))
    layout = _base_layout(title, height=height, show_legend=False)
    layout["yaxis"]["showgrid"] = False
    fig.update_layout(**layout)
    return fig


def donut_chart(labels: list, values: list, title: str = "", height: int = 360) -> go.Figure:
    """Donut chart."""
    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker=dict(colors=COLORS[:len(labels)], line=dict(color="white", width=2)),
        textfont=dict(family=FONT_BODY, size=11),
        hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(family=FONT_DISPLAY, size=14, color="#0F172A"), x=0),
        paper_bgcolor="white",
        font=dict(family=FONT_BODY),
        margin=dict(l=10, r=10, t=40 if title else 20, b=10),
        height=height,
        showlegend=True,
        legend=dict(font=dict(size=11), bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor="#0F172A", bordercolor="#1E293B",
                        font=dict(color="white", size=12)),
    )
    return fig


def histogram_chart(data: list, title: str = "", xaxis_title: str = "",
                    color: str = "#2563EB", height: int = 360,
                    nbins: int = 30) -> go.Figure:
    """Histogram chart."""
    fig = go.Figure(go.Histogram(
        x=data,
        nbinsx=nbins,
        marker=dict(color=color, line=dict(color="white", width=0.5)),
        hovertemplate="%{x}: %{y} customers<extra></extra>",
    ))
    layout = _base_layout(title, height=height, show_legend=False)
    layout["xaxis"]["title"] = xaxis_title
    layout["yaxis"]["title"] = "Count"
    fig.update_layout(**layout)
    return fig


def multi_line_chart(x, y_dict: dict, title: str = "",
                     xaxis_title: str = "", yaxis_title: str = "",
                     height: int = 360) -> go.Figure:
    """Multi-line chart from a dict of {series_name: y_values}."""
    fig = go.Figure()
    for i, (name, y) in enumerate(y_dict.items()):
        fig.add_trace(go.Scatter(
            x=x, y=y, mode="lines+markers",
            name=name,
            line=dict(color=COLORS[i % len(COLORS)], width=2.5),
            marker=dict(size=5),
            hovertemplate=f"{name}: %{{y:.2f}}<extra></extra>",
        ))
    layout = _base_layout(title, height=height)
    layout["xaxis"]["title"] = xaxis_title
    layout["yaxis"]["title"] = yaxis_title
    fig.update_layout(**layout)
    return fig


def scatter_chart(x, y, color=None, title: str = "",
                  xaxis_title: str = "", yaxis_title: str = "",
                  height: int = 380) -> go.Figure:
    """Scatter chart."""
    fig = go.Figure(go.Scatter(
        x=x, y=y,
        mode="markers",
        marker=dict(
            color=color if color is not None else "#2563EB",
            size=6, opacity=0.7,
            line=dict(width=0),
            colorscale=[[0, "#22C55E"], [1, "#EF4444"]] if color is not None else None,
            showscale=color is not None,
            colorbar=dict(thickness=10, len=0.7) if color is not None else None,
        ),
        hovertemplate="X: %{x:.2f}<br>Y: %{y:.2f}<extra></extra>",
    ))
    layout = _base_layout(title, height=height, show_legend=False)
    layout["xaxis"]["title"] = xaxis_title
    layout["yaxis"]["title"] = yaxis_title
    fig.update_layout(**layout)
    return fig


def grouped_bar_chart(categories, groups: dict, title: str = "",
                      xaxis_title: str = "", yaxis_title: str = "",
                      height: int = 380) -> go.Figure:
    """Grouped bar chart."""
    fig = go.Figure()
    for i, (name, values) in enumerate(groups.items()):
        fig.add_trace(go.Bar(
            name=name,
            x=categories,
            y=values,
            marker=dict(color=COLORS[i % len(COLORS)], line=dict(width=0)),
            hovertemplate=f"{name}<br>%{{x}}: %{{y:.2f}}<extra></extra>",
        ))
    layout = _base_layout(title, height=height)
    layout["barmode"] = "group"
    layout["xaxis"]["title"] = xaxis_title
    layout["yaxis"]["title"] = yaxis_title
    fig.update_layout(**layout)
    return fig


def interactive_line_chart(x, y, title: str = "", height: int = 300) -> go.Figure:
    """SaaS Style interactive line chart (Area chart with gradient)."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode="lines",
        line=dict(color="#2B6CB0", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(43, 108, 176, 0.1)",
        hovertemplate="%{x}<br><b>%{y:$,.0f}</b><extra></extra>",
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(family=FONT_DISPLAY, size=15, color="#2D3748"), x=0),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family=FONT_BODY, size=11, color="#A0AEC0"),
        margin=dict(l=10, r=10, t=40 if title else 10, b=10),
        height=height,
        xaxis=dict(showgrid=False, showline=False, tickfont=dict(size=10, color="#A0AEC0")),
        yaxis=dict(showgrid=True, gridcolor="#EDF2F7", showline=False, tickfont=dict(size=10, color="#A0AEC0")),
        hoverlabel=dict(bgcolor="white", font_color="#2D3748", bordercolor="#E2E8F0"),
    )
    return fig


def saas_gauge_chart(value: int, title: str = "", height: int = 250) -> go.Figure:
    """SaaS Style Half-Donut Gauge Chart."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number=dict(
            suffix="%",
            font=dict(family=FONT_DISPLAY, size=32, color="#1A202C")
        ),
        title=dict(text=title, font=dict(family=FONT_DISPLAY, size=15, color="#2D3748")),
        gauge=dict(
            axis=dict(range=[0, 100], tickwidth=0, tickcolor="white", showticklabels=False),
            bar=dict(color="#38B2AC", thickness=0.25),
            bgcolor="#EDF2F7",
            borderwidth=0,
            shape="angular"
        )
    ))
    fig.update_layout(
        paper_bgcolor="white",
        font=dict(family=FONT_BODY),
        margin=dict(l=10, r=10, t=30, b=10),
        height=height,
    )
    return fig
