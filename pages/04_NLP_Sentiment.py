import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

os.environ.setdefault("PYTHONSAFEPATH", "1")
# NLTK >= 3.10 installs a MetaPathFinder that blocks any import it thinks
# comes from the current working directory (CWE-427 mitigation). Because
# .venv lives *inside* this project folder, everything under
# .venv/Lib/site-packages (including NLTK's own 'regex' dependency) is
# technically "inside" the cwd, so the finder false-positives and blocks it.
# Disabling it here is safe: this app doesn't rely on that protection.
os.environ.setdefault("NLTK_DISABLE_IMPORT_SECURITY", "1")

try:
    import nltk
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
except Exception as exc:  # pragma: no cover - defensive import guard
    nltk = None
    SentimentIntensityAnalyzer = None
    NLTK_IMPORT_ERROR = exc
else:
    NLTK_IMPORT_ERROR = None

from components.sidebar import show_sidebar
from components.footer import show_footer

st.set_page_config(page_title="NLP Sentiment Analysis", page_icon="💬", layout="wide")

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
DATASET_PATH = OUTPUTS_DIR / "engineered_dataset.csv"


def load_css():
    css_path = BASE_DIR / "assets" / "style.css"
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

@st.cache_data(show_spinner=False)
def load_dataset() -> pd.DataFrame:
    if DATASET_PATH.exists():
        try:
            df = pd.read_csv(DATASET_PATH)
        except Exception:
            return pd.DataFrame()
        if "Review_Text" in df.columns:
            return df[df["Review_Text"].notna() & (df["Review_Text"].astype(str).str.strip() != "")].copy()
    return pd.DataFrame()


@st.cache_resource(show_spinner=False)
def get_sentiment_analyzer():
    if nltk is None or SentimentIntensityAnalyzer is None:
        raise RuntimeError(f"NLTK could not be imported: {NLTK_IMPORT_ERROR}")

    try:
        nltk.data.find("sentiment/vader_lexicon.zip")
    except LookupError:
        try:
            nltk.download("vader_lexicon", quiet=True)
        except Exception as download_error:
            raise RuntimeError(f"Unable to download VADER lexicon: {download_error}") from download_error

    return SentimentIntensityAnalyzer()


def main():
    load_css()
    show_sidebar()
    
    show_page_header("💬 NLP Sentiment Analysis", "Analyze customer review text")
    
    df = load_dataset()
    if df.empty or "Review_Text" not in df.columns:
        st.info("No review text data is available for sentiment analysis yet.")
        show_footer()
        return

    if NLTK_IMPORT_ERROR is not None:
        st.error(f"NLTK is unavailable in this environment: {NLTK_IMPORT_ERROR}")
        show_footer()
        return

    try:
        sia = get_sentiment_analyzer()
    except Exception as exc:
        st.error(f"Unable to initialize NLP resources: {exc}")
        show_footer()
        return

    # Sample up to 500 reviews
    sample_df = df.sample(n=min(500, len(df)), random_state=42).copy()

    # Calculate sentiment
    sample_df['Sentiment_Scores'] = sample_df['Review_Text'].apply(lambda x: sia.polarity_scores(str(x)))
    sample_df['Compound_Score'] = sample_df['Sentiment_Scores'].apply(lambda x: x['compound'])
    sample_df['Sentiment_Label'] = pd.cut(sample_df['Compound_Score'], bins=[-1.1, -0.05, 0.05, 1.1], labels=['Negative', 'Neutral', 'Positive'])
    
    avg_sentiment = sample_df['Compound_Score'].mean()
    pos_pct = (sample_df['Sentiment_Label'] == 'Positive').mean() * 100
    neg_pct = (sample_df['Sentiment_Label'] == 'Negative').mean() * 100
    
    st.markdown(f"""
    <div style='display: flex; gap: 1rem; margin-bottom: 2rem;'>
        <div class="kpi-card blue sentiment-card sentiment-neutral" style='flex: 1;'>
            <div class="kpi-label">Average Sentiment</div>
            <div class="kpi-value">{avg_sentiment:.2f}</div>
        </div>
        <div class="kpi-card green sentiment-card sentiment-positive" style='flex: 1;'>
            <div class="kpi-label">Positive Reviews</div>
            <div class="kpi-value">{pos_pct:.1f}%</div>
        </div>
        <div class="kpi-card red sentiment-card sentiment-negative" style='flex: 1;'>
            <div class="kpi-label">Negative Reviews</div>
            <div class="kpi-value">{neg_pct:.1f}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 class='section-title'>Sentiment Score Distribution</h3>", unsafe_allow_html=True)
    
    fig = px.histogram(
        sample_df, 
        x="Compound_Score", 
        color="Sentiment_Label",
        color_discrete_map={"Negative": "#EF4444", "Neutral": "#F59E0B", "Positive": "#22C55E"},
        nbins=20,
        title="Distribution of Sentiment Scores"
    )
    
    fig.update_layout(
        title=dict(font=dict(family="Space Grotesk", size=14, color="#0F172A")),
        paper_bgcolor="white",
        plot_bgcolor="rgba(248,250,252,0.5)",
        font=dict(family="Inter", size=12, color="#475569"),
        margin=dict(l=10, r=10, t=40, b=10),
        height=360,
        showlegend=True,
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)"),
        xaxis_title="Compound Sentiment Score",
        yaxis_title="Count"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<h3 class='section-title'>Recent Negative Reviews</h3>", unsafe_allow_html=True)
    
    negative_reviews = sample_df[sample_df['Compound_Score'] < -0.05].sort_values(by='Compound_Score').head(5)
    
    if not negative_reviews.empty:
        table_html = "<table class='styled-table'><thead><tr><th>Score</th><th>Review Text</th></tr></thead><tbody>"
        for _, row in negative_reviews.iterrows():
            table_html += f"<tr><td><span class='badge-danger'>{row['Compound_Score']:.2f}</span></td><td>{row['Review_Text']}</td></tr>"
        table_html += "</tbody></table>"
        st.markdown(table_html, unsafe_allow_html=True)
    else:
        st.markdown("<p>No negative reviews found in the sample.</p>", unsafe_allow_html=True)
        
    show_footer()

if __name__ == "__main__":
    main()
