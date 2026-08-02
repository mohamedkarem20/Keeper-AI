"""
07_About.py - Keeper AI | About & Architecture
"""
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="About | Keeper AI", page_icon="ℹ️", layout="wide")

def _load_css():
    css = Path(__file__).parent.parent / "assets" / "style.css"
    try: st.markdown(f"<style>{css.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
    except FileNotFoundError: pass
_load_css()

from components.sidebar import show_sidebar
from components.header  import show_page_header
from components.footer  import show_footer
from components.cards   import card_open, card_close, alert_card

show_sidebar()
show_page_header("About Keeper AI",
    "Learn about the architecture, technology stack, and mission behind the platform.",
    icon="ℹ️")

c1, c2 = st.columns([0.6, 0.4], gap="large")

with c1:
    card_open("Project Description")
    st.markdown("""
    <div style='color:#334155;font-size:14px;line-height:1.85;'>
        <strong style='color:#0F172A;'>Keeper AI</strong> is an enterprise-grade machine learning
        platform that identifies customers at risk of churning before they cancel.
        <br><br>
        By combining structured demographic and billing data with NLP-based sentiment analysis
        on customer support interactions, Keeper AI delivers real-time, explainable insights
        to retention teams — powered by an optimized XGBoost model and SHAP explainability.
    </div>
    """, unsafe_allow_html=True)
    card_close()

    card_open("System Architecture")
    st.markdown("""
    <div style='background:#F8FAFC;border:1.5px dashed #E2E8F0;border-radius:12px;
                height:240px;display:flex;align-items:center;justify-content:center;
                flex-direction:column;gap:12px;'>
        <span style='font-size:42px;'>🏗️</span>
        <span style='color:#64748B;font-weight:600;'>Architecture Diagram Placeholder</span>
        <span style='color:#94A3B8;font-size:12.5px;text-align:center;max-width:400px;'>
            Data Ingestion → Feature Engineering → XGBoost + NLP Pipeline → SHAP Explainer → Streamlit UI
        </span>
    </div>
    """, unsafe_allow_html=True)
    card_close()

    card_open("Development Timeline")
    st.markdown("""
    <div style='font-size:13.5px;color:#334155;padding-left:20px;
                border-left:2px solid #E2E8F0;margin-left:8px;'>
        <div style='margin-bottom:22px;position:relative;'>
            <div style='position:absolute;left:-27px;top:5px;width:11px;height:11px;
                        background:#4338CA;border-radius:50%;'></div>
            <strong style='color:#0F172A;'>Phase 1 — Data Engineering</strong><br>
            <span style='color:#64748B;font-size:13px;'>Cleaning, feature engineering, TF-IDF vectorization.</span>
        </div>
        <div style='margin-bottom:22px;position:relative;'>
            <div style='position:absolute;left:-27px;top:5px;width:11px;height:11px;
                        background:#4338CA;border-radius:50%;'></div>
            <strong style='color:#0F172A;'>Phase 2 — Model Training</strong><br>
            <span style='color:#64748B;font-size:13px;'>XGBoost tuning, cross-validation, SHAP fitting.</span>
        </div>
        <div style='margin-bottom:22px;position:relative;'>
            <div style='position:absolute;left:-27px;top:5px;width:11px;height:11px;
                        background:#4338CA;border-radius:50%;'></div>
            <strong style='color:#0F172A;'>Phase 3 — UI Architecture</strong><br>
            <span style='color:#64748B;font-size:13px;'>Modular SaaS design system and Streamlit interfaces.</span>
        </div>
        <div style='position:relative;'>
            <div style='position:absolute;left:-27px;top:5px;width:11px;height:11px;
                        background:#10B981;border-radius:50%;
                        box-shadow:0 0 0 3px rgba(16,185,129,0.2);'></div>
            <strong style='color:#0F172A;'>Phase 4 — Deployment ✅</strong><br>
            <span style='color:#64748B;font-size:13px;'>Production layout finalized and launched.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    card_close()

with c2:
    card_open("Developer")
    st.markdown("""
    <div style='display:flex;align-items:center;gap:14px;margin-bottom:18px;'>
        <div style='width:52px;height:52px;border-radius:50%;
                    background:linear-gradient(135deg,#4338CA,#8B5CF6);
                    display:flex;align-items:center;justify-content:center;
                    color:white;font-size:22px;font-weight:bold;flex-shrink:0;'>🧑‍💻</div>
        <div>
            <div style='font-weight:700;font-size:16px;color:#0F172A;'>Lead ML Engineer</div>
            <div style='font-size:13px;color:#64748B;'>Machine Learning · AI · SaaS</div>
        </div>
    </div>
    <div style='display:flex;flex-direction:column;gap:10px;font-size:13.5px;color:#334155;'>
        <div>📧 &nbsp; developer@keeperai.com</div>
        <div>🐙 &nbsp; github.com/keeperai</div>
        <div>🔗 &nbsp; linkedin.com/in/keeperai</div>
    </div>
    """, unsafe_allow_html=True)
    card_close()

    card_open("Technology Stack")
    st.markdown("""
    <div style='display:flex;flex-wrap:wrap;gap:8px;'>
        <span class='kb-badge-primary'>Python 3.10+</span>
        <span class='kb-badge-danger'>Streamlit</span>
        <span class='kb-badge-success'>XGBoost</span>
        <span class='kb-badge-warning'>Scikit-Learn</span>
        <span class='kb-badge-info'>Pandas</span>
        <span class='kb-badge-info'>Plotly</span>
        <span class='kb-badge-primary'>SHAP</span>
        <span class='kb-badge-primary'>TF-IDF / NLP</span>
    </div>
    """, unsafe_allow_html=True)
    card_close()

    card_open("Commercial Roadmap")
    alert_card("Revenue at Risk Module", "Connect churn probability to MRR impact per customer.", "info")
    alert_card("CRM Integrations", "Native connectors for Salesforce, HubSpot, and Stripe.", "info")
    alert_card("Next Best Action Engine", "LLM-powered retention email drafts per customer.", "info")
    card_close()

show_footer()
