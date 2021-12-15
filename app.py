#Import Python Libraries
import folium
import pandas as pd
import streamlit as st
import plotly.express as px
import geopandas as gpd

from datetime import date, datetime

## Page config
st.set_page_config(
    page_title="SARS-COV-2 Dashboard - Genomics Africa ",
    layout="wide",
    initial_sidebar_state="expanded",
     )

#### INPUTS ######
df_africa_path = "./data/africa.csv"

##### Palette colors #####
main_lineages_color_scheme = {'A': '#6c483a', 'A.23.1': '#9f8377', # more: https://coolors.co/6c483a-9f8377-aea198-b9b8ae-cdcfc8
                        'B.1': '#586f6b', 'B.1.1': '#7f9183', 'B.1.1.1': '#b8b8aa', 'B.1.1.318/AZ.x': '#cfc0bd', 'B.1.16': '#DDD5D0',
                        'B.1.1.448': '#d4baca', 'B.1.1.54': '#e69ac8', 'B.1.1.529 (Omicron)': '#e83368', # pink
                        'B.1.1.7 (Alpha)' : '#696969', # more: https://coolors.co/696969-c9c9c9 grey
                        'B.1.237': '#faf0ca', 'B.1.351 (Beta)' : '#ffe45e', 'B.1.351': '#ffe45e', # yellow
                        'B.1.525 (Eta)': '#cdb4db', 'B.1.540': '#c7e8f3', 'B.1.549': '#FFDDD2',
                        'B.1.617.2/AY.x (Delta)': '#2a9d8f',
                        'C.1/C.1.1/C.1.2': '#0D5789', 'C.16': '#3B98C6', 'C.36/C.36.3': '#3B98C6' #more: https://coolors.co/0d5789-3b98c6-edf6f9-ffddd2-e29578

                        }

# #Add sidebar to the app
st.sidebar.title("GENOMICS AFRICA")
# st.sidebar.markdown("#### Accelerating genomics surveillance for COVID-19 response in Africa. A program of CERI and partners in colaboration with Rockefeller Foundation")
st.sidebar.markdown(" ")
st.sidebar.subheader("Filter data ")

#Data preparation to only retrieve fields that are relevant to this project

df_africa = pd.read_csv(df_africa_path)
df_africa = df_africa[df_africa.pangolin_lineage2 != 'None']
# # Date format
# df_africa.date2 = df_africa.date2.str.replace('-', '/')
# df_africa.date2 = pd.to_datetime(df_africa.date2)
# df_africa.date2 = df_africa['date2'].dt.strftime("%Y/%m/%d")

# Filter by selected country
countries = df_africa['country'].unique()
selection = st.sidebar.radio("Select Countries to show",("Show all countries", "Select one or more countries"))

if selection == "Show all countries":
    countries_selected = df_africa['country'].unique()
else:
    countries_selected = st.sidebar.multiselect('Which countries do you want to analyze?', countries, default='Morocco')
mask_countries = df_africa['country'].isin(countries_selected)
df_africa = df_africa[mask_countries]

#Building pangolin data frame
pangolin_count = pd.DataFrame(df_africa.pangolin_lineage2)
pangolin_count = pangolin_count.groupby(['pangolin_lineage2']).size().reset_index(name = 'Count').sort_values(['Count'], ascending=True)
pangolin_count_top20 = pangolin_count.tail(20)
pangolin_count_top20['pangolin_africa'] = pangolin_count_top20.pangolin_lineage2


# Filter by Lineages
lineages_selected = st.sidebar.multiselect('Select variants/lineages to show', pangolin_count_top20['pangolin_africa'],
                                           default=pangolin_count_top20['pangolin_africa'])
mask_lineages = df_africa['pangolin_lineage2'].isin(lineages_selected)
df_africa = df_africa[mask_lineages]

# TODO: Filter by Period

# start_date, end_date = st.sidebar.select_slider("Select a range of time to show", options=df_africa['date2'].unique(),
#                                                 value=(df_africa['date2'].min(), df_africa['date2'].max()))
# st.sidebar.write('Starts from', start_date, 'to', end_date)
#
# df_africa = df_africa.loc[(df_africa['date2'] >= start_date) & (df_africa['date2'] <= end_date)]

### Merge df_africa with pangolin_count_top20

try:
    df_africa1 = pd.merge(df_africa, pangolin_count_top20, on='pangolin_lineage2', how='left')
except pd.errors.MergeError as e:
    st.error("Error on merge dataframe:")
    st.error(e)

df_africa1.pangolin_africa[df_africa1.pangolin_africa.isna()] = 'NA'

variants_percentage = df_africa1.groupby(['date2', 'pangolin_africa']).agg({'Count_x': 'sum'})
variants_percentage = variants_percentage.groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))
variants_percentage = variants_percentage.reset_index()

st.sidebar.markdown("Figures updated from [Wilkinson et al. Science 2021](https://www.krisp.org.za/manuscripts/Wilkinson_AfricaGenomics_Science2021.pdf?_ga=2.79914768.662718457.1637830871-1378797665.1637307000)")
st.sidebar.markdown("Contact email: tulio@sun.ac.za")
#### End of sidebar

# #Add title and subtitle to the main interface of the app
st.title("SARS-COV-2 DASHBOARD")
st.subheader("Results Updated – 4 December 2021")

### Layout of main page
c1, c2 = st.columns((1.5, 2))

############## MAP CHART ##############

# Reading Africa map and joing with africa_df information
gdf = gpd.read_file('data/africa.geojson')
df_map = gdf.merge(df_africa1, left_on="sovereignt", right_on="country", how="outer")
df_map = df_map[['strain','virus','date','country','division','pangolin_africa','Nextstrain_variants', 'sovereignt', 'sov_a3', 'geometry']]


## count strains per country
count_variants = df_map.groupby(['country','sov_a3', 'pangolin_africa']).size().reset_index(name='counts')
with st.container():
    fig_map = px.scatter_geo(count_variants,
                             locations='sov_a3', color='pangolin_africa',
                             hover_name='country', size='counts')
    fig_map.update_layout(geo_scope="africa")
    c1.plotly_chart(fig_map, use_container_width=True)

## Top 20 circulation variants chart
with st.container():
    fig = px.bar(variants_percentage.sort_values(by=['pangolin_africa']), x='date2', y='Count_x',
                 color='pangolin_africa', color_discrete_map=main_lineages_color_scheme,
                 # color_discrete_sequence=px.colors.qualitative.Prism,
                barmode='stack', title="Africa - Top 20 circulating lineages and variants",
                 custom_data=['pangolin_africa', 'Count_x', 'date2'], labels={'pangolin_africa': 'Lineage', 'Count_x': 'Percentage', 'date2': 'Date'})
    fig.update_yaxes(title="Proportion of Genomes")
    fig.update_xaxes(title="Date")
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=0.9,
        xanchor="right",
        x=1
    ), legend_title_text="Lineages", height=400)
    c2.plotly_chart(fig, use_container_width=True)

# TODO: Set colors pallet from Houriyah - idea: gradient color for each variant