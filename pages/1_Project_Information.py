import streamlit as st
import pandas as pd

# ================== PAGE SETUP ==================
st.set_page_config(page_title="Project Info & Data Overview", layout="wide")

# ---------- PAGE HEADER ----------
st.markdown("<h1 style='color:#1E88E5; font-weight:700;'>📋 Project Info & Data Overview</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#555;'>Upload your dataset, preview it, and see project description and steps.</p>", unsafe_allow_html=True)
st.write("---")

# ================== DATA UPLOAD ==================
st.header("Upload Dataset (Optional)")

default_path = r"data/Fresco_Retailerr.xlsx"
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=['csv', 'xlsx'])

@st.cache_data
def load_data(file_path=None, file_obj=None):
    if file_obj is not None:
        if file_obj.name.endswith(".csv"):
            df = pd.read_csv(file_obj)
        else:
            df = pd.read_excel(file_obj)
    else:
        df = pd.read_excel(file_path)
    # Normalize column names
    df.columns = [c.strip().replace(" ", "_") for c in df.columns]
    return df

# Load dataset
df = load_data(file_obj=uploaded_file) if uploaded_file else load_data(file_path=default_path)

# ---------- BASIC INFO ----------
st.subheader("Dataset Overview")
col1, col2 = st.columns(2)
col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
st.write("---")

# ---------- DATA PREVIEW ----------
st.subheader("Data Preview")
st.dataframe(df.head(5), use_container_width=True)

# ---------- COLUMN INFO ----------
st.subheader("Columns & Data Types")
st.dataframe(df.dtypes.apply(lambda x: str(x)).to_frame("Data Type"))

# Optional summary stats
if st.checkbox("Show Summary Statistics"):
    st.subheader("Numerical Columns Summary")
    st.dataframe(df.describe().T)
    st.subheader("Categorical Columns Summary")
    cat_cols = df.select_dtypes(include='object').columns
    if len(cat_cols) > 0:
        st.dataframe(df[cat_cols].describe().T)
    else:
        st.info("No categorical columns found.")

st.write("---")

# ================== PROJECT DESCRIPTION ==================
st.header("Project Overview")
st.markdown("""
This project analyzes **product returns** for a retail company (Fresco Retailer).  
It aims to understand factors influencing returns and provide **actionable insights** to reduce return rates.

**Key Objectives:**
- Identify patterns in customer returns.
- Examine the impact of **payment methods, store types, income levels, product categories, reviews, and tax levels**.
- Provide strategic recommendations to improve customer satisfaction and reduce returns.
""")
st.write("---")

# ================== PROJECT STEPS ==================
st.header("Project Steps / Workflow")
st.markdown("""
1. **Data Quality Check**: Review data types, missing values and duplicates.  
2. **Univariate Analysis**: Explore each column individually to understand distributions and detect issues. 
3. **Bivariate & Multivariate Analysis**: Examine feature interactions to reveal deeper patterns.
4. **Feature Engineering**: Create new features to improve model performance.  
5. **Feature Importance**: Identify the most impactful features using correlation and ExtraTreesClassifier.
6. **ML Pipelines**: Build pipelines for preprocessing, encoding, scaling, and handling class imbalance.  
7. **Model Training**: Train multiple ML models with cross-validation.  
8. **Model Selection**: Choose the best model based on performance metrics (XGBOOST here).  
9. **Hyperparameter Tuning**: Optimize model using GridSearchCV.  
10. **Deployment**: Deploy the model using Streamlit for real-time return prediction.
""")
st.write("---")

# ================== TOOLS & TECHNOLOGIES ==================
st.header("Tools & Technologies")
st.markdown("""
- **Python Libraries:** Pandas, NumPy, Scikit-learn, Plotly, Streamlit  
- **Machine Learning Algorithms:** XGBOOST, GridSearchCV, Pipelines, Imbalance handling techniques  
- **Deployment:** Streamlit for interactive analysis and real-time prediction  
- **Visualization:** Plotly and Streamlit charts for data exploration and insights
""")
