# prediction_page.py
# Fresco Retail — Product Return Prediction
# UI/UX improvements only. All model logic, feature names, defaults, and computations are unchanged.

import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ========== PAGE CONFIG ==========
st.set_page_config(page_title="Fresco Retail — Return Prediction", layout="wide")

st.title("Product Return Prediction")
st.caption("Fresco Retail | ML-powered return risk estimator")

st.info(
    "Fill in the order and customer details below, then click **Predict** to estimate "
    "the probability that this product will be returned. Key values (Price, Total Price, "
    "Tax Ratio) are calculated automatically from your inputs."
)

st.divider()

# ========== MODEL LOADING ==========
MODEL_PATH = "model/XGBoost_Final_Model.joblib"



@st.cache_resource
def load_model(path):
    return joblib.load(path)

try:
    model = load_model(MODEL_PATH)
except Exception as e:
    st.error(f"Model could not be loaded from the configured path. Details: {e}")
    st.stop()

# ========== CATEGORY -> SUBCATEGORY MAPPING ==========
# Unchanged from original.
category_map = {
    "Books": ["Fiction", "DIY", "Non-Fiction", "Academic"],
    "Clothing": ["Women", "Mens"],
    "Home and kitchen": ["Bath", "Kitchen", "Furnishing", "Tools"],
    "Footwear": ["Mens", "Women", "Kids"],
    "Bags": ["Women", "Mens"],
    "Electronics": ["Mobiles", "Audio and video", "Computers", "Cameras", "Personal Appliances"],
}

# ========== SECTION 1: ORDER DETAILS ==========
st.subheader("Order Details")

col_qty, col_price, col_tax = st.columns(3)

with col_qty:
    Quantity = st.slider("Quantity", 1, 10, 3)

with col_price:
    Unit_Price = st.slider("Unit Price", 0.0, 20000.0, 776.17, step=1.0, format="%.2f")

with col_tax:
    Tax = st.slider("Tax", 0.0, 2000.0, 241.24, step=0.1, format="%.2f")

# Auto-calculated values — logic is unchanged.
Price = Quantity * Unit_Price
total_price = Price + Tax
tax_ratio = Tax / (Price + 1)

st.markdown("**Calculated Values**")
calc_col1, calc_col2, calc_col3 = st.columns(3)
calc_col1.metric("Price  (Quantity x Unit Price)", f"${Price:,.2f}")
calc_col2.metric("Total Price  (Price + Tax)", f"${total_price:,.2f}")
calc_col3.metric("Tax Ratio  (Tax / (Price + 1))", f"{tax_ratio:.6f}")

st.divider()

# ========== SECTION 2: PRODUCT DETAILS ==========
st.subheader("Product Details")

prod_col1, prod_col2 = st.columns(2)

with prod_col1:
    product_category = st.selectbox("Product Category", list(category_map.keys()))

with prod_col2:
    sub_options = category_map.get(product_category, [])
    Product_Subcategory = st.selectbox("Product Subcategory", sub_options)

st.divider()

# ========== SECTION 3: CUSTOMER DETAILS ==========
st.subheader("Customer Details")

cust_col1, cust_col2, cust_col3, cust_col4 = st.columns(4)

with cust_col1:
    Reviews = st.slider("Customer Rating (1–5)", 1, 5, 4)

with cust_col2:
    Income = st.slider("Customer Income", 0.0, 300000.0, 70516.88, step=100.0, format="%.2f")

with cust_col3:
    Payment_mode = st.selectbox(
        "Payment Mode",
        ["Mobile Payments", "Credit Card", "Debit Card", "Cash"],
    )

with cust_col4:
    city = st.selectbox(
        "City",
        [
            "Hyderabad", "Bangalore", "Kolkata", "New Delhi", "Chennai",
            "Pune", "Ahmedabad", "Gurgaon", "Vishakhapatnam", "Mumbai",
        ],
    )

st.divider()

# ========== INPUT PREVIEW ==========
# Column names and values are identical to the original.
input_data = pd.DataFrame(
    [
        {
            "Quantity": Quantity,
            "Unit_Price": Unit_Price,
            "Price": Price,
            "Tax": Tax,
            "Reviews": Reviews,
            "Income": Income,
            "total_price": total_price,
            "tax_ratio": tax_ratio,
            "product_category": product_category,
            "Product_Subcategory": Product_Subcategory,
            "Payment_mode": Payment_mode,
            "city": city,
        }
    ]
)

with st.expander("Review input before predicting"):
    st.dataframe(input_data, use_container_width=True)

# ========== PREDICTION ==========
if st.button("Predict", type="primary", use_container_width=False):
    try:
        prob = model.predict_proba(input_data)[0][1]
        pred = model.predict(input_data)[0]
    except Exception as e:
        st.error(f"Prediction failed. Check that model input columns match. Details: {e}")
        st.stop()

    st.divider()
    st.subheader("Prediction Result")

    result_col1, result_col2 = st.columns([1, 2])

    with result_col1:
        st.metric("Return Probability", f"{prob:.1%}")

    with result_col2:
        if pred == 1 or prob >= 0.5:
            st.error(
                f"**Return likely** — The model estimates a {prob:.1%} probability this order "
                "will be returned. Consider reviewing product quality, pricing, or applying a "
                "retention offer before fulfillment."
            )
        else:
            st.success(
                f"**Return unlikely** — The model estimates a {prob:.1%} probability this order "
                "will be not returned. No immediate action required."
            )
