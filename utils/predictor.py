import pandas as pd
import numpy as np

from utils.model_loader import (
    get_model,
    get_preprocessor,
    get_tfidf,
    get_metadata
)


model = get_model()
preprocessor = get_preprocessor()
tfidf_vectorizer = get_tfidf()
metadata = get_metadata()


FINAL_FEATURES = metadata["final_features"]


def create_engineered_features(df):
    """
    Create the same engineered features used during training
    """

    # Avoid division by zero
    df["Contacts_x_ResolutionTime"] = (
        df["Customer_Support_Contacts"]
        *
        df["Resolution_Time_Hours"]
    )


    df["Resolution_Delay_Ratio"] = (
        df["Resolution_Time_Hours"]
        /
        (df["Days_Since_Last_Purchase"] + 1)
    )


    df["Support_Efficiency_Score"] = (
        df["Customer_Support_Contacts"]
        /
        (df["Resolution_Time_Hours"] + 1)
    )


    return df



def add_tfidf_features(df):

    """
    Convert text into TF-IDF features
    """

    text = df["Review_Text"].fillna("")


    tfidf_matrix = tfidf_vectorizer.transform(text)


    tfidf_columns = [
        f"tfidf_{word.replace(' ', '_')}"
        for word in tfidf_vectorizer.get_feature_names_out()
    ]


    tfidf_df = pd.DataFrame(
        tfidf_matrix.toarray(),
        columns=tfidf_columns,
        index=df.index
    )


    df = pd.concat(
        [
            df.drop(columns=["Review_Text"]),
            tfidf_df
        ],
        axis=1
    )
    return df



def predict_customer(customer_data):

    """
    Main prediction function

    Input:
        dictionary

    Output:
        churn prediction + probability
    """


    df = pd.DataFrame([customer_data])


    # Feature Engineering
    df = create_engineered_features(df)


    # TF-IDF
    df = add_tfidf_features(df)


    # Keep only training features order
    df = df.reindex(
        columns=FINAL_FEATURES,
        fill_value=0
    )


    # Preprocessing
    X_processed = preprocessor.transform(df)


    # Prediction probability
    probability = model.predict_proba(
        X_processed
    )[0][1]


    prediction = int(probability >= 0.5)

    if probability >= 0.70:
        risk_level = "Critical Risk"
    elif probability >= 0.40:
        risk_level = "Moderate Risk"
    else:
        risk_level = "Healthy"

    return {
        "prediction": prediction,
        "probability": round(float(probability),4),
        "label": "Churn" if prediction == 1 else "Not Churn",
        "risk_level": risk_level
    }
