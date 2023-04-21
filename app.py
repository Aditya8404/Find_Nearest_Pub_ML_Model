import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Find Your Pub", layout="wide")

# Load the dataset
data = pd.read_csv('open_pubs.csv')

# Rename the columns
data.columns = ['fsa_id', 'name', 'address', 'postcode', 'easting', 'northing', 'latitude', 'longitude', 'local_authority']

# Remove rows with null latitude and longitude values
data.dropna(subset=['latitude', 'longitude'], inplace=True)

st.write("""
    # Welcome to the Pub Finder App

    This app allows you to explore pub locations and find the nearest pubs to your location.
""")

# Show basic statistics about the dataset
st.write('Number of pubs:', len(data))
st.write('Number of unique local authorities:', len(data['local_authority'].unique()))
