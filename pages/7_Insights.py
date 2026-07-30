import streamlit as st

st.set_page_config(page_title="Business Insights", layout="wide")

st.title("Strategic Business Insights")
st.markdown("Actionable recommendations derived from EDA, RFM, and ML processes.")
st.markdown("---")

st.markdown("""
### Market Trends
* **Geographical Dominance:** The UK drives the highest volume, but secondary markets provide significant high-value opportunities.
* **Peak Timing:** Focus marketing blasts and server stability during mid-day hours and Q4 months (November & December).

### Customer Strategies
* **At-Risk Interventions:** Single-purchase dormant users form the largest segment. Automated email campaigns featuring deep discounts are required to prevent hard churn.
* **Loyalty Perks:** 'Champions' provide extreme ROI compared to their group size. Create exclusive tiers, free shipping thresholds, and early product access to maximize their Lifetime Value (LTV).
""")