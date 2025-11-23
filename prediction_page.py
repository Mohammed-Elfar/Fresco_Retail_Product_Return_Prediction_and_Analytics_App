# app.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ========== PAGE CONFIG ==========
st.set_page_config(page_title="Fresco Retail’s Product Return Prediction", layout="wide")
st.title("Fresco Retail’s Product Return Prediction")

st.info(
    """
      **Prediction Overview**

    This page estimates the probability that a product will be returned using a trained ML model.
    - Fill the order and customer fields (quantity, unit price, tax, category, payment mode, income).  
    - Key values (Price, Total Price, Tax Ratio) are auto-calculated.  
    - Click **Predict** to get a return probability and a clear recommendation.

    Use this to spot high-risk orders and act (review quality, adjust offers, or flag for retention).
    """
)

# ========== MODEL LOADING ==========
MODEL_PATH = "model/Final_Model.joblib"

@st.cache_resource
def load_model(path):
    return joblib.load(path)

try:
    model = load_model(MODEL_PATH)
except Exception as e:
    st.error(f"Failed loading model from '{MODEL_PATH}': {e}")
    st.stop()

st.markdown("Fill the product and order details below and click **Predict** to get a return prediction and probability.")

# ========== CATEGORY -> SUBCATEGORY MAPPING ==========
category_map = {
    "Books": ["Fiction", "DIY", "Non-Fiction", "Academic"],
    "Clothing": ["Women", "Mens"],
    "Home and kitchen": ["Bath", "Kitchen", "Furnishing", "Tools"],
    "Footwear": ["Mens", "Women", "Kids"],
    "Bags": ["Women", "Mens"],
    "Electronics": ["Mobiles", "Audio and video", "Computers", "Cameras", "Personal Appliances"]
}

# ========== INPUT SECTION ==========
col1, col2 = st.columns(2)

with col1:
    Quantity = st.slider("Quantity", 1, 10, 3)
    Unit_Price = st.slider("Unit Price", 0.0, 20000.0, 776.17, step=1.0, format="%.2f")
    Tax = st.slider("Tax", 0.0, 2000.0, 241.24, step=0.1, format="%.2f")
    Reviews = st.slider("Reviews (rating)", 1, 5, 4)

with col2:
    Income = st.slider("Customer Income", 0.0, 300000.0, 70516.88, step=100.0, format="%.2f")

    # ----- Auto Calculations -----
    Price = Quantity * Unit_Price
    total_price = Price + Tax
    # avoid division by zero; follow your formula: Tax / (Price + 1)
    tax_ratio = Tax / (Price + 1)

    # show computed values as nice metrics (instead of disabled inputs)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Price = Quantity * Unit_Price", f"${Price:,.2f}")
    with m2:
        st.metric("Total Price = Price + Tax", f"${total_price:,.2f}")
    with m3:
        st.metric("Tax Ratio = Tax / (Price + 1)", f"{tax_ratio:.6f}")

    # Product category selectbox
    product_category = st.selectbox("Product Category", list(category_map.keys()))

    # Product subcategory options depend on selected category
    sub_options = category_map.get(product_category, [])
    Product_Subcategory = st.selectbox("Product Subcategory", sub_options)

# separate row for payment and city
payment_col, city_col = st.columns(2)
with payment_col:
    Payment_mode = st.selectbox("Payment Mode", ["Mobile Payments", "Credit Card", "Debit Card", "Cash"])
with city_col:
    city = st.selectbox("City", [
        "Hyderabad", "Bangalore", "Kolkata", "New Delhi", "Chennai",
        "Pune", "Ahmedabad", "Gurgaon", "Vishakhapatnam", "Mumbai"
    ])

# prepare input dataframe (make sure column names match what the model expects)
input_data = pd.DataFrame([{
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
    "city": city
}])

st.markdown("---")
st.write("Input preview:")
st.dataframe(input_data)

# ======= PREDICT =======
if st.button("Predict"):
    try:
        prob = model.predict_proba(input_data)[0][1]   # Probability of return
        pred = model.predict(input_data)[0]
    except Exception as e:
        st.error(f"Prediction error — check model and input columns: {e}")
        st.stop()

    st.metric("Return probability", f"{prob:.2%}")

    if pred == 1 or prob >= 0.5:
        st.error(f"🔻 Predicted: RETURN (prob = {prob:.2%})")
    else:
        st.success(f"✅ Predicted: NO RETURN (prob = {prob:.2%})")
