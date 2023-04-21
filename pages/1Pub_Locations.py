import numpy as np
import pandas as pd
import streamlit as st

# Load the dataset
data = pd.read_csv('open_pubs.csv')

# Rename the columns
data.columns = ['fsa_id', 'name', 'address', 'postcode', 'easting', 'northing', 'latitude', 'longitude', 'local_authority']

# Remove rows with null latitude and longitude values
data.replace('\\N', np.nan, inplace=True)
data.dropna(inplace=True)
data.latitude = data.latitude.astype(float)
data.longitude = data.longitude.astype(float)


st.write("""
        # Pub Locations

        Choose a postal code or local authority to display the pubs in the area.
    """)

# Get the chosen location
location_type = st.selectbox('Location type', ['Postal code', 'Local authority'])
if location_type == 'Postal code':
    location = st.text_input('Postal code', 'CO7 6LW')
    pub_data = data[data['postcode'] == location]
else:
    location = st.selectbox('Local authority', data['local_authority'].unique())
    pub_data = data[data['local_authority'] == location]

# Display the map of pubs in the chosen area
if len(pub_data) == 0:
    st.warning('No pubs found in the chosen location.')
else:
    st.write(f'Number of pubs in {location}:', len(pub_data))
    st.write('Map of pubs in the area:')
    st.map(pub_data[['latitude', 'longitude']])