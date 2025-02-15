import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

df = pd.read_csv("Airbnb_Open_Data.csv")



df = df.dropna(subset=["instant_bookable"])
df = df.dropna(subset=["host_identity_verified"])
df = df.dropna(subset=["NAME"])
df = df.dropna(subset=["neighbourhood group"])
df = df.dropna(subset=["host name"])
df = df.dropna(subset=["cancellation_policy"])
df = df.dropna(subset=["long"])
df = df.dropna(subset=["lat"])
df = df.dropna(subset=["price"])


st.map(df, latitude="lat", longitude="long", size="price" )


# Show raw data
st.subheader("Raw Data")
st.write(df)

# Select columns to display



columns = st.multiselect("Select columns to display", df.columns, default=df.columns)


# Filter data based on user input
column_to_filter = st.selectbox("Select column to filter", df.columns)
unique_values = df[column_to_filter].unique()
selected_value = st.selectbox("Select value", unique_values)

# Filtered Data
filtered_df = df[df[column_to_filter] == selected_value][columns]

st.subheader("Filtered Data")
st.write(filtered_df)

# Show basic statistics
st.subheader("Basic Statistics")
st.write(df.describe())

# Create a simple visualization
st.subheader("Data Visualization")
column_to_plot = st.selectbox("Select column to plot", df.columns)
st.bar_chart(df[column_to_plot].value_counts())

#Clean the dataset by dropping rows with missing critical values
