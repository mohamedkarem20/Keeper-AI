"""
footer.py - Keeper AI Branded Footer
"""
import streamlit as st
import datetime


def show_footer():
    """Render the Keeper AI global footer."""
    year = datetime.datetime.now().year
    st.markdown(f"""
    <div class="kb-footer">
        <div class="kb-footer-brand">
            <div class="kb-footer-logo">🛡️</div>
            <div class="kb-footer-name">Keeper AI</div>
            <span class="kb-footer-copy">&nbsp;&nbsp;© {year} Keeper Intelligence. AI-powered churn prediction platform.</span>
        </div>
        <div class="kb-footer-status">
            <span class="kb-footer-dot"></span>
            All systems operational &nbsp;·&nbsp; XGBoost + NLP &nbsp;·&nbsp; AUC 0.931
        </div>
    </div>
    """, unsafe_allow_html=True)
