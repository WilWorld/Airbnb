import pandas as pd

# Load the dataset
df = pd.read_csv('Airbnb_Open_Data.csv', low_memory=False)

# Clean the dataset by dropping rows with missing critical values
dfClean = df.dropna(subset=['price', 'neighbourhood', 'neighbourhood group', 'room type', 
                            'number of reviews', 'availability 365', 'calculated host listings count', 
                            'house_rules', 'instant_bookable', 'NAME', 'host_identity_verified']).copy()  # Create a copy

# Clean the price column: remove '$' and ',' then convert to numeric
dfClean['price'] = dfClean['price'].replace({'\\$': '', ',': ''}, regex=True)
dfClean['price'] = pd.to_numeric(dfClean['price'], errors='coerce')

# 1. Average price per neighborhood
avg_price_neighborhood = dfClean.groupby('neighbourhood')['price'].mean().sort_values(ascending=False).round(2)
print("Average Price per Neighborhood:")
print(avg_price_neighborhood)

# 2. Number of reviews per room type
reviews_per_room_type = dfClean.groupby('room type')['number of reviews'].sum().sort_values(ascending=False).round(1)
print("\nNumber of Reviews per Room Type:")
print(reviews_per_room_type)

# 3. Availability trends across boroughs
availability_by_borough = dfClean.groupby('neighbourhood group')['availability 365'].mean().round(0)
print("\nAvailability Trends Across Boroughs:")
print(availability_by_borough)

# 4. Host listing distribution (small vs. large-scale hosts)
dfClean['host_category'] = dfClean['calculated host listings count'].apply(lambda x: 'Small' if x <= 5 else 'Large')
host_distribution = dfClean.groupby('host_category')['host_identity_verified'].count()
print("\nHost Listing Distribution (Small vs. Large-Scale Hosts):")
print(host_distribution)
