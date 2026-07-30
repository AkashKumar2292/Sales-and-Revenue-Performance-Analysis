import streamlit as st
st.set_page_config(
    page_title="Retail Analytics Dashboard",
    layout="wide"
)

st.title("Sales & Revenue Performance Analysis")
st.markdown("---")

st.markdown("""
### Project Overview
Welcome to the Interactive Retail Analytics Dashboard. This project demonstrates an end-to-end Data Science pipeline using the Online Retail Dataset.

**Navigate using the sidebar to explore:**
*   **Dashboard:** High-level KPIs and Dataset overview.
*   **Sales Analysis:** In-depth look at order volume trends over time.
*   **Revenue Analysis:** Breakdown of monetary generation by product, country, and time.
*   **RFM Analysis:** Customer segmentation metrics (Recency, Frequency, Monetary).
*   **K-Means Clustering:** Machine learning segments grouping customers into VIPs, Loyalists, and At-Risk profiles.
*   **Prediction:** Random Forest model to forecast daily quantity sold based on input parameters.
*   **Insights & Recommendations:** Actionable business strategies derived from the data.
""")

st.info("Select a module from the left sidebar to begin.")