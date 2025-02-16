import streamlit as st
import pandas as pd


df = pd.read_csv("Airbnb_Open_Data.csv", low_memory=False)

dfClean = df.dropna(subset=['price','long','lat', 'neighbourhood', 'neighbourhood group', 'room type',
                            'number of reviews', 'availability 365','cancellation_policy', 'calculated host listings count',
                            'house_rules', 'instant_bookable', 'NAME', 'host_identity_verified']).copy()  # Create a copy

# Clean the price column: remove '$' and ',' then convert to numeric
dfClean['price'] = dfClean['price'].replace({'\\$': '', ',': ''}, regex=True)
dfClean['price'] = pd.to_numeric(dfClean['price'], errors='coerce')

st.title("Welcome to The New Yourk Airbnb Listings Website")
st.subheader("Configure the filters based on your preferences and find the listing that's right for you!")

st.audio("Welcome To New York.mp3", format="audio/mp3", autoplay=True)
st.write("Welcome To New York · Taylor Swift")
dfClean = dfClean[dfClean['availability 365'] < 365].copy()

priceLower = dfClean['price'].min()
priceHigher = dfClean['price'].max()

# Sidebar Filters

st.sidebar.header("Filters")
PriceScale = st.sidebar.slider("Price Range:",min_value=priceLower, max_value=priceHigher, value=(priceLower, priceHigher))

room_type = st.sidebar.multiselect("Select Room Type", df['room type'].unique())

selected_neighbourhood = st.sidebar.multiselect("Select Neighbourhood(s)", df['neighbourhood group'].unique())

policy = st.sidebar.multiselect("Cancellation Policy", df['cancellation_policy'].unique())

booking = st.sidebar.checkbox("Instant Booking", df['instant_bookable'].unique)

rating = st.sidebar.slider("Rating: (showing that rating and above)",min_value=1, max_value=5, value=3)

pMin, pMax = PriceScale

dfClean = dfClean[dfClean['review rate number'] >= rating]

dfClean = dfClean[dfClean['instant_bookable'] == booking]


dfClean = dfClean[dfClean['price'] >= pMin]
dfClean = dfClean[dfClean['price'] <= pMax]


if room_type:
    dfClean = dfClean[dfClean['room type'].isin(room_type)]
if selected_neighbourhood:
    dfClean = dfClean[dfClean['neighbourhood group'].isin(selected_neighbourhood)]
if policy:
    dfClean = dfClean[dfClean['cancellation_policy'].isin(policy)]


st.map(dfClean, latitude="lat", longitude="long", size=5)
st.subheader("Showing " + str(len(dfClean)) + " listings")

col1, col2 = st.columns(2)


# 1. Average price per neighborhood
with col1:
    avg_price_neighborhood = dfClean.groupby('neighbourhood')['price'].mean().sort_values(ascending=False).round(2)

    st.subheader("Average Price per Neighborhood:")
    st.dataframe(avg_price_neighborhood, height=300, width=600)

# 2. Number of reviews per room type
with col2:
    reviews_per_room_type = dfClean.groupby('room type')['number of reviews'].sum().sort_values(ascending=False).round(1)
    st.subheader("\nNumber of Reviews per Room Type:")
    st.dataframe(reviews_per_room_type,width=600)

col3, col4 = st.columns(2)

# 3. Availability trends across boroughs
with col3:
    availability_by_borough = dfClean.groupby('neighbourhood group')['availability 365'].mean().round(0)
    st.subheader("\nAvailability Trends Across Boroughs:")
    st.dataframe(availability_by_borough, width=600)

# 4. Host listing distribution (small vs. large-scale hosts)
with col4:
    dfClean['host_category'] = dfClean['calculated host listings count'].apply(lambda x: 'Small' if x <= 5 else 'Large')
    host_distribution = dfClean.groupby('host_category')['host_identity_verified'].count()
    st.subheader("\nHost Listing Distribution (Small vs. Large-Scale Hosts):")
    st.dataframe(host_distribution,width=600)


newDf = dfClean.drop(columns=['id','host id', 'lat','long','country','country code','license'])
st.subheader("Available Housing Listings:")
st.write(newDf)

st.write("Its been waiting for you...")





