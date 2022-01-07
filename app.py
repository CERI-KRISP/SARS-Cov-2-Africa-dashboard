#Import Python Libraries
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import geopandas as gpd
import plotly.graph_objects as go

from datetime import date, datetime

## Page config
st.set_page_config(
    page_title="SARS-COV-2 Dashboard - Genomics Africa ",
    layout="wide",
    initial_sidebar_state="expanded",
     )

##### INPUTS ######
df_africa_path = "./data/africa.csv"

##### Palette colors #####
main_lineages_color_scheme = {'A': '#6c483a', 'A.23.1': '#9f8377', # more: https://coolors.co/6c483a-9f8377-aea198-b9b8ae-cdcfc8
                        'B.1': '#586f6b', 'B.1.1': '#7f9183', 'B.1.1.1': '#b8b8aa', 'B.1.1.318/AZ.x': '#cfc0bd', 'B.1.16': '#DDD5D0',
                        'B.1.1.448': '#d4baca', 'B.1.1.54': '#e69ac8', 'B.1.1.529 (Omicron)': '#e83368', # pink
                        'B.1.1.7 (Alpha)' : '#696969', # more: https://coolors.co/696969-c9c9c9 grey
                        'B.1.237': '#faf0ca', 'B.1.351 (Beta)' : '#ffe45e', 'B.1.351': '#ffe45e', # yellow
                        'B.1.525 (Eta)': '#cdb4db', 'B.1.540': '#c7e8f3', 'B.1.549': '#FFDDD2',
                        'B.1.617.2/AY.x (Delta)': '#2a9d8f',
                        'C.1/C.1.1/C.1.2': '#0D5789', 'C.16': '#3B98C6', 'C.36/C.36.3': '#3B98C6', #more: https://coolors.co/0d5789-3b98c6-edf6f9-ffddd2-e29578
                        'Other Lineages': '#FFFFFF'
                        }
##### Dictionary to convert names of variants #####
variant_names = {'B.1.1.7': 'B.1.1.7 (Alpha)', 'B.1.351': 'B.1.351 (Beta)',
                 'B.1.617.2/AY.x': 'B.1.617.2/AY.x (Delta)', 'B.1.525': 'B.1.525 (Eta)',
                 'B.1.1.529': 'B.1.1.529 (Omicron)'}

###### Dictionary to select countries per region ####
countries_regions = {'Central Africa': {'Burundi', 'Cameroon', 'Central African Republic', 'Republic of Chad',
                                        'Republic of Congo', 'Democratic Republic of Congo',
                                        'Republic of Equatorial Guinea', 'Gabonese Republic', 'São Tomé and Principe'},
                     'Eastern Africa': {'Comoros', 'Djibouti', 'State of Eritrea', 'Ethiopia', 'Kenya', 'Madagascar',
                                        'Mauritius', 'Rwanda', 'Seychelles', 'Somalia', 'Sudan', 'South Sudan', 'Tanzania',
                                        'Uganda'},
                     'Northern Africa': {'Algeria', 'Egypt', 'Libya', 'Mauritania', 'Morocco', 'Sahrawi', 'Tunisia'},
                     'Southern Africa': {'Angola', 'Botswana', 'Eswatini', 'Lesotho', 'Malawi', 'Mozambique', 'Namibia',
                                         'South Africa', 'Zambia', 'Zimbabwe'},
                     'Western Africa': {'Benin', 'Faso', 'Cabo Verde', 'Côte d\'Ivoire', 'Gambia', 'Ghana', 'Guinea',
                                        'Guinea Bissau', 'Liberia', 'Mali', 'Niger', 'Nigeria', 'Senegal', 'Sierra Leone',
                                        'Togolese'}}

##Add sidebar to the app
st.sidebar.title("GENOMICS AFRICA")
st.sidebar.subheader("Results Updated – 30 December 2021")
# st.sidebar.markdown("#### Accelerating genomics surveillance for COVID-19 response in Africa. A program of CERI and partners in colaboration with Rockefeller Foundation")
st.sidebar.markdown(" ")
st.sidebar.subheader("Filter data ")

#Data preparation to only retrieve fields that are relevant to this project

df_africa = pd.read_csv(df_africa_path)
df_africa = df_africa[df_africa.pangolin_lineage2 != 'None']
df_africa.replace({'pangolin_lineage2': variant_names}, inplace=True)
# # Date format
# df_africa.date2 = df_africa.date2.str.replace('-', '/')
# df_africa.date2 = pd.to_datetime(df_africa.date2)
# df_africa.date2 = df_africa['date2'].dt.strftime("%Y/%m/%d")

# Filter by selected country
countries = df_africa['country'].unique()
selection = st.sidebar.radio("Select Countries to show",("Show all countries", "Select region",
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
    countries_selected = st.sidebar.multiselect('What countries do you want to analyze?', countries, default='Morocco')
    display_countries = " and ".join([", ".join(countries_selected[:-1]), countries_selected[-1]] if len(countries_selected) > 2 else countries_selected)
mask_countries = df_africa['country'].isin(countries_selected)
df_africa = df_africa[mask_countries]

#Building pangolin data frame
pangolin_count = pd.DataFrame(df_africa.pangolin_lineage2)
pangolin_count = pangolin_count.groupby(['pangolin_lineage2']).size().reset_index(name='Count').sort_values(['Count'], ascending=True)
pangolin_count_top20 = pangolin_count.tail(20)
pangolin_count_top20['pangolin_africa'] = pangolin_count_top20.pangolin_lineage2


# Filter by Lineages
lineages_selected = st.sidebar.multiselect('Select variants/lineages to show', pangolin_count_top20['pangolin_africa'],
                                           default=pangolin_count_top20['pangolin_africa'])
mask_lineages = df_africa['pangolin_lineage2'].isin(lineages_selected)
df_africa = df_africa[mask_lineages]

# TODO: Filter by Period

# start_date, end_date = st.sidebar.select_slider("Select a range of time to show", options=df_africa['date2'].unique(),
#                                                  value=(df_africa['date2'].min(), df_africa['date2'].max()))
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
#st.title("SARS-COV-2 DASHBOARD")
st.markdown("<h1 style='text-align: center; color: #FF7557;'>SARS-COV-2 AFRICA DASHBOARD</h1>", unsafe_allow_html=True)


st.markdown("<h5 style='text-align: center;'>Showing results from %s </h5>" % display_countries, unsafe_allow_html=True)

### Layout of main page
c1, c2 = st.columns((1.5, 1.9))

############ First column ###############
############## MAP CHART ##############

# Reading Africa map and joing with africa_df information
gdf = gpd.read_file('data/africa.geojson')
df_map = gdf.merge(df_africa1, left_on="sovereignt", right_on="country", how="outer")
df_map = df_map[['strain','virus','date', 'date2','country','division','pangolin_africa','Nextstrain_variants', 'sovereignt', 'sov_a3', 'geometry']]

df_map['date'] = pd.to_datetime(df_map['date'], format='%Y-%m-%d', yearfirst=True)
initial_date = df_map['date'].min()
initial_date = initial_date.strftime('%Y-%m-%d')
final_date = df_map['date'].max()
final_date = final_date.strftime('%Y-%m-%d')

countries_codes = df_map[['country', 'sov_a3']]
countries_codes.drop_duplicates(inplace=True)

## count strains per country - by total
count_variants = df_map.groupby(['country','pangolin_africa', 'date2'], as_index=False).size().rename(columns={'size': 'counts'})
count_variants = count_variants.merge(countries_codes, on='country', how='left')

## count strains per country - by percentage of each lineage in the country
count_variants['percentage'] = 100 * count_variants['counts'] / count_variants.groupby('country')['counts'].transform('sum')

coloured_options = ['A', 'B.1.1.7 (Alpha)', 'B.1.351 (Beta)', 'B.1.617.2/AY.x (Delta)', 'B.1.525 (Eta)', 'B.1.1.529 (Omicron)']
with st.container():
    #Radio selection for scale of data to show
    map_scale = c1.radio("Select scale you want to show the data", ("Absolute", "Relative (%)"))
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    if map_scale == "Absolute":
        map_count_column = 'counts'
    else:
        map_count_column = 'percentage'

    #Lineage selection to color
    colour_by = c1.selectbox('Colour map by', coloured_options, index=len(coloured_options)-1)
    coloured_map = count_variants[count_variants.pangolin_africa == colour_by]

    #Building synthetic data to set initial and end date for dataframe
    synthetic_data = []
    for index, row in coloured_map.groupby('country')[['pangolin_africa', 'sov_a3']].agg('first').reset_index().iterrows():
        synthetic_data.append([row['country'], row['pangolin_africa'], initial_date, np.NAN, row['sov_a3'], np.NAN])
        synthetic_data.append([row['country'], row['pangolin_africa'], final_date, np.NAN, row['sov_a3'], np.NAN])
    synthetic_data = pd.DataFrame(synthetic_data, columns=['country', 'pangolin_africa', 'date2', 'counts', 'sov_a3', 'percentage'])
    coloured_map = coloured_map.append(synthetic_data).sort_values(by=['date2'])

    if coloured_map[map_count_column].empty:
        c1.warning("No data to show for this lineage.")
        fig_map = px.line_geo(lat=[0,0,0,0], lon=[0,0,0,0])
    else:
        fig_map = px.choropleth(coloured_map,
                                 locations='sov_a3', color=map_count_column,
                                labels={'pangolin_africa': 'Lineage', 'counts': 'Total of Genomes (absolute)',
                                        'percentage': 'Total of Genomes (%)', 'date2': 'Date'},
                                hover_name='country',
                                 hover_data =['pangolin_africa', 'counts', 'percentage'], color_continuous_scale="Reds",
                                animation_frame='date2'
                                )
    fig_map.update_layout(geo_scope="africa")
    # fig_map.update_geos(fitbounds="locations")
    fig_map.update_layout(height=600, margin={"r": 0, "t": 0, "l": 0, "b": 0},
                          legend=dict(orientation='h')
                          )
    c1.plotly_chart(fig_map, use_container_width=True)

############ Second column ###############
####### TOP 20 CHART ###########
with st.container():
    fig = px.bar(variants_percentage.sort_values(by=['pangolin_africa']), x='date2', y='Count_x',
                 color='pangolin_africa', color_discrete_map=main_lineages_color_scheme,
                 # color_discrete_sequence=px.colors.qualitative.Prism,
                barmode='stack', title="Top 20 circulating lineages and variants",
                 custom_data=['pangolin_africa', 'Count_x', 'date2'], labels={'pangolin_africa': 'Lineage', 'Count_x': 'Percentage', 'date2': 'Date'})
    fig.update_yaxes(title="Proportion of Genomes")
    fig.update_xaxes(title="Date", range=[variants_percentage['date2'].min(), datetime.today()])
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=0.9,
        xanchor="right",
        x=1
    ), legend_title_text="Lineages", height=450)
    fig.update_layout(title=dict(y=1))
    c2.plotly_chart(fig, use_container_width=True)

####### COUNTRIES WHITH SEQUENCE CHART #########
df_country_lineages = df_africa.copy()
variants = []
for index, row in df_country_lineages.iterrows():
    if row['pangolin_lineage2'] in coloured_options:
        variants.append(row['pangolin_lineage2'])
    else:
        variants.append('Other Lineages')
df_country_lineages['variant'] = variants
with st.container():
    country_lineages = px.scatter(df_country_lineages, x="date", y="country", color="variant",
                 title="Sequence data", color_discrete_map=main_lineages_color_scheme)
    country_lineages.update_traces(marker = dict(size = 15, line=dict(width=0.5, color='#E5ECF6')))
    country_lineages.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="right",
        x=1
    ), legend_title_text="Variants")
    country_lineages.update_layout(title=dict(y=1), yaxis={'categoryorder':'category descending'})
    c2.plotly_chart(country_lineages, use_container_width=True)
