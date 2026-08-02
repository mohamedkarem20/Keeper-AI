"""
sidebar.py - Keeper AI Brand Sidebar
"""
import streamlit as st


PAGES = [
    {"path": "app.py",                        "label": "Dashboard",        "icon": "🏠"},
    {"path": "pages/01_Prediction.py",         "label": "Prediction",       "icon": "🔮"},
    {"path": "pages/02_Analytics.py",          "label": "Analytics",        "icon": "📊"},
    {"path": "pages/03_Explainability.py",     "label": "Explain AI",       "icon": "🧠"},
    {"path": "pages/04_NLP_Sentiment.py",      "label": "NLP Insights",     "icon": "💬"},
    {"path": "pages/05_Model_Performance.py",  "label": "Model Performance","icon": "📈"},
    {"path": "pages/06_Batch_Prediction.py",   "label": "Batch Prediction", "icon": "📁"},
    {"path": "pages/07_About.py",              "label": "About",            "icon": "ℹ️"},
]


def show_sidebar():
    """Render the Keeper AI premium sidebar."""
    with st.sidebar:
        # ── Brand ──
        st.markdown("""
        <div class="kb-brand">
            <div class="kb-logo">🛡️</div>
            <div>
                <div class="kb-brand-name">Keeper AI</div>
                <div class="kb-brand-sub">AI-powered churn platform</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Navigation ──
        st.markdown('<span class="kb-nav-label">Platform</span>', unsafe_allow_html=True)
        for page in PAGES:
            st.page_link(page["path"], label=page["label"], icon=page["icon"],
                         use_container_width=True)

        # ── System Status ──
        st.markdown("""
        <div class="kb-status">
            <div class="kb-status-title">System Status</div>
            <div class="kb-status-row"><span class="kb-dot-green"></span> AI Engine Operational</div>
            <div class="kb-status-row"><span class="kb-dot-blue"></span> XGBoost v2 Loaded</div>
            <div class="kb-status-row"><span class="kb-dot-blue"></span> NLP Pipeline Ready</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Footer ──
        st.markdown("""
        <div class="kb-sidebar-footer">
            <div class="kb-sidebar-footer-text">
                v2.0.0 &nbsp;·&nbsp; XGBoost &nbsp;·&nbsp; AUC 0.931<br>
                © 2025 Keeper Intelligence
            </div>
        </div>
        """, unsafe_allow_html=True)
