# Sales and Revenue Performance Analysis

## Project Overview
This repository contains an end-to-end data science project featuring RFM customer segmentation via K-Means clustering, sales demand forecasting using a Random Forest model, and an interactive Streamlit dashboard. It leverages the Online Retail Dataset to provide a full pipeline from exploratory data analysis to machine learning predictions.  

## Tech Stack
- `Frontend Application:` Streamlit.
- `Data Manipulation:` Pandas, NumPy, and Openpyxl.
- `Machine Learning & Visualization:` Scikit-Learn, Plotly, Seaborn, and Matplotlib.

## Key Features
- `KPI Dashboard:` Tracks high-level metrics including total revenue, order counts, customer volume, and average order value.
- `Sales & Revenue Analysis:` Visualizes performance trends by month, day, and hour, alongside country-wise revenue distributions.
- `RFM Segmentation:` Calculates Recency, Frequency, and Monetary metrics to understand purchasing behavior.
- `K-Means Clustering:` Employs machine learning to group customers into actionable segments like At-Risk, Champions, Loyal, and Casual.
- `Revenue Prediction:` Features a Random Forest model that forecasts transaction revenue based on specific item, region, and time inputs.
- `Business Insights:` Delivers strategic recommendations based on geographical dominance, peak timing, and customer loyalty strategies.
  
## Dataset
The data for this application is stored in the local data/ directory.
- `Source File:` The dashboard relies on data/Online_Retail.xlsx to render the visualizations and calculate metrics.
- `Data Processing:` The raw data is dynamically loaded, cleaned (removing missing Customer IDs and filtering out negative quantities/prices), and transformed directly within the Streamlit application before being passed to the visualizations and models. 
