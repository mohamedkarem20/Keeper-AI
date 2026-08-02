"""
03_Explainability.py - Keeper AI | SHAP Explainability
"""
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Explain AI | Keeper AI", page_icon="🧠", layout="wide")

def _load_css():
    css = Path(__file__).parent.parent / "assets" / "style.css"
    try: st.markdown(f"<style>{css.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
    except FileNotFoundError: pass
_load_css()

from components.sidebar import show_sidebar
from components.header  import show_page_header
from components.footer  import show_footer
from components.cards   import card_open, card_close, alert_card
from utils.data_loader  import load_dataset

show_sidebar()
show_page_header("Model Explainability (SHAP)",
    "Understand the why behind every prediction — at both global and individual levels.",
    icon="🧠")

st.markdown("<h3 style='font-family:Outfit,sans-serif;font-size:17px;color:#0F172A;margin-bottom:16px;'>Global Feature Drivers</h3>", unsafe_allow_html=True)

g1, g2 = st.columns([0.42, 0.58])

with g1:
    card_open("Global Feature Importance")
    features   = ["Monthly_Bill","Age","Support_Contacts","Total_Usage_GB","Tenure","Gender_Male"]
    importance = [1.25, 0.95, 0.85, 0.45, 0.35, 0.15]
    colors     = ["#4338CA","#4338CA","#4338CA","#8B5CF6","#8B5CF6","#06B6D4"]
    fig = px.bar(x=importance, y=features, orientation='h',
                 color=features, color_discrete_sequence=colors, template="simple_white")
    fig.update_layout(margin=dict(l=0,r=0,t=10,b=0), height=320,
                      paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
                      yaxis={'categoryorder':'total ascending'},
                      xaxis_title="Mean |SHAP Value|")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    card_close()

with g2:
    card_open("SHAP Summary Plot")
    st.markdown("""
    <div style='background:#F8FAFC;border:1.5px dashed #E2E8F0;border-radius:12px;
                height:320px;display:flex;align-items:center;justify-content:center;
                flex-direction:column;gap:10px;'>
        <span style='font-size:42px;'>📊</span>
        <span style='color:#64748B;font-weight:600;font-size:14px;'>SHAP Beeswarm Summary Plot</span>
        <span style='color:#94A3B8;font-size:12.5px;text-align:center;max-width:340px;'>
            Pass your <code>shap.summary_plot()</code> figure using <code>st.pyplot(fig)</code> here.</span>
    </div>
    """, unsafe_allow_html=True)
    card_close()

st.markdown("<hr style='border:none;border-top:1px solid #F1F5F9;margin:28px 0;'>", unsafe_allow_html=True)
st.markdown("<h3 style='font-family:Outfit,sans-serif;font-size:17px;color:#0F172A;margin-bottom:16px;'>Single Prediction Explanation</h3>", unsafe_allow_html=True)

try:
    df = load_dataset()
    if df is not None and not df.empty and 'Customer_ID' in df.columns:
        sel_col, _ = st.columns([0.3, 0.7])
        with sel_col:
            cid = st.selectbox("Select Customer to Analyze", df['Customer_ID'].head(50).tolist())

        l1, l2 = st.columns([0.65, 0.35])
        with l1:
            card_open(f"SHAP Waterfall — Customer {cid}")
            base  = -0.5
            feats = ["Tenure=12","Monthly_Bill=120","Age=35","Support_Calls=4"]
            sv    = [-0.8, 1.2, -0.2, 0.9]
            fig_wf = go.Figure(go.Waterfall(
                orientation="h", measure=["relative"]*len(feats),
                x=sv, y=feats, base=base,
                decreasing={"marker":{"color":"#10B981"}},
                increasing={"marker":{"color":"#EF4444"}},
            ))
            fig_wf.update_layout(
                margin=dict(l=0,r=0,t=10,b=0), height=320,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
                yaxis=dict(autorange="reversed")
            )
            st.plotly_chart(fig_wf, use_container_width=True, config={"displayModeBar":False})
            card_close()

        with l2:
            card_open("Reading the Chart")
            alert_card("Base Value", "Average churn probability across the full training dataset.", "info")
            alert_card("Red Bars (Risk Drivers)", "Features pushing this customer's probability higher.", "danger")
            alert_card("Green Bars (Retention)", "Features keeping this customer's probability lower.", "success")
            card_close()
except Exception as e:
    st.warning(f"Could not load dataset: {e}")

show_footer()
