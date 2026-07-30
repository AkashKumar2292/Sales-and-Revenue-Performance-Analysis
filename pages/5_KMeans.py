import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

st.set_page_config(page_title="Segmentation", layout="wide")
st.title("K-Means Customer Segmentation")
st.markdown("---")

@st.cache_data
def load_data():
    df = pd.read_excel("data/Online_Retail.xlsx")
    df = df.dropna(subset=['CustomerID'])
    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] >= 1]
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    reference_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (reference_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'Revenue': 'sum'
    }).reset_index()
    rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
    return rfm

try:
    rfm = load_data()
    scaler = joblib.load("models/scaler.pkl")
    kmeans = joblib.load("models/kmeans.pkl")
    
    rfm_scaled = scaler.transform(rfm[['Recency', 'Frequency', 'Monetary']])
    rfm['Cluster'] = kmeans.predict(rfm_scaled)
    
    cluster_labels = {0: 'At-Risk', 1: 'Champions', 2: 'Loyal', 3: 'Casual'}
    rfm['Segment'] = rfm['Cluster'].map(cluster_labels)

    col1, col2 = st.columns(2)
    seg_counts = rfm['Segment'].value_counts().reset_index()
    seg_counts.columns = ['Segment', 'Count']

    with col1:
        st.subheader("Customer Segment Distribution")
        fig_bar_dist = px.bar(seg_counts, x='Segment', y='Count', color='Segment')
        st.plotly_chart(fig_bar_dist, use_container_width=True)

    with col2:
        st.subheader("Customer Segment Pie Chart")
        fig_pie_dist = px.pie(seg_counts, values='Count', names='Segment', hole=0.4)
        st.plotly_chart(fig_pie_dist, use_container_width=True)

    st.markdown("---")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Revenue by Segment")
        seg_rev = rfm.groupby('Segment')['Monetary'].sum().reset_index()
        fig_rev_seg = px.bar(seg_rev, x='Segment', y='Monetary', color='Segment')
        fig_rev_seg.update_yaxes(tickprefix="$")
        st.plotly_chart(fig_rev_seg, use_container_width=True)
        
    with col4:
        st.subheader("K-Means Cluster Plot")
        fig_kmeans_scatter = px.scatter(rfm, x='Recency', y='Monetary', color='Segment', size='Frequency', log_y=True)
        st.plotly_chart(fig_kmeans_scatter, use_container_width=True)

    st.markdown("---")
    st.subheader("Average RFM by Segment")
    avg_rfm = rfm.groupby('Segment')[['Recency', 'Frequency', 'Monetary']].mean().round(2)
    st.dataframe(avg_rfm, use_container_width=True)

except FileNotFoundError:
    st.error("Model artifacts not found in `models/` directory.")