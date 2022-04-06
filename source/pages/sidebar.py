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
                                                    default='Southern Africa')
        display_countries = " and ".join([", ".join(countries_selected[:-1]), countries_selected[-1]] if len(
            countries_selected) > 2 else countries_selected)
        for key in countries_selected:
            aux_countries.extend(countries_regions[key])
        countries_selected = aux_countries
        print(countries_selected)
        df_africa.to_csv("data/analyses/df_after_select_region.csv")
    else:
        countries_selected = st.sidebar.multiselect('What countries do you want to analyze?', countries,
                                                    default='South Africa')
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
    df_africa.dropna(subset=['date_2weeks'], inplace=True)

    df_africa['date_2weeks'] = pd.to_datetime(df_africa['date_2weeks'], errors='coerce', format='%Y-%m-%d', yearfirst=True)

    df_africa['date_2weeks'] = df_africa['date_2weeks'].sort_values(ascending=False)
    df_africa['date_2weeks'] = df_africa['date_2weeks'].dt.strftime('%b %d,%Y')

    start_date, end_date = st.sidebar.select_slider("Select a range of time to show",
                                                    options=sorted(df_africa['date_2weeks'].unique()),
                                                    value=(df_africa['date_2weeks'].min(),
                                                           df_africa['date_2weeks'].max()))

    # make selection
    df_africa = df_africa.loc[(df_africa['date_2weeks'] >= start_date) & (df_africa['date_2weeks'] <= end_date)]

    # returning original date format
    df_africa['date_2weeks'] = df_africa['collection_date'] + pd.offsets.SemiMonthEnd()
    df_africa['date_2weeks'] = df_africa['date_2weeks'].dt.strftime('%Y-%m-%d')
    return df_africa

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

@st.cache(allow_output_mutation=True)
def acknowledgment_section(logo_path, link):
    logo = get_img_with_href(logo_path, link)
    st.sidebar.markdown(logo, unsafe_allow_html=True)
