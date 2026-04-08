# 1_Project_Information.py
# Fresco Retail — Project Info & Data Overview

import streamlit as st
import pandas as pd

# ========== PAGE CONFIG ==========
st.set_page_config(page_title="Project Info & Data Overview", layout="wide")

st.title("Fresco Retail — Product Return Prediction")
st.caption(
    "A machine learning project to identify, analyze, and predict product return risk "
    "across customer segments, product categories, and order attributes."
)

st.divider()

# ========== DATA UPLOAD ==========
st.subheader("Dataset")

default_path = "/Users/mohammedmahmood/Desktop/Data projects/Projects/Data science/Supervised /Fresco Retailer Product Return Prediction/data/Fresco_Retailerr.xlsx"


uploaded_file = st.file_uploader(
    "Upload a CSV or Excel file to use your own dataset. "
    "If no file is uploaded, the project default dataset is loaded automatically.",
    type=["csv", "xlsx"],
)

@st.cache_data
def load_data(file_path=None, file_obj=None):
    if file_obj is not None:
        if file_obj.name.endswith(".csv"):
            df = pd.read_csv(file_obj)
        else:
            df = pd.read_excel(file_obj)
    else:
        df = pd.read_excel(file_path)
    df.columns = [c.strip().replace(" ", "_") for c in df.columns]
    return df

df = load_data(file_obj=uploaded_file) if uploaded_file else load_data(file_path=default_path)

# ========== DATASET OVERVIEW ==========
st.subheader("Dataset Overview")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Records", f"{df.shape[0]:,}")
m2.metric("Total Features", df.shape[1])
m3.metric("Numerical Columns", len(df.select_dtypes(include="number").columns))
m4.metric("Categorical Columns", len(df.select_dtypes(include="object").columns))

st.divider()

st.subheader("Data Preview")
st.dataframe(df.head(5), use_container_width=True)

st.subheader("Columns and Data Types")
st.dataframe(
    df.dtypes.apply(lambda x: str(x)).to_frame("Data Type"),
    use_container_width=True,
)

if st.checkbox("Show Summary Statistics"):
    st.subheader("Numerical Columns — Descriptive Statistics")
    st.dataframe(df.describe().T, use_container_width=True)

    st.subheader("Categorical Columns — Descriptive Statistics")
    cat_cols = df.select_dtypes(include="object").columns
    if len(cat_cols) > 0:
        st.dataframe(df[cat_cols].describe().T, use_container_width=True)
    else:
        st.info("No categorical columns found in this dataset.")

st.divider()

# ========== BUSINESS CONTEXT ==========
st.subheader("Business Context")
st.markdown(
    """
    Product returns are one of the most costly operational challenges in retail.
    Each return represents lost revenue, increased reverse-logistics costs, and a signal
    of unmet customer expectations. For Fresco Retailer, understanding *why* customers
    return products — and *which* orders carry the highest return risk — is a direct
    business priority with measurable financial impact.

    This project addresses that challenge by combining structured exploratory analysis
    with a supervised machine learning model that estimates return probability at the
    order level. The result is a practical decision-support tool that operations,
    merchandising, and customer experience teams can act on before and after fulfillment.
    """
)

st.divider()

# ========== PROJECT OBJECTIVES ==========
st.subheader("Project Objectives")

obj_col1, obj_col2 = st.columns(2)

with obj_col1:
    st.markdown(
        """
        **Analytical Objectives**
        - Quantify return rates across product categories, subcategories, store types, and payment methods.
        - Identify which customer segments — by income level and satisfaction rating — carry the highest return risk.
        - Measure the influence of tax levels on return behavior across product subcategories.
        - Surface interaction effects between features that a single-variable view would miss.
        """
    )

with obj_col2:
    st.markdown(
        """
        **Predictive Objectives**
        - Build a classification model that estimates the probability of return for any new order.
        - Ensure robustness to class imbalance, which is common in return datasets.
        - Deliver predictions through a real-time interface accessible to non-technical stakeholders.
        - Provide interpretable outputs — probability score plus a clear recommendation — rather than opaque binary labels.
        """
    )

st.divider()

# ========== DATASET DESCRIPTION ==========
st.subheader("Dataset Description")
st.markdown(
    """
    The dataset contains transactional records from Fresco Retailer, covering customer orders
    across multiple product categories, store types, and cities in India.
    Each row represents a single order with associated customer, product, and financial attributes.

    **Raw Features**

    | Feature | Type | Description |
    |---|---|---|
    | Product Category | Categorical | Top-level category of the purchased item (e.g., Electronics, Clothing, Bags) |
    | Product Subcategory | Categorical | Specific subcategory within the category (e.g., Mobiles, Women, Kitchen) |
    | Quantity | Numerical | Number of units ordered |
    | Unit Price | Numerical | Price per unit before tax |
    | Tax | Numerical | Tax amount applied to the order |
    | Income | Numerical | Annual income of the customer |
    | Reviews | Numerical | Customer satisfaction rating on a 1–5 scale |
    | Payment Mode | Categorical | Payment method used (Credit Card, Debit Card, Cash, Mobile Payments) |
    | City | Categorical | City where the order was placed |
    | Return | Binary (Target) | 1 if the product was returned, 0 otherwise |

    **Engineered Features** (derived during preprocessing)

    | Feature | Formula | Purpose |
    |---|---|---|
    | Price | Quantity × Unit Price | Total order value before tax |
    | Total Price | Price + Tax | Final order value including tax |
    | Tax Ratio | Tax / (Price + 1) | Relative tax burden on the order |
    | Review Level | Binned from Reviews: Low (1–2), Medium (3), High (4–5) | Categorical satisfaction segment |
    | Income Category | Binned: Low / Medium / High / Very High | Customer income segment |
    | Tax Level | Binned: Low / Medium / High | Categorical tax burden classification |
    """
)

st.divider()

# ========== PROJECT WORKFLOW ==========
st.subheader("Project Workflow")
st.markdown(
    """
    | Phase | Step | Description |
    |---|---|---|
    | **Data Understanding** | 1. Data Quality Check | Audit data types, missing values, duplicates, and outliers before any analysis begins. |
    | **Exploratory Analysis** | 2. Univariate Analysis | Examine the distribution of each feature individually — range, skew, and category frequencies. |
    | **Exploratory Analysis** | 3. Bivariate and Multivariate Analysis | Investigate relationships between features and the return target, including interaction effects that single-variable analysis misses. |
    | **Feature Engineering** | 4. Feature Creation | Derive Price, Total Price, Tax Ratio, and binned categorical variables to improve model signal. |
    | **Modeling Preparation** | 5. Feature Importance | Rank features using correlation analysis and ExtraTreesClassifier to guide feature selection and reduce noise. |
    | **Modeling Preparation** | 6. ML Pipelines | Build end-to-end pipelines covering encoding, scaling, SMOTE oversampling, and preprocessing consistency between training and inference. |
    | **Model Development** | 7. Model Training | Train and cross-validate multiple classifiers (Logistic Regression, Random Forest, XGBoost) using stratified K-Fold to prevent data leakage. |
    | **Model Development** | 8. Model Selection | Select the best model based on F1-score, ROC-AUC, and precision-recall trade-off. XGBoost was selected as the final model. |
    | **Optimization** | 9. Hyperparameter Tuning | Fine-tune the selected model using GridSearchCV to maximize generalization on unseen data. |
    | **Deployment** | 10. Production Interface | Serialize the trained pipeline with Joblib and deploy via Streamlit for real-time return probability estimation. |
    """
)

st.divider()

# ========== TOOLS & TECHNOLOGIES ==========
st.subheader("Tools and Technologies")

t1, t2, t3 = st.columns(3)

with t1:
    st.markdown(
        """
        **Data and Analysis**
        - Pandas — data manipulation and aggregation
        - NumPy — numerical computation
        - Plotly — interactive visualizations
        """
    )

with t2:
    st.markdown(
        """
        **Machine Learning**
        - Scikit-learn — pipelines, preprocessing, cross-validation, GridSearchCV
        - XGBoost — gradient boosted classifier (final selected model)
        - Imbalanced-learn — SMOTE for handling class imbalance
        - Joblib — model serialization and deployment
        """
    )

with t3:
    st.markdown(
        """
        **Deployment and Interface**
        - Streamlit — multi-page interactive application
        - Python 3.x — core runtime environment
        """
    )

st.divider()

# ========== EXPECTED BUSINESS VALUE ==========
st.subheader("Expected Business Value")
st.markdown(
    """
    | Stakeholder | How This Project Delivers Value |
    |---|---|
    | **Operations / Logistics** | Flag high-risk orders before dispatch to reduce reverse logistics volume and cost. |
    | **Merchandising** | Identify product subcategories with structurally high return rates to inform sourcing, quality control, and supplier negotiations. |
    | **Customer Experience** | Detect low-satisfaction segments early and trigger proactive outreach, fit guidance, or retention offers. |
    | **Finance** | Quantify return risk by segment to improve revenue forecasting and reserve planning. |
    | **Marketing** | Tailor campaigns by income group and product category based on return risk profiles to improve ROI. |
    """
)