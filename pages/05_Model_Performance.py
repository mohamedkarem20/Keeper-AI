import streamlit as st
import pandas as pd
import json
from pathlib import Path
from sklearn.metrics import roc_curve, confusion_matrix
import plotly.express as px
import plotly.graph_objects as go

from components.sidebar import show_sidebar
from components.footer import show_footer

st.set_page_config(page_title="Model Performance", page_icon="📈", layout="wide")

def load_css():
    css_path = Path(__file__).parent.parent / "assets" / "style.css"
    try:
        with open(css_path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

def show_page_header(title, subtitle):
    st.markdown(f"""
    <div class="page-hero">
        <h1 class="hero-title">{title}</h1>
        <p class="hero-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

@st.cache_data
def load_model_metadata():
    meta_path = Path(__file__).parent.parent / "outputs" / "model_metadata.json"
    if meta_path.exists():
        with open(meta_path, "r") as f:
            return json.load(f)
    return {}

@st.cache_data
def load_test_predictions():
    preds_path = Path(__file__).parent.parent / "outputs" / "test_set_predictions.csv"
    if preds_path.exists():
        return pd.read_csv(preds_path)
    return pd.DataFrame()

def get_chart_layout(title="", height=360):
    return dict(
        title=dict(text=title, font=dict(family="Space Grotesk", size=14, color="#0F172A")),
        paper_bgcolor="white",
        plot_bgcolor="rgba(248,250,252,0.5)",
        font=dict(family="Inter", size=12, color="#475569"),
        margin=dict(l=10, r=10, t=40, b=10),
        height=height,
        showlegend=True,
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)"),
    )

def roc_curve_chart(y_true, y_prob):
    try:
        from components.charts import roc_curve_chart as rcc
        return rcc(y_true, y_prob)
    except ImportError:
        fpr, tpr, _ = roc_curve(y_true, y_prob)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=fpr, y=tpr, name="ROC Curve", mode='lines', line=dict(color="#2563EB", width=2)))
        fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], name="Random Guess", mode='lines', line=dict(color="#94A3B8", width=2, dash='dash')))
        fig.update_layout(**get_chart_layout("ROC Curve"))
        fig.update_xaxes(title="False Positive Rate")
        fig.update_yaxes(title="True Positive Rate")
        return fig

def confusion_matrix_chart(y_true, y_pred):
    try:
        from components.charts import confusion_matrix_chart as cmc
        return cmc(y_true, y_pred)
    except ImportError:
        cm = confusion_matrix(y_true, y_pred)
        fig = px.imshow(cm, text_auto=True, color_continuous_scale="Blues", aspect="auto")
        fig.update_layout(**get_chart_layout("Confusion Matrix"))
        fig.update_xaxes(title="Predicted Label", tickvals=[0, 1], ticktext=["No Churn", "Churn"])
        fig.update_yaxes(title="True Label", tickvals=[0, 1], ticktext=["No Churn", "Churn"])
        return fig

def main():
    load_css()
    show_sidebar()
    
    show_page_header("📈 Model Performance", "XGBoost evaluation metrics")
    
    metadata = load_model_metadata()
    test_preds = load_test_predictions()
    
    if not metadata and test_preds.empty:
        st.markdown("<div class='empty-state'>Model performance data is not available. Please run model training first.</div>", unsafe_allow_html=True)
        show_footer()
        return
        
    metrics = metadata.get("test_metrics", {})
    
    st.markdown(f"""
    <div style='display: flex; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap;'>
        <div class="kpi-card blue" style='flex: 1; min-width: 150px;'>
            <div class="kpi-label">Accuracy</div>
            <div class="kpi-value">{metrics.get('Accuracy', 0):.3f}</div>
        </div>
        <div class="kpi-card green" style='flex: 1; min-width: 150px;'>
            <div class="kpi-label">ROC AUC</div>
            <div class="kpi-value">{metrics.get('ROC_AUC', 0):.3f}</div>
        </div>
        <div class="kpi-card purple" style='flex: 1; min-width: 150px;'>
            <div class="kpi-label">Precision</div>
            <div class="kpi-value">{metrics.get('Precision', 0):.3f}</div>
        </div>
        <div class="kpi-card orange" style='flex: 1; min-width: 150px;'>
            <div class="kpi-label">Recall</div>
            <div class="kpi-value">{metrics.get('Recall', 0):.3f}</div>
        </div>
        <div class="kpi-card red" style='flex: 1; min-width: 150px;'>
            <div class="kpi-label">F1-Score</div>
            <div class="kpi-value">{metrics.get('F1', 0):.3f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not test_preds.empty and 'y_true' in test_preds.columns:
        col1, col2 = st.columns(2)
        
        y_true = test_preds['y_true']
        
        y_prob = None
        if 'y_prob' in test_preds.columns:
            y_prob = test_preds['y_prob']
        elif 'churn_probability' in test_preds.columns:
            y_prob = test_preds['churn_probability']
            
        y_pred = None
        if 'y_pred' in test_preds.columns:
            y_pred = test_preds['y_pred']
        elif 'churn_prediction' in test_preds.columns:
            y_pred = test_preds['churn_prediction']
            
        with col1:
            if y_prob is not None:
                fig_roc = roc_curve_chart(y_true, y_prob)
                st.plotly_chart(fig_roc, use_container_width=True)
            else:
                st.info("Probability predictions not found for ROC Curve.")
                
        with col2:
            if y_pred is not None:
                fig_cm = confusion_matrix_chart(y_true, y_pred)
                st.plotly_chart(fig_cm, use_container_width=True)
            else:
                st.info("Binary predictions not found for Confusion Matrix.")
    else:
        st.info("Test set predictions missing required columns (y_true, y_prob, y_pred).")
        
    show_footer()

if __name__ == "__main__":
    main()
