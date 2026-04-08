# 3_recommendations.py
# Fresco Retail — Strategic Recommendations

import streamlit as st

st.set_page_config(page_title="Recommendations", layout="wide")

# ========== PAGE HEADER ==========

st.title("Strategic Recommendations")
st.caption(
    "Actionable plans derived from return rate analysis across product categories, "
    "income segments, customer satisfaction, and tax levels."
)
st.divider()

# ========== KEY TAKEAWAY (always visible at the top) ==========

st.info(
    "Returns are driven by three root causes: product quality & fit issues, "
    "low customer satisfaction, and high-tax or high-income segment sensitivity. "
    "The recommendations below address each root cause directly."
)

st.divider()

# ========== PRIORITY FILTER ==========

st.sidebar.header("Filter Recommendations")

priority_filter = st.sidebar.radio(
    "Show by priority",
    ["All", "High Priority", "Medium Priority"],
)

theme_filter = st.sidebar.radio(
    "Show by theme",
    ["All", "Women's Products", "Electronics", "Segment Strategy", "Process"],
)

st.sidebar.divider()
st.sidebar.caption(
    "Use the filters to focus on the recommendations most relevant to your team. "
    "All recommendations are derived from the Analytics & Insights analysis."
)

# ========== RECOMMENDATION DATA ==========
# Each recommendation is a dict so it can be filtered and rendered uniformly.

recommendations = [
    {
        "id": 1,
        "priority": "High Priority",
        "theme": "Women's Products",
        "title": "Women's Bags — Fix the 59% Return Rate",
        "metric": "59%",
        "metric_label": "Return rate (low satisfaction)",
        "context": (
            "Women's Bags under low customer satisfaction have the highest return rate in the entire dataset at 59%. "
            "This is far above the overall average and signals a clear product-quality or expectation problem."
        ),
        "actions": [
            "Audit the top-returned Bag SKUs for quality defects, material issues, or misleading product descriptions.",
            "Add detailed size guides, material composition, and real-photo galleries to all Bags product pages.",
            "Introduce a pre-purchase fit or style consultation for high-value Bag items.",
            "Collect structured return reasons at point-of-return to identify the primary driver quickly.",
        ],
    },
    {
        "id": 2,
        "priority": "High Priority",
        "theme": "Women's Products",
        "title": "Women's Clothing & Footwear — Reduce 55% and 52% Return Rates",
        "metric": "55% / 52%",
        "metric_label": "Return rates (low satisfaction)",
        "context": (
            "Women's Clothing (55%) and Footwear (52%) return rates under low satisfaction are consistently among "
            "the highest across all subcategories. Both are driven by fit, sizing, and unmet expectations."
        ),
        "actions": [
            "Implement dynamic sizing recommendations based on customer purchase history.",
            "Display fit feedback from previous buyers (e.g., 'runs small', 'true to size') prominently on product pages.",
            "Train in-store staff on fit consultations for Women's Clothing and Footwear.",
            "Add easy exchange options as an alternative to returns to reduce net return volume.",
        ],
    },
    {
        "id": 3,
        "priority": "High Priority",
        "theme": "Women's Products",
        "title": "Women's Home and Kitchen — Address 50% Return Rate",
        "metric": "50%",
        "metric_label": "Return rate (low satisfaction)",
        "context": (
            "Women's Home and Kitchen products show a 50% return rate among low satisfaction customers. "
            "This suggests product descriptions, usage expectations, or quality are not aligned with what buyers receive."
        ),
        "actions": [
            "Review product descriptions for accuracy — ensure dimensions, materials, and use cases are clearly stated.",
            "Add usage videos or how-to guides for complex items (appliances, kitchen tools).",
            "Follow up with customers after delivery to identify dissatisfaction before a return is initiated.",
        ],
    },
    {
        "id": 4,
        "priority": "High Priority",
        "theme": "Electronics",
        "title": "Mobiles — Tackle 24% Return Rate Under High Tax",
        "metric": "24%",
        "metric_label": "Return rate (High tax segment)",
        "context": (
            "Mobiles show a 24% return rate under the High tax level — the highest of any subcategory in the tax analysis. "
            "High-tax items face a perceived value gap: customers pay more and expect more, making them quicker to return."
        ),
        "actions": [
            "Introduce a 14-day no-questions exchange policy for Mobiles to redirect returns into exchanges.",
            "Bundle Mobiles with warranty extensions or accessories to improve perceived value.",
            "Create a dedicated Mobile technical support channel (chat or call) to resolve post-purchase issues before return.",
            "Run a pricing sensitivity test: does reducing margin on high-tax Mobile SKUs reduce return rates?",
        ],
    },
    {
        "id": 5,
        "priority": "Medium Priority",
        "theme": "Segment Strategy",
        "title": "Very High Income Customers — High Value, High Risk Segment",
        "metric": "14%",
        "metric_label": "Overall return rate (Very High income)",
        "context": (
            "Very High income customers return at 14% — well above other income groups. "
            "They show particularly high return rates for Bags (20%) and Home & Kitchen (18–20%). "
            "This segment has high lifetime value but elevated expectations around product quality and service."
        ),
        "actions": [
            "Assign a dedicated post-purchase support experience for Very High income customers.",
            "Proactively follow up within 48 hours of delivery to address any issues before a return is filed.",
            "Review Bags and Home & Kitchen quality standards to ensure they match premium buyer expectations.",
            "Offer personalized loyalty incentives to retain this segment even when they experience issues.",
        ],
    },
    {
        "id": 6,
        "priority": "Medium Priority",
        "theme": "Segment Strategy",
        "title": "High Tax Segments — Improve Perceived Value",
        "metric": "15–24%",
        "metric_label": "Return rates across high-tax subcategories",
        "context": (
            "Across multiple subcategories — Mobiles (24%), Women's products (19–20%), Furnishing/Kitchen (15–19%) — "
            "High tax is associated with elevated return rates. The tax burden raises the effective price and "
            "heightens customer expectations, creating a gap that leads to returns."
        ),
        "actions": [
            "Test bundled value offers (extended warranty, free delivery, accessories) on high-tax SKUs to justify the price.",
            "Make tax amounts transparent on product pages so customers understand the total cost upfront.",
            "Identify which high-tax SKUs have the highest return rates and prioritize quality reviews for those specific items.",
        ],
    },
    {
        "id": 7,
        "priority": "Medium Priority",
        "theme": "Process",
        "title": "Pilot Program — Test and Learn at Scale",
        "metric": "—",
        "metric_label": "Operational initiative",
        "context": (
            "Rather than rolling out all changes at once, a controlled pilot allows the team to measure the impact "
            "of specific interventions — fit guides, post-purchase surveys, enhanced support — before scaling."
        ),
        "actions": [
            "Select 2–3 high-return subcategories (e.g., Women's Bags, Mobiles) as pilot categories.",
            "Implement one targeted intervention per category (fit guide, exchange policy, proactive support).",
            "Measure return rate before and after over a 60-day window.",
            "Use results to prioritize which interventions to roll out across all categories.",
        ],
    },
    {
        "id": 8,
        "priority": "Medium Priority",
        "theme": "Process",
        "title": "Return Data Collection — Build a Feedback Loop",
        "metric": "—",
        "metric_label": "Data infrastructure initiative",
        "context": (
            "Currently, root causes of returns are inferred from return rates. "
            "Without structured return reason data, it is difficult to distinguish between sizing issues, "
            "quality defects, unmet expectations, and shipping damage."
        ),
        "actions": [
            "Implement a mandatory return reason form at point-of-return (in-store and online).",
            "Categorize return reasons into: sizing, defect, expectation mismatch, shipping damage, changed mind.",
            "Review return reason data monthly and feed findings into product and process improvement cycles.",
            "Connect return reason data to the prediction model as an additional feature in the next model iteration.",
        ],
    },
]

# ========== FILTER LOGIC ==========

filtered = recommendations

if priority_filter != "All":
    filtered = [r for r in filtered if r["priority"] == priority_filter]

if theme_filter != "All":
    filtered = [r for r in filtered if r["theme"] == theme_filter]

# ========== RESULTS COUNT ==========

total = len(filtered)
if total == 0:
    st.warning("No recommendations match the selected filters. Adjust the sidebar filters to see results.")
    st.stop()

st.markdown(f"Showing **{total}** recommendation{'s' if total != 1 else ''}")
st.divider()

# ========== RENDER RECOMMENDATIONS ==========

PRIORITY_COLOR = {
    "High Priority":   st.error,
    "Medium Priority": st.warning,
}

for rec in filtered:

    with st.container():

        # --- Header row: metric on the right, title on the left ---
        head_col, metric_col = st.columns([3, 1], gap="large")

        with head_col:
            PRIORITY_COLOR.get(rec["priority"], st.info)(
                f"{rec['priority']}   |   {rec['theme']}"
            )
            st.subheader(rec["title"])

        with metric_col:
            st.metric(label=rec["metric_label"], value=rec["metric"])

        # --- Context ---
        st.markdown("**Why this matters**")
        st.write(rec["context"])

        # --- Actions ---
        st.markdown("**What to do**")
        for action in rec["actions"]:
            st.markdown(f"- {action}")

    st.divider()

# ========== BOTTOM KEY TAKEAWAY ==========

with st.container():
    st.subheader("Key Takeaway")
    st.info(
        "Women's products and high-tax items are the highest-priority areas. "
        "Focus on fit, quality, and post-purchase support for Women's categories, "
        "and on perceived value and exchange policies for high-tax segments like Mobiles. "
        "A structured return reason feedback loop will accelerate all future improvements."
    )