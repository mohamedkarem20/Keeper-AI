import json
import joblib

from config import (
    MODEL_PATH,
    PREPROCESSOR_PATH,
    TFIDF_PATH,
    METADATA_PATH,
)


# ==========================
# Load Artifacts
# ==========================

model = joblib.load(MODEL_PATH)

preprocessor = joblib.load(PREPROCESSOR_PATH)

tfidf_vectorizer = joblib.load(TFIDF_PATH)


with open(METADATA_PATH, "r") as f:
    metadata = json.load(f)


# ==========================
# Getter Functions
# ==========================

def get_model():
    return model


def get_preprocessor():
    return preprocessor


def get_tfidf():
    return tfidf_vectorizer


def get_metadata():
    return metadata