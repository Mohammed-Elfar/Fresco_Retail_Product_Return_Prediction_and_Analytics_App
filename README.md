# Fresco Retail Product Return Prediction and Analytics App

## Project Overview
This project analyzes **product returns** for a retail company (Fresco Retailer).  
It aims to understand factors influencing returns and provide **actionable insights** to reduce return rates.

**Key Objectives:**
- Identify patterns in customer returns.
- Examine the impact of **payment methods, store types, income levels, product categories, reviews and tax levels**.
- Provide strategic recommendations to improve customer satisfaction and reduce returns.

---

## Project Steps / Workflow

1. **Data Quality Check**: Review data types, missing values, and duplicates.  
2. **Univariate Analysis**: Explore each column individually to understand distributions and detect issues.  
3. **Bivariate & Multivariate Analysis**: Examine feature interactions to reveal deeper patterns.  
4. **Feature Engineering**: Create new features to improve model performance.  
5. **Feature Importance**: Identify the most impactful features using correlation and ExtraTreesClassifier.  
6. **ML Pipelines**: Build pipelines for preprocessing, encoding, scaling, and handling class imbalance.  
7. **Model Training**: Train multiple ML models with cross-validation.  
8. **Model Selection**: Choose the best model based on performance metrics (XGBOOST here).  
9. **Hyperparameter Tuning**: Optimize model using GridSearchCV.  
10. **Deployment**: Deploy the model using Streamlit for real-time return prediction.

---
