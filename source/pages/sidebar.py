import streamlit as st
import pandas as pd

from utils.dicts import countries_regions
from utils.functions import get_img_with_href


def filter_countries(df_africa):
    # Filter by selected country
    countries = df_africa['country'].unique()
    selection = st.sidebar.radio("Select Countries to show", ("Show all countries", "Select region",
                                                              "Select one or more countries"))

    if selection == "Show all countries":
        countries_selected = df_africa['country'].unique()
        display_countries = "all countries in Africa continent"
    elif selection == "Select region":
        aux_countries = []
        countries_selected = st.sidebar.multiselect('What region do you want to analyze?', countries_regions.keys(),
                                                    default='Northern Africa')
        display_countries = " and ".join([", ".join(countries_selected[:-1]), countries_selected[-1]] if len(
            countries_selected) > 2 else countries_selected)
        for key in countries_selected:
            aux_countries.extend(countries_regions[key])
        countries_selected = aux_countries
    else:
        countries_selected = st.sidebar.multiselect('What countries do you want to analyze?', countries,
                                                    default='Morocco')
        display_countries = " and ".join([", ".join(countries_selected[:-1]), countries_selected[-1]] if len(
            countries_selected) > 2 else countries_selected)
    mask_countries = df_africa['country'].isin(countries_selected)
    df_africa = df_africa[mask_countries]
    return df_africa, display_countries

def filter_lineages(df_africa):

    # Building variant data frame
    variant_count = pd.DataFrame(df_africa.variant)
    variant_count = variant_count.groupby(['variant']).size().reset_index(name='Count').sort_values(['Count'],
        ascending=True)

    # Filter by Variants
    lineages_selected = st.sidebar.multiselect("Select variants to show", df_africa['variant'].unique(),
                                               default=sorted(df_africa['variant'].unique()))
    mask_lineages = df_africa['variant'].isin(lineages_selected)
    df_africa = df_africa[mask_lineages]
    df_africa.variant[df_africa.variant.isna()] = 'NA'

    return df_africa, variant_count

def filter_by_period(df_africa):
    # TODO: Filter by Period
    df_africa.dropna(subset=['date', 'date2'], inplace=True)
    df_africa['date2'] = df_africa['date2'].sort_values(ascending=True)
    # st.write(df_africa['date2'].unique())
    start_date, end_date = st.sidebar.select_slider("Select a range of time to show", options=df_africa['date2'].unique(),
                                                     value=(df_africa['date2'][0], df_africa['date2'][48]))
    st.sidebar.write('Starts from', start_date, 'to', end_date)

    df_africa = df_africa.loc[(df_africa['date2'] >= start_date) & (df_africa['date2'] <= end_date)]

def show_metrics(df_africa):
    sd_col1, sd_col2 = st.sidebar.columns(2)
    sequences = int(df_africa.shape[0])
    sd_col1.metric("Sequences selected", '{:,}'.format(sequences))
    sd_col2.metric("Countries selected", len(df_africa.country.unique()))

def about_section():
    st.sidebar.info("""
    Figures updated from [Wilkinson et al. Science 2021]\
    (https://www.krisp.org.za/manuscripts/Wilkinson_AfricaGenomics_Science2021.pdf?_ga=2.79914768.662718457.1637830871-1378797665.1637307000)
    
    Contact email: tulio@sun.ac.za
    """)
def acknowledgment_section(logo_path, link):
    logo = get_img_with_href(logo_path, link)
    st.sidebar.markdown(logo, unsafe_allow_html=True)
