"""
Data Loader Utilities — Customer Churn Intelligence Platform
All data loading functions with @st.cache_data for performance.
"""

import json
import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"


@st.cache_data(show_spinner=False)
def load_model_metadata() -> dict:
    """Load model metadata JSON."""
    try:
        with open(OUTPUTS_DIR / "model_metadata.json", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


@st.cache_data(show_spinner=False)
def load_dataset() -> pd.DataFrame | None:
    """Load the engineered dataset CSV (cached)."""
    path = OUTPUTS_DIR / "engineered_dataset.csv"
    if not path.exists():
        return None
    try:
        df = pd.read_csv(path, low_memory=False)
        return df
    except Exception:
        return None


@st.cache_data(show_spinner=False)
def load_test_predictions() -> pd.DataFrame | None:
    """Load test set predictions CSV."""
    path = OUTPUTS_DIR / "test_set_predictions.csv"
    if not path.exists():
        return None
    try:
        return pd.read_csv(path)
    except Exception:
        return None


@st.cache_data(show_spinner=False)
def load_shap_global() -> pd.DataFrame | None:
    """Load SHAP global feature importance CSV."""
    path = OUTPUTS_DIR / "shap_global_importance.csv"
    if not path.exists():
        return None
    try:
        df = pd.read_csv(path)
        # Normalize column names
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception:
        return None


@st.cache_data(show_spinner=False)
def load_shap_sample():
    """Load SHAP sample values (.npy) and feature names CSV."""
    npy_path = OUTPUTS_DIR / "shap_values_sample.npy"
    feat_path = OUTPUTS_DIR / "shap_sample_features.csv"
    try:
        shap_values = np.load(str(npy_path))
        features_df = pd.read_csv(feat_path)
        return shap_values, features_df
    except Exception:
        return None, None


def detect_target_column(df: pd.DataFrame) -> str | None:
    """Try to find the churn target column in a DataFrame."""
    candidates = ["Churned", "Churn", "churn", "churned", "Target", "target",
                  "label", "Label", "is_churn", "Is_Churn"]
    for c in candidates:
        if c in df.columns:
            return c
    # Try partial match
    for c in df.columns:
        if "churn" in c.lower():
            return c
    return None


def get_metric(metadata: dict, key: str, default=None):
    """Safely get a metric from model metadata."""
    return metadata.get("test_metrics", {}).get(key, default)
