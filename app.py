#Import Python Libraries
import datetime

import pandas as pd
import streamlit as st
import plotly.express as px

## Page config
st.set_page_config(
    page_title="SARS-COV-2 Dashboard - Genomics Africa ",
    layout="wide",
    initial_sidebar_state="expanded",
     )

#### INPUTS ######
df_africa_path = "./data/africa.csv"

# #Add sidebar to the app
st.sidebar.markdown("# GENOMICS AFRICA")
# st.sidebar.markdown("#### Accelerating genomics surveillance for COVID-19 response in Africa. A program of CERI and partners in colaboration with Rockefeller Foundation")
st.sidebar.markdown(" ")
st.sidebar.markdown("### Filter data ")

#Data preparation to only retrieve fields that are relevant to this project

df_africa = pd.read_csv(df_africa_path)
df_africa = df_africa[df_africa.pango_lineage2 != 'None']

# Filter by selected country
countries = df_africa['country'].unique()
selection = st.sidebar.radio("Select Countries to show",("Show all countries", "Select one or more countries"))
if selection == "Show all countries":
    countries_selected =df_africa['country'].unique()
else:
    countries_selected = st.sidebar.multiselect('Which countries do you want to analyze?', countries, default='South Africa')
mask_countries = df_africa['country'].isin(countries_selected)
df_africa = df_africa[mask_countries]

#Building pangolin data frame
pangolin_count = pd.DataFrame(df_africa.pango_lineage2)
pangolin_count = pangolin_count.groupby(['pango_lineage2']).size().reset_index(name = 'Count').sort_values(['Count'], ascending=True)
pangolin_count_top20 = pangolin_count.tail(20)
pangolin_count_top20['pangolin_africa'] = pangolin_count_top20.pango_lineage2

# Filter by Lineages
lineages_selected = st.sidebar.multiselect('Select variants/lineages to show', pangolin_count_top20['pangolin_africa'],
                                           default=pangolin_count_top20['pangolin_africa'])
mask_lineages = df_africa['pango_lineage2'].isin(lineages_selected)
df_africa = df_africa[mask_lineages]

# Filter by Period
start_date, end_date = st.sidebar.select_slider("Select a range of time to show",
                                        options=df_africa['date2'].unique(), value=(df_africa['date2'].min(), df_africa['date2'].max()))
st.sidebar.write('Starts from', start_date, 'to', end_date)
df_africa = df_africa[(df_africa['date2'] > start_date) & (df_africa['date2'] < end_date)]

### Merge df_africa with pangolin_count_top20

df_africa1 = pd.merge(df_africa, pangolin_count_top20, on='pango_lineage2', how='left')

df_africa1.pangolin_africa[df_africa1.pangolin_africa.isna() == True] = 'NA'
variants_percentage = df_africa1.groupby(['date2', 'pangolin_africa']).agg({'Count_x': 'sum'})
variants_percentage = variants_percentage.groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))
variants_percentage = variants_percentage.reset_index()


st.sidebar.markdown("Figures updated from [Wilkinson et al. Science 2021](https://www.krisp.org.za/manuscripts/Wilkinson_AfricaGenomics_Science2021.pdf?_ga=2.79914768.662718457.1637830871-1378797665.1637307000)")
st.sidebar.markdown("Contact email: tulio@sun.ac.za")
# #Add title and subtitle to the main interface of the app
st.title("SARS-COV-2 DASHBOARD")
st.markdown("#### Results Updated – 15 November 2021")

with st.container():
    fig = px.bar(variants_percentage.sort_values(by=['pangolin_africa']), x='date2', y='Count_x', color='pangolin_africa', color_discrete_sequence=px.colors.qualitative.Prism,
             barmode='stack', title="Africa - Top 20 circulating lineages and variants",
                 custom_data=['pangolin_africa', 'Count_x', 'date2'], labels={'pangolin_africa': 'Lineage', 'Count_x': 'Percentage', 'date2': 'Date'})
    fig.update_yaxes(title="Proportion of Genomes")
    fig.update_xaxes(title="Date")
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.5,
        xanchor="right",
        x=1
    ), legend_title_text="Lineages", height=600)
    st.plotly_chart(fig, use_container_width=True)
