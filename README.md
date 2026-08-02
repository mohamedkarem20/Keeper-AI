# 🚀 Keeper-AI

## AI-Powered Customer Churn Prediction Platform

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-green)
![NLP](https://img.shields.io/badge/NLP-TF--IDF-orange)
![Streamlit](https://img.shields.io/badge/App-Streamlit-red)
![Status](https://img.shields.io/badge/Project-Production%20Ready-success)

---

# 📌 Overview

**Keeper-AI** is an end-to-end Artificial Intelligence platform designed to predict customer churn, analyze customer behavior, and provide actionable business retention strategies.

The platform combines:

* Machine Learning
* Natural Language Processing (NLP)
* Explainable AI (XAI)
* Interactive Analytics Dashboard

to transform raw customer data into intelligent business decisions.

---

# 🎯 Business Problem

Customer churn is one of the biggest challenges facing modern businesses, especially in:

* E-commerce platforms
* Subscription services
* Customer-based applications

Losing customers affects:

* Revenue
* Customer Lifetime Value (CLV)
* Business growth

Keeper-AI provides an intelligent solution to answer:

* Which customers are most likely to leave?
* What factors influence customer churn?
* Why did the model classify a customer as risky?
* What retention actions should businesses take?

---

# 💡 Project Objectives

The main goals of Keeper-AI are:

✅ Predict customer churn probability
✅ Identify high-risk customers
✅ Explain model decisions
✅ Analyze customer sentiment
✅ Provide data-driven retention recommendations

---

# 🏗️ System Architecture

```
                 Customer Data
                       |
                       ↓
            Data Processing Layer
                       |
                       ↓
          Feature Engineering Pipeline
                       |
                       ↓
             Feature Selection
                       |
                       ↓
          Machine Learning Models
                       |
        --------------------------------
        |                              |
        ↓                              ↓
 Churn Prediction              Explainable AI
        |
        ↓
 Customer Analytics Dashboard
        |
        ↓
 Retention Recommendations
```

---

# 🔄 Machine Learning Pipeline

## 1. Data Preparation

Performed:

* Data cleaning
* Missing value handling
* Data transformation
* Categorical encoding
* Data validation

---

## 2. Exploratory Data Analysis (EDA)

Analyzed:

* Customer behavior patterns
* Purchase activity
* Churn distribution
* Feature relationships
* Customer segments

---

## 3. Feature Engineering

Created meaningful features related to:

* Customer engagement
* Purchase behavior
* Customer activity
* Retention indicators

---

## 4. Feature Selection

Applied multiple feature selection techniques:

* Mutual Information
* Chi-Square Test
* ANOVA F-Test
* Random Forest Feature Importance
* Recursive Feature Elimination (RFE)

---

## 5. Model Training

Implemented and compared multiple Machine Learning algorithms:

* Logistic Regression
* Random Forest
* XGBoost
* Support Vector Machine (SVM)
* Neural Network Models

---

## 6. Model Evaluation

Models were evaluated using:

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC Score

---

# 🧠 AI Features

## 🔮 Churn Prediction Engine

Predicts:

* Customer churn status
* Churn probability score
* Customer risk level

---

## 📊 Interactive Analytics Dashboard

Provides:

* Customer behavior visualization
* Churn analysis
* Business insights
* Data exploration

---

## 🔍 Explainable AI (XAI)

The platform explains model predictions using:

* Feature Importance
* SHAP Analysis

Helping users understand:

* Why a customer is classified as risky
* Which features influence decisions

---

## 💬 NLP Sentiment Analysis

Analyzes customer reviews and feedback using NLP techniques.

Capabilities:

* Sentiment classification
* Customer satisfaction analysis
* Identification of negative feedback patterns

---

## 📦 Batch Prediction

Allows users to:

* Upload customer datasets
* Run multiple predictions
* Export prediction results

---

# 🛠️ Technologies Used

## Programming

* Python

## Data Processing

* Pandas
* NumPy

## Visualization

* Matplotlib
* Plotly

## Machine Learning

* Scikit-learn
* XGBoost
* Joblib

## NLP

* TF-IDF
* Text Processing

## Application Development

* Streamlit

## Development Tools

* Git
* GitHub
* Jupyter Notebook

---

# 📂 Project Structure

```
Keeper-AI/

│
├── app.py
├── config.py
├── requirements.txt
│
├── artifacts/
│   ├── final_model.joblib
│   ├── preprocessor.joblib
│   ├── tfidf_vectorizer.joblib
│   └── model_metadata.json
│
├── components/
│   ├── cards.py
│   ├── charts.py
│   ├── header.py
│   ├── metrics.py
│   └── sidebar.py
│
├── pages/
│   ├── Prediction.py
│   ├── Analytics.py
│   ├── Explainability.py
│   ├── NLP_Sentiment.py
│   ├── Model_Performance.py
│   └── Batch_Prediction.py
│
├── notebooks/
│   └── Machine Learning Development Notebooks
│
├── outputs/
│   └── Analysis Reports
│
└── README.md
```

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/mohamedkarem20/Keeper-AI.git
```

Navigate to project directory:

```bash
cd Keeper-AI
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate environment:

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Application

Start Streamlit application:

```bash
streamlit run app.py
```

The application will open automatically in your browser.

---

# 📸 Application Screenshots

(Add screenshots here)

Recommended screenshots:

* Home Dashboard
* Prediction Page
* Analytics Dashboard
* Explainability Page
* NLP Sentiment Analysis
* Model Performance

---

# 🚀 Future Improvements

Planned enhancements:

* Deploy model using cloud services
* Build REST API using FastAPI
* Real-time churn prediction
* Automated model retraining pipeline
* Advanced Deep Learning models
* Customer retention recommendation system

---

# 👨‍💻 Author

## Mohamed Karem

AI & Data Analytics Enthusiast

GitHub:
https://github.com/mohamedkarem20

LinkedIn:
https://www.linkedin.com/in/mohamed-karem-mahmoud/

---

# ⭐ Support

If you find this project useful, consider giving it a ⭐ on GitHub.
