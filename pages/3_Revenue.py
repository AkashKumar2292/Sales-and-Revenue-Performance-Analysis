import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Revenue Analysis", layout="wide")
st.title("Revenue Drivers (Market & Customer)")
st.markdown("---")

@st.cache_data
def load_data():
    df = pd.read_excel("data/Online_Retail.xlsx")
    df = df.dropna(subset=['CustomerID'])
    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] >= 1]
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    df['CustomerID_Str'] = "Cust ID: " + df['CustomerID'].astype(int).astype(str)
    return df

df = load_data()

st.subheader("Country Wise Revenue")
country_rev = df.groupby('Country')['Revenue'].sum().reset_index()
country_rev = country_rev.sort_values('Revenue', ascending=False).head(10)
fig_c_rev = px.bar(country_rev, x='Revenue', y='Country', orientation='h', color='Revenue', color_continuous_scale='Greens')
fig_c_rev.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig_c_rev, use_container_width=True)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Customers (By Revenue)")
    top_customers = df.groupby('CustomerID_Str')['Revenue'].sum().reset_index()
    top_customers = top_customers.sort_values('Revenue', ascending=False).head(10)
    fig_top_c = px.bar(top_customers, x='Revenue', y='CustomerID_Str', orientation='h', color='Revenue', color_continuous_scale='Purples')
    fig_top_c.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_top_c, use_container_width=True)

with col2:
    st.subheader("Customer Purchase Frequency")
    freq_customers = df.groupby('CustomerID_Str')['InvoiceNo'].nunique().reset_index()
    freq_customers = freq_customers.sort_values('InvoiceNo', ascending=False).head(10)
    fig_freq_c = px.bar(freq_customers, x='InvoiceNo', y='CustomerID_Str', orientation='h', color='InvoiceNo', color_continuous_scale='Teal')
    fig_freq_c.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_freq_c, use_container_width=True)