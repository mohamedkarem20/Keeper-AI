import streamlit as st
import pandas as pd
from pathlib import Path

from components.sidebar import show_sidebar
from components.footer import show_footer
from components.header import show_page_header
from components.metrics import kpi_row
from components.charts import donut_chart, bar_chart
from utils.data_loader import load_dataset, detect_target_column

st.set_page_config(page_title="Customer Analytics", page_icon="📊", layout="wide")

def load_css():
    css_path = Path(__file__).parent.parent / "assets" / "style.css"
    try:
        with open(css_path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css()
show_sidebar()

show_page_header("📊 Customer Analytics", "Dataset exploration and churn drivers")

df = load_dataset()

if df is None:
    st.markdown('<div class="empty-state">No dataset available. Please ensure data is loaded.</div>', unsafe_allow_html=True)
else:
    df = df.dropna()
    target_col = detect_target_column(df) or "Churned"
    if target_col not in df.columns:
        # Fallback if no target col found
        df[target_col] = 0
    
    # Calculate KPIs
    total_customers = len(df)
    churn_rate = float(df[target_col].mean()) if target_col in df.columns else 0.0
    
    tenure_col = next((c for c in ["Days_Since_Last_Purchase", "Tenure", "Purchase_Count"] if c in df.columns), None)
    tenure_label = "Avg Days Active" if tenure_col == "Days_Since_Last_Purchase" else "Avg Purchases" if tenure_col == "Purchase_Count" else "Avg Tenure"
    avg_tenure = float(df[tenure_col].mean()) if tenure_col else 0.0
    
    metrics = [
        {"label": "Total Customers", "value": f"{total_customers:,}", "icon": "👥", "color": "blue"},
        {"label": "Churn Rate", "value": f"{churn_rate:.1%}", "icon": "⚠️", "color": "red"},
        {"label": tenure_label, "value": f"{avg_tenure:.1f}", "icon": "📅", "color": "green"}
    ]
    kpi_row(metrics)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    cat_col = next((c for c in ["Country", "Subscription_Type", "Gender"] if c in df.columns), None)
    with col1:
        if cat_col and target_col in df.columns:
            churn_counts = df[df[target_col] == 1][cat_col].value_counts()
            if churn_counts.empty:
                churn_counts = df[cat_col].value_counts()
            fig1 = donut_chart(
                labels=churn_counts.index.astype(str).tolist(), 
                values=churn_counts.values.tolist(), 
                title=f"Churn Distribution by {cat_col.replace('_', ' ')}"
            )
            st.plotly_chart(fig1, use_container_width=True)
            
    with col2:
        if tenure_col and target_col in df.columns:
            try:
                df["Tenure_Group"] = pd.qcut(df[tenure_col], q=4, duplicates="drop").astype(str)
                churn_by_tenure = df.groupby("Tenure_Group", observed=False)[target_col].mean().reset_index()
                fig2 = bar_chart(
                    x=churn_by_tenure["Tenure_Group"].astype(str), 
                    y=churn_by_tenure[target_col], 
                    title=f"Churn Rate by {tenure_label} Quartiles", 
                    xaxis_title=tenure_label, 
                    yaxis_title="Churn Rate"
                )
                st.plotly_chart(fig2, use_container_width=True)
            except Exception:
                pass
            
    col3, col4 = st.columns(2)
    
    with col3:
        if "Customer_Support_Contacts" in df.columns and target_col in df.columns:
            churn_by_support = df.groupby("Customer_Support_Contacts")[target_col].mean().reset_index()
            fig3 = bar_chart(
                x=churn_by_support["Customer_Support_Contacts"].astype(str), 
                y=churn_by_support[target_col], 
                title="Support Contacts vs Churn Rate", 
                xaxis_title="Support Contacts", 
                yaxis_title="Churn Rate"
            )
            st.plotly_chart(fig3, use_container_width=True)

show_footer()
