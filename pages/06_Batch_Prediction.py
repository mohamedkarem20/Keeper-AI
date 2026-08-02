import streamlit as st
import pandas as pd
from pathlib import Path
import time

from components.sidebar import show_sidebar
from components.footer import show_footer
from utils.predictor import predict_customer

st.set_page_config(page_title="Batch Prediction - Churn AI", page_icon="📁", layout="wide")

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

load_css()
show_sidebar()

show_page_header("📁 Batch Prediction", "Score multiple customers at once")

st.markdown("""
<div class="card">
    <div class="card-header">
        <h3 class="card-title">Upload Customer Data</h3>
    </div>
    <div class="upload-info-card" style="padding: 1rem; background-color: #F8FAFC; border-radius: 8px; margin-bottom: 1rem; color: #334155; font-family: 'Inter', sans-serif;">
        <strong>Required Columns:</strong> Age, Gender, Country, Customer_Support_Contacts, Days_Since_Last_Purchase, Purchase_Count, Total_Spent, Resolution_Time_Hours, Review_Text. CSV or Excel (.xlsx) files are accepted.
    </div>
</div>
""", unsafe_allow_html=True)

REQUIRED_COLUMNS = [
    "Age", "Gender", "Country", "Customer_Support_Contacts",
    "Days_Since_Last_Purchase", "Purchase_Count", "Total_Spent",
    "Resolution_Time_Hours", "Review_Text",
]

uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        filename = uploaded_file.name.lower()
        if filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)

        # Normalize headers: strip stray whitespace and match required
        # columns case-insensitively, so a file with e.g. "resolution_time_hours "
        # or "resolution_time_hours" still lines up with what the model expects.
        df.columns = [str(c).strip() for c in df.columns]
        lookup = {c.lower(): c for c in df.columns}
        rename_map = {}
        for req_col in REQUIRED_COLUMNS:
            match = lookup.get(req_col.lower())
            if match and match != req_col:
                rename_map[match] = req_col
        if rename_map:
            df = df.rename(columns=rename_map)

        st.write(f"**Loaded {len(df)} rows.**")

        missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        if missing_cols:
            st.error(
                "Your file is missing the following required column(s): "
                f"**{', '.join(missing_cols)}**. Please add them and re-upload. "
                f"Required columns: {', '.join(REQUIRED_COLUMNS)}."
            )
            st.caption(f"Columns detected in your file: {', '.join(df.columns)}")
        elif st.button("Run Batch Prediction", type="primary"):
            progress_text = "Scoring customers..."
            my_bar = st.progress(0, text=progress_text)

            try:
                results = []
                for i, row in df.iterrows():
                    customer_data = row.to_dict()
                    pred_result = predict_customer(customer_data)

                    res_row = customer_data.copy()
                    res_row["Churn_Probability"] = pred_result["probability"]
                    res_row["Churn_Prediction"] = pred_result["prediction"]
                    res_row["Risk_Level"] = pred_result["risk_level"]
                    results.append(res_row)

                    progress = int((i + 1) / len(df) * 100)
                    if progress > 100: progress = 100
                    my_bar.progress(progress, text=f"{progress_text} ({i+1}/{len(df)})")

                time.sleep(0.5)
            finally:
                my_bar.empty()

            results_df = pd.DataFrame(results)

            st.markdown("### Prediction Results")
            st.dataframe(results_df, use_container_width=True)

            csv = results_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Results as CSV",
                data=csv,
                file_name='batch_predictions.csv',
                mime='text/csv',
            )

    except Exception as e:
        st.error(f"Error processing file: {e}")

show_footer()
