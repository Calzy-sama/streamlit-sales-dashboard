import streamlit as st
import pandas as pd
import plotly.express as px

# Load data with error handling
try:
    df = pd.read_csv("sales data.csv")
except FileNotFoundError:
    st.error("CSV file 'sales data.csv' not found. Please ensure the file is in the correct directory.")
    st.stop()

# App title
st.title("Interactive Sales Dashboard")

# Convert columns to numeric, coercing errors
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

# Sidebar filters
st.sidebar.header("Filter the data")

countries = st.sidebar.multiselect("Select Country", df['Country'].dropna().unique(), default=df['Country'].dropna().unique())
years = st.sidebar.multiselect("Select Year", df['Year'].dropna().unique(), default=df['Year'].dropna().unique())

# Filtered data
filtered_df = df[(df['Country'].isin(countries)) & (df['Year'].isin(years))]

# Display filtered data
st.subheader("Filtered Data")
st.dataframe(filtered_df)

# Line chart - Sales Trend
st.subheader("Sales Trend Over Time")
fig = px.line(
    filtered_df,
    x='Year',
    y='Value',
    color='Country',
    markers=True,
    title='Sales over Time'
)
st.plotly_chart(fig)

# Bar chart - Sales by Country
bar_data = filtered_df.groupby('Country')['Value'].sum().reset_index()

st.subheader("Sales by Country")
bar_fig = px.bar(
    bar_data,
    x='Country',
    y='Value',
    color='Country',
    title='Sales Comparison'
)
st.plotly_chart(bar_fig)

# Footer
st.markdown("Data Source: World Bank")
