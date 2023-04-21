import numpy as np
import pandas as pd
import streamlit as st
import folium
from sklearn.metrics.pairwise import euclidean_distances

# Load the dataset
data = pd.read_csv('open_pubs.csv')

# Rename the columns
data.columns = ['fsa_id', 'name', 'address', 'postcode', 'easting', 'northing', 'latitude', 'longitude', 'local_authority']

# Remove rows with null latitude and longitude values
# data.dropna(subset=['latitude', 'longitude'], inplace=True)

data.replace('\\N', np.nan, inplace=True)
data.dropna(inplace=True)
data.latitude = data.latitude.astype(float)
data.longitude = data.longitude.astype(float)


# Define function to find nearest pubs
def find_nearest_pubs(data, location, num_pubs):
    # Compute Euclidean distances between location and each pub
    distances = euclidean_distances(data[['latitude', 'longitude']], [location]).flatten()

    # Sort the distances and get the indices of the closest pubs
    closest_indices = distances.argsort()[:num_pubs]

    # Get the data for the closest pubs
    closest_pubs = data.iloc[closest_indices]

    # Create a folium map centered at the location
    m = folium.Map(location=location, zoom_start=10)

    # Add markers for the closest pubs
    for index, row in closest_pubs.iterrows():
        folium.Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(m)

    # Return the map
    return m



st.write("""
        # Find the Nearest Pub

        Enter your latitude and longitude to find the nearest pubs.
    """)

# Get the user's location
lat = st.number_input('Latitude', value=51.5, step=0.01, format="%.6f")
lon = st.number_input('Longitude', value=-0.1, step=0.01, format="%.6f")

# Calculate the Euclidean distance between the user's location and each pub's location
distances = np.sqrt((data['latitude'] - lat)**2 + (data['longitude'] - lon)**2)

# Sort the dataframe by distance in ascending order
data['distance'] = distances
df = data.sort_values(by='distance')

# Display the nearest 5 pubs on the map
st.map(df.head(5))