import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Analysis", layout="wide")
st.title("Sales Performance Analysis")
st.markdown("---")

@st.cache_data
def load_data():
    df = pd.read_excel("data/Online_Retail.xlsx")
    df = df.dropna(subset=['CustomerID'])
    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] >= 1]
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    df['Month_Year'] = df['InvoiceDate'].dt.to_period('M').astype(str)
    df['Day'] = df['InvoiceDate'].dt.day_name()
    df['Hour'] = df['InvoiceDate'].dt.hour
    return df

df = load_data()

# 1. Monthly Revenue Analysis
st.subheader("Monthly Revenue Analysis")
monthly_rev = df.groupby('Month_Year')['Revenue'].sum().reset_index()
fig_m_rev = px.line(monthly_rev, x='Month_Year', y='Revenue', markers=True)
fig_m_rev.update_yaxes(tickprefix="$")
st.plotly_chart(fig_m_rev, use_container_width=True)

st.markdown("---")

col1, col2 = st.columns(2)

# 2. Sales by Days
with col1:
    st.subheader("Sales Volume by Days")
    day_sales = df.groupby('Day')['InvoiceNo'].nunique().reset_index()
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_sales['Day'] = pd.Categorical(day_sales['Day'], categories=days_order, ordered=True)
    day_sales = day_sales.sort_values('Day')
    fig_day = px.bar(day_sales, x='Day', y='InvoiceNo', color='InvoiceNo', color_continuous_scale='Blues')
    st.plotly_chart(fig_day, use_container_width=True)

# 3. Sales by Hours
with col2:
    st.subheader("Sales Volume by Hours")
    hourly_sales = df.groupby('Hour')['InvoiceNo'].nunique().reset_index()
    fig_hour = px.line(hourly_sales, x='Hour', y='InvoiceNo', markers=True)
    fig_hour.update_xaxes(dtick=1)
    st.plotly_chart(fig_hour, use_container_width=True)