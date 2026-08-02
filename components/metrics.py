"""
Metrics / KPI Card Components — Customer Churn Intelligence Platform
"""

import streamlit as st
from typing import Optional


def kpi_row(metrics: list):
    """
    Render a horizontal row of KPI cards using CSS grid.

    Each metric dict:
        {
            "label": str,      # Card label (uppercase caption)
            "value": str,      # Main displayed value
            "delta": str,      # Optional trend text
            "delta_type": str, # "positive" | "negative" | "neutral"
            "icon": str,       # Emoji icon
            "color": str,      # "blue" | "green" | "red" | "orange" | "purple"
        }
    """
    cards_html = ""
    for m in metrics:
        color = m.get("color", "blue")
        delta = m.get("delta", "")
        delta_type = m.get("delta_type", "neutral")
        icon = m.get("icon", "📊")

        delta_html = (
            f'<span class="kpi-delta {delta_type}">{delta}</span>'
            if delta else ""
        )
        cards_html += f'<div class="kpi-card {color}"><div class="kpi-top-row"><div class="kpi-label">{m["label"]}</div><div class="kpi-icon {color}">{icon}</div></div><div class="kpi-value">{m["value"]}</div>{delta_html}</div>'

    st.markdown(f'<div class="kpi-grid">{cards_html}</div>', unsafe_allow_html=True)


def single_kpi_card(label: str, value: str, icon: str = "📊",
                    color: str = "blue", delta: str = "",
                    delta_type: str = "neutral"):
    """Render a single KPI card inline."""
    kpi_row([{
        "label": label, "value": value, "icon": icon,
        "color": color, "delta": delta, "delta_type": delta_type,
    }])


def status_row(items: list = None):
    """
    Render a row of status/health cards.

    Each item dict:
        {"icon": str, "icon_class": str, "label": str, "value": str, "sub": str}
    """
    if items is None:
        items = [
            {"icon": "⚡", "icon_class": "online", "label": "API Engine", "value": "Operational", "sub": "Latency 12ms"},
            {"icon": "🤖", "icon_class": "model", "label": "XGBoost Model", "value": "v2.0 Loaded", "sub": "AUC 0.931"},
            {"icon": "🛡️", "icon_class": "ready", "label": "Pipeline Status", "value": "Healthy", "sub": "0 Errors"}
        ]
    cards_html = ""
    for item in items:
        cards_html += f"""
        <div class="status-card">
            <div class="status-card-icon {item.get('icon_class', 'model')}">
                {item.get('icon', '⚙️')}
            </div>
            <div>
                <div class="status-card-label">{item.get('label', '')}</div>
                <div class="status-card-value">{item.get('value', '')}</div>
                <div class="status-card-sub">{item.get('sub', '')}</div>
            </div>
        </div>
        """
    # Render in columns
    n = len(items)
    if n == 0:
        return
    cols = st.columns(n)
    for col, item in zip(cols, items):
        with col:
            st.markdown(f"""
            <div class="status-card">
                <div class="status-card-icon {item.get('icon_class','model')}">
                    {item.get('icon','⚙️')}
                </div>
                <div>
                    <div class="status-card-label">{item.get('label','')}</div>
                    <div class="status-card-value">{item.get('value','')}</div>
                    <div class="status-card-sub">{item.get('sub','')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
