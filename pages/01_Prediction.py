"""
01_Prediction.py - Keeper AI | Customer Churn Prediction
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="Prediction | Keeper AI", page_icon="🔮", layout="wide")

def _load_css():
    css = Path(__file__).parent.parent / "assets" / "style.css"
    try: st.markdown(f"<style>{css.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
    except FileNotFoundError: pass
_load_css()

from components.sidebar import show_sidebar
from components.header  import show_page_header
from components.footer  import show_footer
from components.cards   import card_open, card_close, alert_card, kpi_card
from utils.predictor    import predict_customer

if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

show_sidebar()
show_page_header("Customer Risk Prediction",
    "Input customer data and support text to generate a real-time churn probability score.",
    icon="🔮")

col_form, col_results = st.columns([0.45, 0.55], gap="large")

with col_form:
    card_open("Customer Profile Form")
    with st.form("prediction_form"):
        st.markdown("<div style='font-size:13px;font-weight:600;color:#334155;margin-bottom:8px;'>Demographics & Account</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            age          = st.number_input("Age", min_value=18, max_value=100, value=35)
            gender       = st.selectbox("Gender", ["Male", "Female", "Other"])
            country      = st.selectbox("Country", ["USA", "UK", "Germany", "France", "Spain"])
        with c2:
            subscription = st.selectbox("Subscription", ["Basic", "Standard", "Premium"])
            tenure       = st.number_input("Tenure (Months)", min_value=0, value=12)

        st.markdown("<hr style='margin:16px 0;border:none;border-top:1px solid #E2E8F0;'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:13px;font-weight:600;color:#334155;margin-bottom:8px;'>Usage & Financials</div>", unsafe_allow_html=True)
        u1, u2 = st.columns(2)
        with u1:
            usage_freq    = st.selectbox("Usage Frequency", ["Daily", "Weekly", "Monthly"])
            support_calls = st.number_input("Support Calls", min_value=0, value=1)
        with u2:
            spend = st.number_input("Total Spend ($)", min_value=0.0, value=500.0)
            delay = st.number_input("Payment Delay (Days)", min_value=0, value=0)

        st.markdown("<hr style='margin:16px 0;border:none;border-top:1px solid #E2E8F0;'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:13px;font-weight:600;color:#334155;margin-bottom:8px;'>NLP Analysis</div>", unsafe_allow_html=True)
        review_text = st.text_area("Customer Interaction / Review Text",
            value="The service is okay but I experienced downtime last week which was frustrating.",
            height=100)

        submitted = st.form_submit_button("🚀  Run Prediction Engine", type="primary", use_container_width=True)
    card_close()

with col_results:
    if submitted:
        input_data = {
            "Age": age,
            "Gender": gender,
            "Country": country,
            "Location": country,
            "Subscription_Length_Months": tenure,
            "Monthly_Bill": spend / max(tenure, 1),
            "Total_Usage_GB": 50.0,
            "Customer_Support_Contacts": support_calls,
            "Payment_Delay_Days": delay,
            "Usage_Frequency": usage_freq,
            "Subscription_Type": subscription,
            "Days_Since_Last_Purchase": max(tenure * 30, 0),
            "Purchase_Count": 1 if usage_freq == "Monthly" else 2 if usage_freq == "Weekly" else 3,
            "Total_Spent": spend,
            "Resolution_Time_Hours": max(delay + 1, 1),
            "Review_Text": review_text
        }
        try:
            with st.spinner("Running prediction engine..."):
                result = predict_customer(input_data)
            prob = result.get("probability", 0) * 100

            if prob >= 70:
                risk_label, risk_color, sev = "Critical Risk",  "#EF4444", "danger"
            elif prob >= 40:
                risk_label, risk_color, sev = "Moderate Risk",  "#F59E0B", "warning"
            else:
                risk_label, risk_color, sev = "Healthy",        "#10B981", "success"

            st.session_state.prediction_history.append({
                "Time": datetime.now().strftime("%H:%M:%S"),
                "Country": country, "Spend": f"${spend:,.2f}",
                "Probability": f"{prob:.1f}%", "Status": risk_label
            })

            card_open("Prediction Result")
            r1, r2 = st.columns([0.45, 0.55])
            with r1:
                st.markdown(f"""
                <div style='text-align:center;padding:20px 0;'>
                    <div style='font-size:11px;font-weight:700;color:#94A3B8;
                                text-transform:uppercase;letter-spacing:0.08em;margin-bottom:12px;'>Risk Status</div>
                    <div style='background:{risk_color}18;color:{risk_color};
                                padding:10px 20px;border-radius:9999px;font-weight:700;
                                font-size:18px;border:1px solid {risk_color}30;'>{risk_label}</div>
                    <div style='font-size:42px;font-weight:800;color:{risk_color};
                                margin-top:16px;letter-spacing:-0.04em;font-family:Outfit,sans-serif;'>{prob:.1f}%</div>
                    <div style='font-size:12px;color:#94A3B8;margin-top:4px;'>Churn Probability</div>
                </div>
                """, unsafe_allow_html=True)
            with r2:
                try:
                    import plotly.graph_objects as go
                    gauge = go.Figure(go.Indicator(
                        mode="gauge+number", value=prob,
                        number=dict(suffix="%", font=dict(family="Outfit", size=28, color="#0F172A")),
                        gauge=dict(
                            axis=dict(range=[0, 100], showticklabels=False),
                            bar=dict(color=risk_color, thickness=0.28),
                            bgcolor="#F8FAFC", borderwidth=0,
                            steps=[dict(range=[0,40],color="#ECFDF5"),
                                   dict(range=[40,70],color="#FFFBEB"),
                                   dict(range=[70,100],color="#FEF2F2")]
                        )
                    ))
                    gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                                        margin=dict(l=10,r=10,t=20,b=10), height=200)
                    st.plotly_chart(gauge, use_container_width=True, config={"displayModeBar":False})
                except ImportError:
                    st.metric("Churn Probability", f"{prob:.1f}%")
            card_close()

            card_open("AI Recommendations")
            if sev == "danger":
                alert_card("Immediate Outreach Required",
                    "Churn probability >70%. Assign to Tier 2 retention specialist with a 15% discount offer.",
                    "danger")
            elif sev == "warning":
                alert_card("Monitor Account Closely",
                    "Moderate risk detected. Enroll in proactive check-in email sequence and offer a free training webinar.",
                    "warning")
            else:
                alert_card("Customer Appears Healthy",
                    "Continue standard automated marketing and billing cycles.", "success")
            if result.get("sentiment_score") is not None:
                s = result["sentiment_score"]
                sl = "Negative" if s < -0.2 else ("Positive" if s > 0.2 else "Neutral")
                alert_card("NLP Sentiment", f"Detected {sl} sentiment ({s:.2f}) from the review text.", "info")
            card_close()

        except Exception as e:
            st.error(f"Prediction Error: {e}")
    else:
        st.markdown("""
        <div style='display:flex;flex-direction:column;align-items:center;justify-content:center;
                    min-height:400px;background:white;border-radius:16px;
                    border:1.5px dashed #E2E8F0;text-align:center;'>
            <div style='font-size:52px;margin-bottom:16px;'>🤖</div>
            <div style='font-family:Outfit,sans-serif;font-size:20px;font-weight:700;
                        color:#0F172A;margin-bottom:8px;'>Awaiting Input</div>
            <div style='font-size:14px;color:#64748B;max-width:280px;'>
                Fill the customer profile form and click predict.</div>
        </div>
        """, unsafe_allow_html=True)

if st.session_state.prediction_history:
    st.write("")
    card_open("Session History")
    df_h = pd.DataFrame(st.session_state.prediction_history).tail(5)[::-1]
    st.dataframe(df_h, use_container_width=True, hide_index=True)
    card_close()

show_footer()
