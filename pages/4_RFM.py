import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

st.set_page_config(page_title="RFM Analysis", layout="wide")
st.title("RFM (Recency, Frequency, Monetary) Analysis")
st.markdown("---")

@st.cache_data
def load_rfm():
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
    rfm_df = load_rfm()
    scaler = joblib.load("models/scaler.pkl")
    kmeans = joblib.load("models/kmeans.pkl")
    
    rfm_scaled = scaler.transform(rfm_df[['Recency', 'Frequency', 'Monetary']])
    rfm_df['Cluster'] = kmeans.predict(rfm_scaled)
    
    cluster_labels = {0: 'At-Risk', 1: 'Champions', 2: 'Loyal', 3: 'Casual'}
    rfm_df['Segment'] = rfm_df['Cluster'].map(cluster_labels)

    col1, col2 = st.columns(2)
    seg_counts = rfm_df['Segment'].value_counts().reset_index()
    seg_counts.columns = ['Segment', 'Count']


    with col1:
        st.subheader("Recency vs Revenue")
        fig_rec_rev = px.scatter(rfm_df, x='Recency', y='Monetary', log_y=True, hover_data=['Frequency'])
        st.plotly_chart(fig_rec_rev, use_container_width=True)

    with col2:
        st.subheader("Frequency vs Revenue")
        fig_freq_rev = px.scatter(rfm_df, x='Frequency', y='Monetary', log_x=True, log_y=True, hover_data=['Recency'])
        st.plotly_chart(fig_freq_rev, use_container_width=True)

    st.markdown("---")

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("RFM Segmentation Count")
        segment_counts = rfm_df["Segment"].value_counts().reset_index()
        segment_counts.columns = ["Segment", "Customers"]
        fig_box = px.bar(segment_counts,
                        x="Segment",
                        y="Customers",
                        color="Customers",
                        title="Customer Segments",
                        log_y=True
                        )
        st.plotly_chart(fig_box, use_container_width=True)

    with col4:
        st.subheader("Correlation Heatmap")
        corr_matrix = rfm_df[['Recency', 'Frequency', 'Monetary']].corr()
        fig_corr, ax = plt.subplots(figsize=(5, 4))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
        st.pyplot(fig_corr)

except FileNotFoundError:
    st.error("Model artifacts not found in `models/` directory.")