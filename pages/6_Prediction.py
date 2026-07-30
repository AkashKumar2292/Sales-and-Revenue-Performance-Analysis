import streamlit as st
import numpy as np
import joblib

st.set_page_config(page_title="Revenue Prediction", layout="wide")

st.title("Sales & Revenue Prediction")
st.markdown("Predict transaction revenue based on item, region, and time factors.")
st.markdown("---")

# --- Exact Mappings from Training Data ---
MONTH_MAP = {
    "April": 0, "August": 1, "December": 2, "February": 3, "January": 4, 
    "July": 5, "June": 6, "March": 7, "May": 8, "November": 9, 
    "October": 10, "September": 11
}

DAY_MAP = {
    "Friday": 0, "Monday": 1, "Sunday": 2, "Thursday": 3, "Tuesday": 4, "Wednesday": 5
}

COUNTRY_MAP = {
    "Australia": 0, "Austria": 1, "Bahrain": 2, "Belgium": 3, "Brazil": 4, 
    "Canada": 5, "Channel Islands": 6, "Cyprus": 7, "Czech Republic": 8, 
    "Denmark": 9, "EIRE": 10, "European Community": 11, "Finland": 12, 
    "France": 13, "Germany": 14, "Greece": 15, "Iceland": 16, "Israel": 17, 
    "Italy": 18, "Japan": 19, "Lebanon": 20, "Lithuania": 21, "Malta": 22, 
    "Netherlands": 23, "Norway": 24, "Poland": 25, "Portugal": 26, "RSA": 27, 
    "Saudi Arabia": 28, "Singapore": 29, "Spain": 30, "Sweden": 31, 
    "Switzerland": 32, "USA": 33, "United Arab Emirates": 34, "United Kingdom": 35, 
    "Unspecified": 36
}

# --- Ordered Lists for UI ---
ORDERED_MONTHS = [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"
]

ORDERED_DAYS = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Sunday"
] # Saturday excluded as it is not in the training data

@st.cache_resource
def load_model():
    try:
        rf_model = joblib.load("models/random_forest.pkl")
        return rf_model
    except Exception:
        return None

rf_model = load_model()

if rf_model is None:
    st.warning("Model not found. Ensure `random_forest.pkl` is in `models/`.")
else:
    with st.form("prediction_form"):
        st.subheader("Enter Transaction Details")
        col1, col2 = st.columns(2)
        
        with col1:
            quantity = st.number_input("Quantity", min_value=1, value=10, step=1)
            unit_price = st.number_input("Unit Price ($)", min_value=0.0, value=2.50, step=0.1)
            hour = st.slider("Hour of Day", min_value=0, max_value=23, value=12, step=1)

        with col2:
            country = st.selectbox("Country", options=list(COUNTRY_MAP.keys()), index=list(COUNTRY_MAP.keys()).index("United Kingdom"))
            
            # Pass the ordered lists to the options
            month = st.selectbox("Month", options=ORDERED_MONTHS)
            day = st.selectbox("Day", options=ORDERED_DAYS)

        submit_button = st.form_submit_button(label="Predict Revenue")

    if submit_button:
        try:
            # Look up the correct integer based on the user's text selection
            c_enc = COUNTRY_MAP[country]
            m_enc = MONTH_MAP[month]
            d_enc = DAY_MAP[day]

            # Construct the input array strictly matching: ['Quantity', 'UnitPrice', 'Country', 'Month', 'Day', 'Hour']
            input_data = [[quantity, unit_price, c_enc, m_enc, d_enc, hour]]
                
            # Make prediction directly
            prediction = rf_model.predict(input_data)[0]

            st.success(f"### Predicted Revenue: ${prediction:,.2f}")
            
        except Exception as e:
            st.error(f"Prediction Error: {e}")