"""
header.py - Keeper AI Page Headers & Hero Sections
"""
import streamlit as st


def show_page_hero(title: str, subtitle: str = "", badge: str = None):
    """Render the full hero section for the main dashboard."""
    badge_html = ""
    if badge:
        badge_html = f'<div class="kb-hero-badge">✨ {badge}</div>'

    st.markdown(f"""
    <div class="kb-hero">
        {badge_html}
        <div class="kb-hero-title">{title}</div>
        <div class="kb-hero-subtitle">{subtitle}</div>
        <div class="kb-hero-stats">
            <div>
                <div class="kb-hero-stat-value">93.1%</div>
                <div class="kb-hero-stat-label">Model AUC Score</div>
            </div>
            <div>
                <div class="kb-hero-stat-value">16,431</div>
                <div class="kb-hero-stat-label">Customers Monitored</div>
            </div>
            <div>
                <div class="kb-hero-stat-value">2,832</div>
                <div class="kb-hero-stat-label">At-Risk Detected</div>
            </div>
            <div>
                <div class="kb-hero-stat-value">$446K</div>
                <div class="kb-hero-stat-label">MRR Protected</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def show_page_header(title: str, description: str = "", icon: str = ""):
    """Render a clean page header for inner pages."""
    icon_html = f'<span style="font-size:28px; margin-right:12px;">{icon}</span>' if icon else ""
    desc_html = f'<div class="kb-page-desc">{description}</div>' if description else ""
    st.markdown(f"""
    <div class="kb-page-hero">
        <div style="display:flex; align-items:center; margin-bottom:6px;">
            {icon_html}
            <h1 class="kb-page-title">{title}</h1>
        </div>
        {desc_html}
    </div>
    """, unsafe_allow_html=True)
