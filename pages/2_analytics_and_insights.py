# app.py
# Streamlit app: Analytics & Insights for Fresco returns
# - Load an Excel file, perform univariate & multivariate analyses
# - Show interactive Plotly charts, downloadable CSVs, insight expanders

import streamlit as st
import pandas as pd
import plotly.express as px

# ================== PAGE SETUP ==================
st.set_page_config(page_title=" Analytics & Insights", layout="wide")
st.title("📊 Analytics & Insights")

# ================== CONFIG ==================
# Change this path to where your Excel file lives on your machine
DATA_PATH = r'/Users/mohammedmahmood/Desktop/Data projects/Data science/Fresco Retailer Product Return Prediction/data/Fresco_Retailerr.xlsx'

# ================== HELPERS ==================
@st.cache_data
def load_data(path=DATA_PATH):
    """
    Load Excel data and normalise column names.
    Using caching so reload is fast during development.
    """
    df = pd.read_excel(path)
    # replace spaces and trim column names so we can reference them easily
    df.columns = [c.strip().replace(" ", "_") for c in df.columns]
    return df

def ensure_review_level(df, reviews_col):
    """
    Derive 'Review_Level' (Low / Medium / High) from numeric reviews.
    Returns the same dataframe (in-place addition).
    """
    if "Review_Level" in df.columns:
        return df

    def categorize_review(x):
        try:
            x = float(x)
        except:
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
    """
    Bucket income into categorical bins: Low / Medium / High / Very High.
    Adjust the bin thresholds if your data distribution differs.
    """
    if "Income_Category" in df.columns:
        return df
    bins = [0, 38000, 69000, 99000, df[income_col].max()]
    labels = ['Low', 'Medium', 'High', 'Very High']
    df["Income_Category"] = pd.cut(df[income_col], bins=bins, labels=labels, include_lowest=True)
    return df

def ensure_tax_level(df, tax_col):
    """
    Create 'Tax_Level' categories: Low / Medium / High based on thresholds.
    Thresholds chosen from prior conversation — tweak as needed.
    """
    if "Tax_Level" in df.columns:
        return df

    def map_tax(x):
        try:
            x = float(x)
        except:
            return "Unknown"
        if x <= 95.76:
            return "Low"
        elif x <= 349.97:
            return "Medium"
        else:
            return "High"

    df["Tax_Level"] = df[tax_col].apply(map_tax)
    return df

# Helper to support datasets that might use slightly different names
def first_col(df, candidates):
    """
    Return the first existing column name from candidates, or None if none exist.
    This helps make the script robust to small column-name variations.
    """
    for c in candidates:
        if c in df.columns:
            return c
    return None

# ================== LOAD DATA ==================
try:
    df = load_data()  # loads and normalizes column names
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

data = df.copy()

# ================== COLUMN DETECTION (variants) for Univariate ==================
# We try to detect several common column-name variants to be robust.
return_col = first_col(data, ["Return", "return", "is_return", "Is_Return"])
payment_col = first_col(data, ["Payment_mode", "payment_mode", "Payment Method", "PaymentMethod"])
store_col = first_col(data, ["Store_type", "store_type", "Store Type", "Store"])
income_col = first_col(data, ["Income", "income", "Annual_Income", "Annual Income"])
product_cat_col = first_col(data, ["product_category", "Product_category", "Product Category", "Category"])
product_subcat_col = first_col(data, ["Product_Subcategory", "product_subcategory", "Product Subcategory", "Subcategory"])
reviews_col = first_col(data, ["Reviews", "reviews", "Customer_Reviews", "Rating"])
tax_col = first_col(data, ["Tax", "tax", "Tax_Amount", "TaxAmount"])

# create derived columns only if the source exists
if reviews_col:
    data = ensure_review_level(data, reviews_col)
if income_col:
    data = ensure_income_category(data, income_col)
if tax_col:
    data = ensure_tax_level(data, tax_col)

# core sanity check: we need a Return column to compute rates
if return_col is None:
    st.error("No 'Return' column found in the dataset. Please ensure the dataset contains a 'Return' column.")
    st.stop()

# ================== SIDEBAR (UI) ==================
analysis_type = st.sidebar.selectbox(
    "Select analysis type:",
    ["Univariate Analysis", "Multivariate Analysis"]
)

if analysis_type == "Univariate Analysis":
    question = st.sidebar.selectbox(
        "Select analysis question:",
        [
            "1️⃣ Does Payment_mode affect the return rate?",
            "2️⃣ Does the Store_type influence returns?",
            "3️⃣ Does Income level influence return behavior?",
            "4️⃣ What is Return Rate of products in each Category?",
            "5️⃣ How does Reviews (customer satisfaction) relate to Return?",
            "6️⃣ Does Tax amount (Low/Medium/High) influence returns?"
        ]
    )
else:
    question = st.sidebar.selectbox(
        "Select multivariate question:",
        [
            "1️⃣ Combined effect of Review_Level on returns for Women's products (Clothing & Footwear)",
            "2️⃣ Effect of Reviews on Return across Product Categories",
            "3️⃣ Interaction of Income_Level and Product Category on return rates",
            "4️⃣ Return Rate by Tax Level for each Product Subcategory"
        ]
    )

st.markdown("---")
st.write(f"**Selected:** {analysis_type} → {question}")

# ================== UNIVARIATE SECTION ==================
# Each block below:
# - checks that required columns exist,
# - computes an aggregated table,
# - shows a Plotly chart,
# - provides an insight expander and a download button.

if analysis_type == "Univariate Analysis":
    # 1) Payment mode
    if question == "1️⃣ Does Payment_mode affect the return rate?":
        st.header("Does Payment Mode affect the return rate?")
        if payment_col:
            return_by_payment = data.groupby(payment_col)[return_col].mean().reset_index()
            fig = px.bar(return_by_payment, x=payment_col, y=return_col,
                         title="Return Rate by Payment Mode",
                         labels={payment_col: "Payment Mode", return_col: "Average Return Rate"},
                         color=return_col, color_continuous_scale="Blues")
            fig.update_traces(texttemplate='%{y:.2%}', textposition='outside')
            fig.update_layout(yaxis_tickformat='.0%')
            st.plotly_chart(fig, use_container_width=True)
            st.download_button("📥 Download data (CSV)", data=return_by_payment.to_csv(index=False).encode("utf-8"), file_name="return_by_payment.csv")

            with st.expander("Insight Summary"):
                st.write("- **The effect of payment mode on returns seems weak because the differences are small (only about 2% between Credit Card and others).**")
        else:
            st.warning("Payment_mode column not found.")

    # 2) Store type
    elif question == "2️⃣ Does the Store_type influence returns?":
        st.header("Does the Store Type influence returns?")
        if store_col:
            return_by_store = data.groupby(store_col)[return_col].mean().reset_index()
            fig = px.bar(return_by_store, x=store_col, y=return_col,
                         title="Return Rate by Store Type",
                         labels={store_col: "Store Type", return_col: "Average Return Rate"},
                         color=return_col, color_continuous_scale="Blues")
            fig.update_traces(texttemplate='%{y:.2%}', textposition='outside')
            fig.update_layout(yaxis_tickformat='.0%')
            st.plotly_chart(fig, use_container_width=True)
            st.download_button("📥 Download data (CSV)", data=return_by_store.to_csv(index=False).encode("utf-8"), file_name="return_by_store.csv")
        else:
            st.warning("Store_type column not found.")

    # 3) Income level
    elif question == "3️⃣ Does Income level influence return behavior?":
        st.header("Does Income level influence return behavior?")
        if income_col:
            tmp = data.copy()
            if "Income_Category" not in tmp.columns:
                tmp = ensure_income_category(tmp, income_col)
            return_by_income = tmp.groupby("Income_Category")[return_col].mean().reset_index()
            fig = px.bar(return_by_income, x="Income_Category", y=return_col,
                         title="Return Rate by Income Level",
                         labels={"Income_Category": "Income Level", return_col: "Average Return Rate"},
                         color=return_col, color_continuous_scale="Blues")
            fig.update_traces(texttemplate='%{y:.2%}', textposition='outside')
            fig.update_layout(yaxis_tickformat='.0%')
            st.plotly_chart(fig, use_container_width=True)
            st.download_button("📥 Download data (CSV)", data=return_by_income.to_csv(index=False).encode("utf-8"), file_name="return_by_income.csv")

            with st.expander("Insight Summary"):
                st.write("- **1- Very High income level has the highest return rate at 0.14 (14% returned), much higher than the others**")
                st.write("- **2- The effect of income on returns is strong because Very High income people return a lot more than others.**")
            with st.expander("Recommendation Summary"):
                st.write("- **1- Focus on why Very High income customers return items—maybe they buy expensive things and change their minds.**")
                st.write("- **2- Check if product quality or store service needs improvement for high-income shoppers**")
        else:
            st.warning("Income column not found.")

    # 4) Return rate by category & subcategory
    elif question == "4️⃣ What is Return Rate of products in each Category?":
        st.header("Return Rate of products in each Category")
        if product_cat_col and product_subcat_col:
            return_by_category = (
                data.groupby([product_cat_col, product_subcat_col])[return_col]
                .mean()
                .reset_index()
                .sort_values(return_col, ascending=False)
            )
            fig = px.bar(
                return_by_category,
                x=product_subcat_col,
                y=return_col,
                color=return_col,
                facet_col=product_cat_col,
                facet_col_wrap=3,
                title='Return Rate of products in each Category',
                labels={product_subcat_col: 'Product Subcategory', return_col: 'Average Return Rate'}
            )
            fig.update_traces(texttemplate='%{y:.2%}', textposition='outside')
            fig.update_layout(height=900, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            st.download_button("📥 Download data (CSV)", data=return_by_category.to_csv(index=False).encode("utf-8"), file_name="return_by_category.csv")
            st.dataframe(return_by_category)

            with st.expander("Insight Summary"):
                st.write("- **1- In the Bags, Footwear, and Clothing categories, Women’s products have a high return rate above 17%, much higher than Men’s products, suggesting a specific issue with women’s items.**")
                st.write("- **2- In the Home and Kitchen category, Kitchen and Furnishing subcategories show significant returns at 15-16%, indicating potential problems in these areas.**")
                st.write("- **3- In the Electronics category, Mobiles have a notable return rate of 14%, pointing to possible quality or usability concerns.**")
                st.write("- **4- In the Books category, DIY stands out with a 12% return rate, higher than other subcategories, suggesting an area needing attention.**")
                st.write("- **5- The effect of gender and subcategory on returns is strong, with women’s products and specific subcategories like Kitchen, Furnishing, Mobiles, and DIY driving higher return rates.**")
            with st.expander("Recommendation Summary"):
                st.write("- **1- For Bags, Footwear, and Clothing, investigate why Women’s products exceed 17% returns—check for sizing issues, fit problems, or quality defects—and improve product design or provide better fitting guides**")
                st.write("- **2- For Electronics, address Mobiles’ 14% return rate with better quality control, improved warranties, or customer support for technical issues.**")
                st.write("- **3- Collect customer feedback during the trial month to understand why they are returning products (e.g., wrong size or poor quality) and use the results to improve the products.**")
        else:
            st.warning("Category or Subcategory column missing.")

    # 5) Reviews -> Return
    elif question == "5️⃣ How does Reviews (customer satisfaction) relate to Return?":
        st.header("How does Reviews (customer satisfaction) relate to Return?")
        if reviews_col:
            tmp = data.copy()
            tmp = ensure_review_level(tmp, reviews_col)
            review_return = tmp.groupby("Review_Level")[return_col].mean().reset_index().sort_values(return_col, ascending=False)
            fig = px.bar(review_return, x='Review_Level', y=return_col, title='Return Rate by Customer Satisfaction Level',
                         labels={'Review_Level': 'Review Level', return_col: 'Average Return Rate'}, color='Review_Level')
            fig.update_traces(texttemplate='%{y:.2%}', textposition='outside')
            fig.update_layout(yaxis_tickformat='.0%')
            st.plotly_chart(fig, use_container_width=True)
            st.download_button("📥 Download data (CSV)", data=review_return.to_csv(index=False).encode("utf-8"), file_name="review_return.csv")
            st.dataframe(review_return)

            with st.expander("Insight Summary"):
                st.write("- **1- Low satisfaction level has the highest return rate at 0.43 (43% returned), much higher than the average.**")
                st.write("- **2- The effect of satisfaction level on returns is strong because low satisfaction leads to a lot more returns than high or medium.**")
            with st.expander("Recommendation Summary"):
                st.write("- **1- Focus on improving satisfaction for customers with low reviews to reduce returns.**")
        else:
            st.warning("Reviews column not found.")

    # 6) Tax question
    elif question == "6️⃣ Does Tax amount (Low/Medium/High) influence returns?":
        st.header("Does Tax amount (Low/Medium/High) influence returns?")
        if tax_col:
            tmp = data.copy()
            tmp = ensure_tax_level(tmp, tax_col)
            tax_return = tmp.groupby("Tax_Level")[return_col].mean().reset_index().sort_values(return_col, ascending=False)
            tax_return_display = tax_return.copy()
            tax_return_display[return_col] = tax_return_display[return_col] * 100
            fig = px.bar(tax_return_display, x="Tax_Level", y=return_col,
                         title="Return Rate by Tax Level (%)",
                         labels={"Tax_Level": "Tax Level", return_col: "Return Rate (%)"},
                         text=tax_return_display[return_col].round(2).astype(str) + '%')
            fig.update_traces(textposition='outside')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            st.download_button("📥 Download data (CSV)", data=tax_return.to_csv(index=False).encode("utf-8"), file_name="tax_return.csv")
            st.dataframe(tax_return_display)
        else:
            st.warning("Tax column not found.")

# ================== MULTIVARIATE SECTION ==================
elif analysis_type == "Multivariate Analysis":
    # 1) Combined effect of Review_Level on returns for Women's subcategories
    if question.startswith("1️⃣ Combined effect"):
        st.header("Combined effect of Review Level on returns for Women's products (Clothing & Footwear)")
        subcat = product_subcat_col
        if subcat:
            df_women = data[data[subcat].astype(str).str.contains("women", case=False, na=False) | data[subcat].astype(str).str.contains("wom", case=False, na=False)]
            if df_women.empty:
                st.warning("No rows found for women's products based on Product_Subcategory content.")
            else:
                if reviews_col:
                    df_women = ensure_review_level(df_women, reviews_col)
                else:
                    st.warning("No Reviews column found to derive Review_Level.")
                if "Review_Level" in df_women.columns:
                    return_analysis = (
                        df_women.groupby([subcat, "Review_Level"])[return_col]
                        .mean()
                        .reset_index()
                        .sort_values(by=[subcat, "Review_Level"])
                    )
                    fig = px.bar(
                        return_analysis,
                        x="Review_Level",
                        y=return_col,
                        color=subcat,
                        barmode="group",
                        title="Return Rates by Review Level for Women's subcategories",
                        labels={return_col: "Return Rate", "Review_Level": "Review Level"}
                    )
                    fig.update_traces(texttemplate='%{y:.2%}', textposition='outside')
                    st.plotly_chart(fig, use_container_width=True)
                    st.download_button("📥 Download data (CSV)", data=return_analysis.to_csv(index=False).encode("utf-8"), file_name="women_return_by_review.csv")
                    st.dataframe(return_analysis)

                    with st.expander("Insight Summary"):
                        st.write("The relationship between Reviews and Return is strong across categories, especially for Women’s products, where low satisfaction significantly increases return rates.")
                    with st.expander("Recommendation Summary"):
                        st.write("Focus on addressing the 59% return rate for Women’s Clothing and Footwear under low satisfaction by improving product quality, fit accuracy, or expectation alignment.")
                else:
                    st.warning("Review_Level not available to calculate return by satisfaction level.")
        else:
            st.warning("Product_Subcategory column not found. Cannot filter women's products.")

    # 2) Effect of Reviews on Return across Product Categories
    elif question.startswith("2️⃣ Effect of Reviews"):
        st.header("Effect of Reviews on Return Rate by Product Category")
        # Clean, fixed-column implementation uses 'product_category', 'Reviews', 'Return'
        prod_cat_col = "product_category"
        reviews_col_fixed = "Reviews"
        return_col_fixed = "Return"

        # check columns exist
        missing_cols = [c for c in [prod_cat_col, reviews_col_fixed, return_col_fixed] if c not in data.columns]
        if missing_cols:
            st.warning("Missing columns for this analysis: " + ", ".join(missing_cols))
        else:
            tmp = data.copy()
            tmp = ensure_review_level(tmp, reviews_col_fixed)  # ensure Review_Level exists
            review_return = (
                tmp.groupby([prod_cat_col, "Review_Level"])[return_col_fixed]
                .mean()
                .reset_index()
                .sort_values(by=[prod_cat_col, "Review_Level"])
            )
            fig = px.line(
                review_return,
                x="Review_Level",
                y=return_col_fixed,
                color=prod_cat_col,
                markers=True,
                title="Effect of Customer Review Level on Return Rate by Category",
                labels={return_col_fixed: "Average Return Rate", "Review_Level": "Review Level"}
            )
            fig.update_traces(line=dict(width=2))
            st.plotly_chart(fig, use_container_width=True)
            st.download_button("📥 Download data (CSV)", data=review_return.to_csv(index=False).encode("utf-8"), file_name="review_return_by_category.csv")
            st.dataframe(review_return)

            with st.expander("Insight Summary"):
                st.write("The relationship between Reviews and Return is strong across categories, especially for Women’s products, where low satisfaction significantly increases return rates.")
            with st.expander("Recommendation Summary"):
                st.write("Focus on addressing the 59% return rate for Women’s Clothing and Footwear under low satisfaction by improving product quality, fit accuracy, or expectation alignment.")

    # 3) Interaction of Income_Level and Product Category on return rates
    elif question.startswith("3️⃣ Interaction of Income_Level"):
        st.header("Return Rate by Income Level and Product Category (Heatmap)")
        # Clean, fixed-column implementation uses 'product_category', 'Income', 'Return'
        prod_cat_col = "product_category"
        income_col_fixed = "Income"
        return_col_fixed = "Return"

        missing_cols = [c for c in [prod_cat_col, income_col_fixed, return_col_fixed] if c not in data.columns]
        if missing_cols:
            st.warning("Missing columns for this analysis: " + ", ".join(missing_cols))
        else:
            tmp = data.copy()
            if "Income_Category" not in tmp.columns:
                tmp = ensure_income_category(tmp, income_col_fixed)

            income_category_return = (
                tmp.groupby(["Income_Category", prod_cat_col])[return_col_fixed]
                .mean()
                .reset_index()
            )

            fig = px.density_heatmap(
                income_category_return,
                x="Income_Category",
                y=prod_cat_col,
                z=return_col_fixed,
                color_continuous_scale="RdYlBu_r",
                title="Return Rate by Income Level and Product Category",
                labels={return_col_fixed: "Return Rate"}
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(income_category_return)
            st.download_button("📥 Download data (CSV)", data=income_category_return.to_csv(index=False).encode("utf-8"), file_name="income_category_return.csv")

            with st.expander("Insight Summary"):
                st.write("""
                - Very High income customers drive the highest return rates, particularly for Bags (up to 20%) and Home and Kitchen (18–20%), indicating their significant influence on returns.
                - Bags show elevated return rates across both Medium and Very High income groups, suggesting sensitivity to expectations or product quality.
                - Home and Kitchen also experience high returns (18–20%) among Very High income buyers, showing they are a critical segment in this category.
                - The findings highlight that Very High income customers are a key driver of elevated return rates, especially within Bags and Home and Kitchen.
                """)
            with st.expander("Recommendation Summary"):
                st.write("""
                - Recognize Very High income customers as a high-value segment and develop retention strategies such as improved customer experience, enhanced quality assurance, and dedicated post-purchase support.
                """)

    # 4) Return Rate by Tax Level for each Product Subcategory
    elif question.startswith("4️⃣ Return Rate by Tax Level"):
        st.header("Return Rate by Tax Level for each Product Subcategory")
        if tax_col and product_subcat_col:
            tmp = data.copy()
            tmp = ensure_tax_level(tmp, tax_col)
            tax_sub_return = (
                tmp.groupby(["Tax_Level", product_subcat_col])[return_col]
                .mean()
                .reset_index()
                .sort_values("Return", ascending=False)
            )
            tax_sub_return_display = tax_sub_return.copy()
            tax_sub_return_display[return_col] = tax_sub_return_display[return_col] * 100
            fig = px.bar(
                tax_sub_return_display,
                x=product_subcat_col,
                y=return_col,
                color="Tax_Level",
                barmode="group",
                text=tax_sub_return_display[return_col].round(1).astype(str) + '%',
                title="Return Rate by Tax Level and Product Subcategory",
                labels={return_col: "Return Rate (%)", product_subcat_col: "Product Subcategory"}
            )
            fig.update_traces(textposition='outside')
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            st.download_button("📥 Download data (CSV)", data=tax_sub_return.to_csv(index=False).encode("utf-8"), file_name="tax_sub_return.csv")
            st.dataframe(tax_sub_return_display)

            with st.expander("Insight Summary"):
                st.write("- Mobiles under the High tax level show the highest return rate at 24%, indicating a strong link between increased tax and higher return rates in this subcategory.")
                st.write("- Women’s products (19–20%) and Furnishing/Kitchen (15–19%) also have elevated returns under high tax levels.")
                st.write("- Women’s category shows consistently high return rates (19–20%) across all tax levels, indicating a persistent product issue independent of tax.")
                st.write("- High tax levels overall are associated with higher product returns, especially for Mobiles and Women’s subcategories.")
            with st.expander("Recommendation Summary"):
                st.write("- Prioritize investigating Mobiles with a 24% return rate under High tax—evaluate perceived value, product quality, and customer expectations.")
                st.write("- Launch a pilot with tax adjustments, improved warranties, or bundled value offers to reduce the high return rate observed in Mobiles.")
        else:
            st.warning("Tax column or Product_Subcategory column missing.")

    else:
        st.info("Choose a multivariate question from the sidebar.")

# ================== FINAL INSIGHTS & RECOMMENDATIONS ==================
with st.expander(" ", expanded=False):  # final polished summary & recommendations
    st.markdown("""
        <div style='text-align:center; padding:10px 0;'>
            <h1 style='color:#1565C0; font-size:36px; font-weight:800; letter-spacing:1px;'>
                 Final Summary & Recommendations
            </h1>
            <hr style='border:2px solid #1565C0; width:60%; margin:auto;'>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='font-size:17px; line-height:1.8; text-align:justify; color:white;'>

    ###  <span style='color:#90CAF9;'>Overall Insights Summary</span>

    • **Income & Product Category:**  
      Very High income customers show the highest return rates, especially for Bags and Home & Kitchen.  
      Medium and Very High income groups contribute noticeably to Bags return rates.  

    • **Reviews:**  
      Low satisfaction customers drive high return rates—up to 59% for Women’s Bags, 55% for Clothing, 52% for Footwear.  
      High satisfaction customers have minimal returns (~3%), showing the importance of quality and fit.

    • **Tax Levels:**  
      Mobiles under High tax show 24% return rate. Women’s products and Furnishing/Kitchen also show elevated returns under high tax levels.

    <br>
    <hr style='margin:10px 0;'>

    ###  <span style='color:#81C784;'>Strategic Recommendations / Action Plan</span>

    1. **Focus on Women’s Bags:** Fix the 59% return rate for low satisfaction by improving quality and fit. Add clear size guides and let customers try before buying.

    2. **Improve Women’s Clothing and Footwear:** Cut the 55% and 52% returns for low satisfaction with better designs and easy return options. Offer fit advice in stores.

    3. **Boost Women’s Home and Kitchen:** Lower the 50% return rate for low satisfaction by checking product quality and giving simple use instructions.

    4. **Help with Mobiles:** Reduce the 24% return rate for low satisfaction in Electronics by offering strong warranties and quick tech support.

    5. **Target High Tax and Income Issues:** For items like Mobiles (24% at high tax) and Bags (20% for Very High income), test lower taxes or discounts to keep customers happy.

    6. **Use Happy Customers:** Learn from the 3% return rate with high satisfaction—share good designs and service tips across all products.

    7. **Start a Big Test:** Run a pilot program with fit checks, surveys, and better support for low-satisfaction customers, especially for Women’s products and high-tax items, to find and fix problems fast.

    8. **Collect Data on Returned Products:** Gather info from all returned items in every category using surveys, logs, or feedback forms. Common causes include sizing/fit issues, damaged/defective products, unmet expectations, and shipping damage. Use this data to fix problems, such as better size guides for clothing/bags, stronger packaging for electronics/home items, and clear descriptions for books.

    <br>
    <hr style='margin:10px 0;'>

    ###  <span style='color:#FFCDD2;'>Key Takeaway</span>
    <b>Returns are driven by product quality, fit, customer satisfaction, and high tax or income-sensitive items.</b>  
    Reducing returns requires <b>proactive quality control, better sizing guides, improved support, and targeted promotions</b> for high-risk segments.
    </div>
    """, unsafe_allow_html=True)

    st.success("✅ This summary unifies insights and actionable recommendations from all analyses for strategic decision-making.")
