import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

df = pd.read_csv("Airbnb_Open_Data.csv", low_memory=False)



dfClean = df.dropna(subset=['price','long','lat', 'neighbourhood', 'neighbourhood group', 'room type',
                            'number of reviews', 'availability 365', 'calculated host listings count',
                            'house_rules', 'instant_bookable', 'NAME', 'host_identity_verified']).copy()  # Create a copy

# Clean the price column: remove '$' and ',' then convert to numeric
dfClean['price'] = dfClean['price'].replace({'\\$': '', ',': ''}, regex=True)
dfClean['price'] = pd.to_numeric(dfClean['price'], errors='coerce')

print(dfClean['price'].max())



# Sidebar Filters
st.sidebar.header("Filters")
selected_neighborhoods = st.sidebar.multiselect("Select Neighborhood(s)", df['neighbourhood group'].unique())

priceLower = st.number_input("Price Lower Limit:",value=250)
priceHigher = st.number_input("Price Upper Limit:",value=500)

dfClean = dfClean[dfClean['price'] >= priceLower]
dfClean = dfClean[dfClean['price'] <= priceHigher]


for hoods in selected_neighborhoods:
    if selected_neighborhoods:
        dfClean = dfClean[dfClean['neighbourhood group'] == hoods]

st.map(dfClean, latitude="lat", longitude="long")



# Show raw data
st.subheader("Raw Data")
st.write(dfClean)

# Select columns to display



