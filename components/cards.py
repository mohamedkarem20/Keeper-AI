"""
cards.py - Keeper AI Reusable Card Components
"""
import streamlit as st


def kpi_card(label: str, value: str, delta: str = None, positive: bool = True, icon: str = ""):
    """
    Render a KPI metric card in Keeper AI brand style.

    Args:
        label:    Card title text.
        value:    Primary large metric value.
        delta:    Change indicator text (e.g. '+15.5% vs last month').
        positive: If True, delta renders green; False renders red.
        icon:     Optional emoji icon for the card.
    """
    delta_html = ""
    if delta:
        badge_class = "kb-badge-success" if positive else "kb-badge-danger"
        arrow = "▲" if positive else "▼"
        delta_html = f'<div class="kb-kpi-footer"><span class="{badge_class}">{arrow} {delta}</span></div>'

    icon_html = f'<span style="font-size:22px; margin-bottom:10px; display:block;">{icon}</span>' if icon else ""

    st.markdown(f"""
    <div class="kb-kpi-card">
        {icon_html}
        <div class="kb-kpi-label">{label}</div>
        <div class="kb-kpi-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def card_open(title: str = "", action_label: str = None):
    """
    Open a kb-card container. Must be paired with card_close().
    """
    action_html = ""
    if action_label:
        action_html = f'<span style="font-size:11px;color:var(--primary);font-weight:600;cursor:pointer;">{action_label}</span>'
    title_html = f'<div class="kb-card-title">{title} {action_html}</div>' if title else ""
    st.markdown(f'<div class="kb-card">{title_html}', unsafe_allow_html=True)


def card_close():
    """Close a kb-card container."""
    st.markdown('</div>', unsafe_allow_html=True)


def alert_card(title: str, description: str, severity: str = "info"):
    """
    Render an alert block.

    severity: 'success' | 'warning' | 'danger' | 'info'
    """
    icons = {"success": "✅", "warning": "⚠️", "danger": "🚨", "info": "ℹ️"}
    icon = icons.get(severity, "ℹ️")
    st.markdown(f"""
    <div class="kb-alert kb-alert-{severity}">
        <span style="font-size:18px;flex-shrink:0;">{icon}</span>
        <div>
            <div class="kb-alert-title">{title}</div>
            <div class="kb-alert-desc">{description}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def risk_badge(label: str, severity: str = "info"):
    """Inline status pill badge."""
    cls = f"kb-badge-{severity}"
    dots = {"success": "🟢", "warning": "🟡", "danger": "🔴", "info": "🔵", "primary": "🟣"}
    dot = dots.get(severity, "⚪")
    st.markdown(f'<span class="{cls}">{dot} {label}</span>', unsafe_allow_html=True)
