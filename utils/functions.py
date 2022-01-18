import streamlit as st
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim

from utils.dicts import concerned_variants


def lineages_to_concerned_variantes(df, variant_column):
    var = []
    for index, row in df.iterrows():
        if row[variant_column] in concerned_variants:
            var.append(row[variant_column])
        else:
            var.append('Other Lineages')
    return var

# Function to find the coordinate of a given code (city, alpha code or country) - coordinate results are related to the capital of the country
@st.cache
def findGeocode(location):
    try:
        geolocator = Nominatim(user_agent="covid_dashboard_africa")
        return geolocator.geocode(location)
    except GeocoderTimedOut:
        return findGeocode(location)