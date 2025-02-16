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

dfClean = dfClean[dfClean['availability 365'] < 365].copy()


priceLower = dfClean['price'].min()
priceHigher = dfClean['price'].max()

# Sidebar Filters

st.sidebar.header("Filters")
room_type = st.sidebar.multiselect("Select Room Type", df['room type'].unique())
selected_neighbourhood = st.sidebar.multiselect("Select Neighbourhood(s)", df['neighbourhood group'].unique())
policy = st.sidebar.multiselect("Cancellation Policy", df['cancellation_policy'].unique())
booking = st.sidebar.checkbox("Instant Booking", df['instant_bookable'].unique)

PriceScale = st.slider("Price Range:",min_value=priceLower, max_value=priceHigher, value=(priceLower, priceHigher))
rating = st.sidebar.slider("Rating:",min_value=1, max_value=5, value=1)
pMin, pMax = PriceScale

dfClean = dfClean[dfClean['review rate number'] >= rating]

dfClean = dfClean[dfClean['price'] >= pMin]
dfClean = dfClean[dfClean['price'] <= pMax]

if room_type:
    dfClean = dfClean[dfClean['room type'].isin(room_type)]
if selected_neighbourhood:
    dfClean = dfClean[dfClean['neighbourhood group'].isin(selected_neighbourhood)]
if policy:
    dfClean = dfClean[dfClean['cancellation_policy'].isin(policy)]

dfClean = dfClean[dfClean['instant_bookable']]



st.map(dfClean, latitude="lat", longitude="long", size=5)


st.write("Showing " + str(len(dfClean)) + " listings :)")
# Show raw data
st.subheader("Raw Data")
st.write(dfClean)

# Select columns to display




