import base64
import os
import streamlit as st

from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim

from utils.dicts import concerned_variants


def lineages_to_concerned_variants(df, variant_column):
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


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)


def icon(color, icon_name, label):
    return f'<i class="material-icons" style="color:{color}">{icon_name}</i>{label}'


def custom_legend(list_labels, color_dict, col):
    icon_name = "stop"
    html_icon = ""
    for item in list_labels:
        html_icon = html_icon + "  " + icon(color=color_dict.get(item), icon_name=icon_name, label=item)
    col.markdown(html_icon, unsafe_allow_html=True)

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache(allow_output_mutation=True)
def get_img_with_href(local_img_path, target_url):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}" target="_blank">
            <img src="data:image/{img_format};base64,{bin_str}" />
        </a>'''
    return html_code