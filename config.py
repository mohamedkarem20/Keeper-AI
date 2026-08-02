from pathlib import Path

# ===========================
# Project Paths
# ===========================

BASE_DIR = Path(__file__).resolve().parent

OUTPUTS_DIR = BASE_DIR / "outputs"
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"


# ===========================
# Model Files
# ===========================

MODEL_PATH = OUTPUTS_DIR / "final_model.joblib"

PREPROCESSOR_PATH = OUTPUTS_DIR / "preprocessor.joblib"

TFIDF_PATH = OUTPUTS_DIR / "tfidf_vectorizer.joblib"

METADATA_PATH = OUTPUTS_DIR / "model_metadata.json"


# ===========================
# Application Settings
# ===========================

DEFAULT_THRESHOLD = 0.50