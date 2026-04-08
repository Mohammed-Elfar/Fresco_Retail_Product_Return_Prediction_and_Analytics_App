# 2_analytics_and_insights.py
# Fresco Retail — Analytics & Insights

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Analytics & Insights", layout="wide")

default_path = "/Users/mohammedmahmood/Desktop/Data projects/Projects/Data science/Supervised /Fresco Retailer Product Return Prediction/data/Fresco_Retailerr.xlsx"

# ========== DATA HELPERS ==========

@st.cache_data
def load_data(path=default_path):
    df = pd.read_excel(path)
    df.columns = [c.strip().replace(" ", "_") for c in df.columns]
    return df


def ensure_review_level(df, reviews_col):
    if "Review_Level" in df.columns:
        return df
    def categorize_review(x):
        try:
            x = float(x)
        except Exception:
            return "Unknown"
        if x <= 2:
            return "Low"
        elif x == 3:
            return "Medium"
        else:
            return "High"
    df["Review_Level"] = df[reviews_col].apply(categorize_review)
    return df


def ensure_income_category(df, income_col):
    if "Income_Category" in df.columns:
        return df
    bins   = [0, 38000, 69000, 99000, df[income_col].max()]
    labels = ["Low", "Medium", "High", "Very High"]
    df["Income_Category"] = pd.cut(df[income_col], bins=bins, labels=labels, include_lowest=True)
    return df


def ensure_tax_level(df, tax_col):
    if "Tax_Level" in df.columns:
        return df
    def map_tax(x):
        try:
            x = float(x)
        except Exception:
            return "Unknown"
        if x <= 95.76:
            return "Low"
        elif x <= 349.97:
            return "Medium"
        else:
            return "High"
    df["Tax_Level"] = df[tax_col].apply(map_tax)
    return df


def first_col(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None


# ========== UI HELPERS ==========

def render_insight(text):
    st.markdown("**Insight**")
    st.info(text)


def render_data_expander(df_to_show, download_bytes, file_name):
    with st.expander("View underlying data"):
        st.dataframe(df_to_show, use_container_width=True)
        st.download_button("Download as CSV", data=download_bytes, file_name=file_name, mime="text/csv")


# ========== PAGE HEADER ==========

st.title("Analytics & Insights")
st.caption("Explore return rate patterns across payment methods, income levels, product categories, reviews, and tax.")
st.divider()

# ========== LOAD DATA ==========

try:
    with st.spinner("Loading dataset..."):
        df = load_data()
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

data = df.copy()

# ========== COLUMN DETECTION ==========

return_col         = first_col(data, ["Return", "return", "is_return", "Is_Return"])
payment_col        = first_col(data, ["Payment_mode", "payment_mode", "Payment Method", "PaymentMethod"])
store_col          = first_col(data, ["Store_type", "store_type", "Store Type", "Store"])
income_col         = first_col(data, ["Income", "income", "Annual_Income", "Annual Income"])
product_cat_col    = first_col(data, ["product_category", "Product_category", "Product Category", "Category"])
product_subcat_col = first_col(data, ["Product_Subcategory", "product_subcategory", "Product Subcategory", "Subcategory"])
reviews_col        = first_col(data, ["Reviews", "reviews", "Customer_Reviews", "Rating"])
tax_col            = first_col(data, ["Tax", "tax", "Tax_Amount", "TaxAmount"])

if reviews_col:
    data = ensure_review_level(data, reviews_col)
if income_col:
    data = ensure_income_category(data, income_col)
if tax_col:
    data = ensure_tax_level(data, tax_col)

if return_col is None:
    st.error("No 'Return' column found. Please ensure the dataset contains a 'Return' column.")
    st.stop()

# ========== SIDEBAR ==========

st.sidebar.header("Analysis Controls")

analysis_type = st.sidebar.selectbox("Analysis type", ["Univariate Analysis", "Multivariate Analysis"])

if analysis_type == "Univariate Analysis":
    question = st.sidebar.selectbox(
        "Select a question",
        [
            "Does Payment_mode affect the return rate?",
            "Does the Store_type influence returns?",
            "Does Income level influence return behavior?",
            "What is the Return Rate of products in each Category?",
            "How does Reviews (customer satisfaction) relate to Return?",
            "Does Tax amount (Low/Medium/High) influence returns?",
        ],
    )
else:
    question = st.sidebar.selectbox(
        "Select a question",
        [
            "Combined effect of Review_Level on returns for Women's products (Clothing & Footwear)",
            "Effect of Reviews on Return across Product Categories",
            "Interaction of Income_Level and Product Category on return rates",
            "Return Rate by Tax Level for each Product Subcategory",
        ],
    )

st.sidebar.divider()
st.sidebar.caption("Switch between Univariate and Multivariate views. Each question renders a focused chart with insights.")

# ========== ACTIVE QUESTION HEADER ==========

st.caption(f"Analysis type: {analysis_type}")
st.subheader(question)
st.divider()

# ========== UNIVARIATE SECTION ==========

if analysis_type == "Univariate Analysis":

    if question == "Does Payment_mode affect the return rate?":
        if payment_col:
            with st.spinner("Building chart..."):
                return_by_payment = data.groupby(payment_col)[return_col].mean().reset_index()
                fig = px.bar(
                    return_by_payment, x=payment_col, y=return_col,
                    title="Return Rate by Payment Mode",
                    labels={payment_col: "Payment Mode", return_col: "Average Return Rate"},
                    color=return_col, color_continuous_scale="Blues",
                )
                fig.update_traces(texttemplate="%{y:.2%}", textposition="outside")
                fig.update_layout(yaxis_tickformat=".0%")
            st.plotly_chart(fig, use_container_width=True)
            render_insight(
                "The effect of payment mode on returns appears weak — differences between "
                "payment methods are small (approximately 2% between Credit Card and others)."
            )
            render_data_expander(return_by_payment, return_by_payment.to_csv(index=False).encode(), "return_by_payment.csv")
        else:
            st.warning("Payment_mode column not found in the dataset.")

    elif question == "Does the Store_type influence returns?":
        if store_col:
            with st.spinner("Building chart..."):
                return_by_store = data.groupby(store_col)[return_col].mean().reset_index()
                fig = px.bar(
                    return_by_store, x=store_col, y=return_col,
                    title="Return Rate by Store Type",
                    labels={store_col: "Store Type", return_col: "Average Return Rate"},
                    color=return_col, color_continuous_scale="Blues",
                )
                fig.update_traces(texttemplate="%{y:.2%}", textposition="outside")
                fig.update_layout(yaxis_tickformat=".0%")
            st.plotly_chart(fig, use_container_width=True)
            render_data_expander(return_by_store, return_by_store.to_csv(index=False).encode(), "return_by_store.csv")
        else:
            st.warning("Store_type column not found in the dataset.")

    elif question == "Does Income level influence return behavior?":
        if income_col:
            with st.spinner("Building chart..."):
                tmp = data.copy()
                if "Income_Category" not in tmp.columns:
                    tmp = ensure_income_category(tmp, income_col)
                return_by_income = tmp.groupby("Income_Category")[return_col].mean().reset_index()
                fig = px.bar(
                    return_by_income, x="Income_Category", y=return_col,
                    title="Return Rate by Income Level",
                    labels={"Income_Category": "Income Level", return_col: "Average Return Rate"},
                    color=return_col, color_continuous_scale="Blues",
                )
                fig.update_traces(texttemplate="%{y:.2%}", textposition="outside")
                fig.update_layout(yaxis_tickformat=".0%")
            st.plotly_chart(fig, use_container_width=True)
            render_insight(
                "Very High income customers have the highest return rate (14%), "
                "significantly above other income groups. Income level has a strong effect on return behavior."
            )
            render_data_expander(return_by_income, return_by_income.to_csv(index=False).encode(), "return_by_income.csv")
        else:
            st.warning("Income column not found in the dataset.")

    elif question == "What is the Return Rate of products in each Category?":
        if product_cat_col and product_subcat_col:
            with st.spinner("Building chart..."):
                return_by_category = (
                    data.groupby([product_cat_col, product_subcat_col])[return_col]
                    .mean().reset_index().sort_values(return_col, ascending=False)
                )
                fig = px.bar(
                    return_by_category, x=product_subcat_col, y=return_col,
                    color=return_col, facet_col=product_cat_col, facet_col_wrap=3,
                    title="Return Rate of Products in each Category",
                    labels={product_subcat_col: "Product Subcategory", return_col: "Average Return Rate"},
                )
                fig.update_traces(texttemplate="%{y:.2%}", textposition="outside")
                fig.update_layout(height=900, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            render_insight(
                "Women's products in Bags, Footwear, and Clothing show return rates above 17% — "
                "well above Men's products in the same categories. "
                "In Home and Kitchen, Kitchen and Furnishing subcategories show notable returns at 15–16%. "
                "In Electronics, Mobiles have a 14% return rate. In Books, DIY stands out with a 12% return rate."
            )
            render_data_expander(return_by_category, return_by_category.to_csv(index=False).encode(), "return_by_category.csv")
        else:
            st.warning("Category or Subcategory column missing.")

    elif question == "How does Reviews (customer satisfaction) relate to Return?":
        if reviews_col:
            with st.spinner("Building chart..."):
                tmp = data.copy()
                tmp = ensure_review_level(tmp, reviews_col)
                review_return = (
                    tmp.groupby("Review_Level")[return_col].mean()
                    .reset_index().sort_values(return_col, ascending=False)
                )
                fig = px.bar(
                    review_return, x="Review_Level", y=return_col,
                    title="Return Rate by Customer Satisfaction Level",
                    labels={"Review_Level": "Review Level", return_col: "Average Return Rate"},
                    color="Review_Level",
                )
                fig.update_traces(texttemplate="%{y:.2%}", textposition="outside")
                fig.update_layout(yaxis_tickformat=".0%")
            st.plotly_chart(fig, use_container_width=True)
            render_insight(
                "Low satisfaction customers have the highest return rate at 43% — well above the dataset average. "
                "Satisfaction level has a strong relationship with returns: low satisfaction leads to "
                "significantly more returns than medium or high satisfaction."
            )
            render_data_expander(review_return, review_return.to_csv(index=False).encode(), "review_return.csv")
        else:
            st.warning("Reviews column not found in the dataset.")

    elif question == "Does Tax amount (Low/Medium/High) influence returns?":
        if tax_col:
            with st.spinner("Building chart..."):
                tmp = data.copy()
                tmp = ensure_tax_level(tmp, tax_col)
                tax_return = (
                    tmp.groupby("Tax_Level")[return_col].mean()
                    .reset_index().sort_values(return_col, ascending=False)
                )
                tax_return_display = tax_return.copy()
                tax_return_display[return_col] = tax_return_display[return_col] * 100
                fig = px.bar(
                    tax_return_display, x="Tax_Level", y=return_col,
                    title="Return Rate by Tax Level (%)",
                    labels={"Tax_Level": "Tax Level", return_col: "Return Rate (%)"},
                    text=tax_return_display[return_col].round(2).astype(str) + "%",
                )
                fig.update_traces(textposition="outside")
                fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            render_data_expander(tax_return_display, tax_return.to_csv(index=False).encode(), "tax_return.csv")
        else:
            st.warning("Tax column not found in the dataset.")

# ========== MULTIVARIATE SECTION ==========

elif analysis_type == "Multivariate Analysis":

    if question.startswith("Combined effect"):
        if product_subcat_col:
            df_women = data[
                data[product_subcat_col].astype(str).str.contains("women", case=False, na=False)
                | data[product_subcat_col].astype(str).str.contains("wom", case=False, na=False)
            ]
            if df_women.empty:
                st.warning("No rows found for Women's products based on Product_Subcategory content.")
            else:
                if reviews_col:
                    df_women = ensure_review_level(df_women, reviews_col)
                if "Review_Level" in df_women.columns:
                    with st.spinner("Building chart..."):
                        return_analysis = (
                            df_women.groupby([product_subcat_col, "Review_Level"])[return_col]
                            .mean().reset_index()
                            .sort_values(by=[product_subcat_col, "Review_Level"])
                        )
                        fig = px.bar(
                            return_analysis, x="Review_Level", y=return_col,
                            color=product_subcat_col, barmode="group",
                            title="Return Rates by Review Level for Women's Subcategories",
                            labels={return_col: "Return Rate", "Review_Level": "Review Level"},
                        )
                        fig.update_traces(texttemplate="%{y:.2%}", textposition="outside")
                    st.plotly_chart(fig, use_container_width=True)
                    render_insight(
                        "The relationship between Reviews and Returns is strong across Women's categories. "
                        "Low satisfaction significantly increases return rates for both Clothing and Footwear."
                    )
                    render_data_expander(return_analysis, return_analysis.to_csv(index=False).encode(), "women_return_by_review.csv")
                else:
                    st.warning("Review_Level not available — cannot compute return by satisfaction level.")
        else:
            st.warning("Product_Subcategory column not found. Cannot filter Women's products.")

    elif question.startswith("Effect of Reviews"):
        if reviews_col and product_cat_col:
            with st.spinner("Building chart..."):
                tmp = data.copy()
                tmp = ensure_review_level(tmp, reviews_col)
                review_cat_return = (
                    tmp.groupby([product_cat_col, "Review_Level"])[return_col].mean().reset_index()
                )
                fig = px.bar(
                    review_cat_return, x="Review_Level", y=return_col,
                    color=product_cat_col, barmode="group",
                    title="Return Rate by Review Level across Product Categories",
                    labels={
                        return_col: "Average Return Rate",
                        "Review_Level": "Review Level",
                        product_cat_col: "Product Category",
                    },
                )
                fig.update_traces(texttemplate="%{y:.2%}", textposition="outside")
                fig.update_layout(yaxis_tickformat=".0%")
            st.plotly_chart(fig, use_container_width=True)
            render_data_expander(review_cat_return, review_cat_return.to_csv(index=False).encode(), "review_category_return.csv")
        else:
            st.warning("Reviews or Product Category column not found.")

    elif question.startswith("Interaction of Income_Level"):
        missing_cols = [c for c in ["product_category", "Income", "Return"] if c not in data.columns]
        if missing_cols:
            st.warning("Missing columns for this analysis: " + ", ".join(missing_cols))
        else:
            with st.spinner("Building chart..."):
                tmp = data.copy()
                if "Income_Category" not in tmp.columns:
                    tmp = ensure_income_category(tmp, "Income")
                income_category_return = (
                    tmp.groupby(["Income_Category", "product_category"])["Return"].mean().reset_index()
                )
                fig = px.density_heatmap(
                    income_category_return, x="Income_Category", y="product_category", z="Return",
                    color_continuous_scale="RdYlBu_r",
                    title="Return Rate by Income Level and Product Category",
                    labels={"Return": "Return Rate"},
                )
                fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
            render_insight(
                "Very High income customers drive the highest return rates, particularly for Bags (up to 20%) "
                "and Home and Kitchen (18–20%). Bags show elevated return rates across both Medium and "
                "Very High income groups, suggesting sensitivity to product expectations or quality."
            )
            render_data_expander(income_category_return, income_category_return.to_csv(index=False).encode(), "income_category_return.csv")

    elif question.startswith("Return Rate by Tax Level"):
        if tax_col and product_subcat_col:
            with st.spinner("Building chart..."):
                tmp = data.copy()
                tmp = ensure_tax_level(tmp, tax_col)
                tax_sub_return = (
                    tmp.groupby(["Tax_Level", product_subcat_col])[return_col]
                    .mean().reset_index().sort_values("Return", ascending=False)
                )
                tax_sub_return_display = tax_sub_return.copy()
                tax_sub_return_display[return_col] = tax_sub_return_display[return_col] * 100
                fig = px.bar(
                    tax_sub_return_display, x=product_subcat_col, y=return_col,
                    color="Tax_Level", barmode="group",
                    text=tax_sub_return_display[return_col].round(1).astype(str) + "%",
                    title="Return Rate by Tax Level and Product Subcategory",
                    labels={return_col: "Return Rate (%)", product_subcat_col: "Product Subcategory"},
                )
                fig.update_traces(textposition="outside")
                fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            render_insight(
                "Mobiles under the High tax level show the highest return rate at 24%. "
                "Women's products (19–20%) and Furnishing/Kitchen (15–19%) also show elevated returns under high tax. "
                "Women's subcategories maintain consistently high return rates across all tax levels, "
                "suggesting a persistent product issue independent of tax."
            )
            render_data_expander(tax_sub_return_display, tax_sub_return.to_csv(index=False).encode(), "tax_sub_return.csv")
        else:
            st.warning("Tax column or Product_Subcategory column missing.")


