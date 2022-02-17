import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import geopandas as gpd

from utils.functions import *
from utils.dicts import *

def map_data(df_africa):
    # Reading Africa map and joing with africa_df information
    gdf = gpd.read_file('data/africa.geojson')
    df_map = gdf.merge(df_africa, left_on="sovereignt", right_on="country", how="outer")
    df_map = df_map[
        ['strain', 'virus', 'date', 'date2', 'country', 'division', 'variant', 'Nextstrain_variants', 'sovereignt',
         'sov_a3', 'geometry', 'Count']]

    df_map['date'] = pd.to_datetime(df_map['date'], format='%Y-%m-%d', yearfirst=True)
    initial_date = df_map['date'].min()
    initial_date = initial_date.strftime('%Y-%m-%d')
    final_date = df_map['date'].max()
    final_date = final_date.strftime('%Y-%m-%d')

    countries_codes = df_map[['country', 'sov_a3']]
    countries_codes.drop_duplicates(inplace=True)

    ## count strains per country - by total
    count_variants = df_map.groupby(['country', 'variant', 'date2'], as_index=False).size().rename(
        columns={'size': 'counts'})
    count_variants = count_variants.merge(countries_codes, on='country', how='left')

    ## count strains per country - by percentage of each lineage in the country
    count_variants['percentage'] = 100 * count_variants['counts'] / count_variants.groupby('country')[
        'counts'].transform(
        'sum')
    return count_variants, initial_date, final_date

def map_synthetic_data(df, initial_date, final_date):
    coloured_map = df
    synthetic_data = []
    for index, row in coloured_map.groupby('country')[['variant', 'sov_a3']].agg(
            'first').reset_index().iterrows():
        synthetic_data.append([row['country'], row['variant'], initial_date, np.NAN, row['sov_a3'], np.NAN])
        synthetic_data.append([row['country'], row['variant'], final_date, np.NAN, row['sov_a3'], np.NAN])
    synthetic_data = pd.DataFrame(synthetic_data,
                                  columns=['country', 'variant', 'date2', 'counts', 'sov_a3', 'percentage'])
    coloured_map = coloured_map.append(synthetic_data).sort_values(by=['date2'])
    return coloured_map

def map_fill_na_values(df):
    coloured_map = df
    counts = []
    min_country_dates = coloured_map.groupby('country').agg({'date2': 'min'}).reset_index()

    for index, row in coloured_map.iterrows():
        min_date = min_country_dates['date2'].loc[min_country_dates['country'] == row['country']].min()
        if (row['date2'] == min_date) and np.isnan(row['counts']) == True:
            counts.append(0)
        else:
            counts.append(row['counts'])
    coloured_map['counts'] = counts
    coloured_map_aux = coloured_map.sort_values(by=['country', 'date2'])
    coloured_map_aux['counts'] = coloured_map_aux['counts'].fillna(method='ffill')
    coloured_map = coloured_map_aux.sort_values(by='date2')
    return coloured_map

def colorpath_africa_map(df_africa, column):
    c = column
    count_variants, initial_date, final_date = map_data(df_africa)
    map_count_column = 'percentage'
    with st.container():
        # Radio selection for scale of data to show
        # COLORPATH SELECTION
        map_scale = c.radio("Select scale you want to show the data", ("Absolute", "Relative (%)"))
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        if map_scale == "Absolute":
            map_count_column = 'counts'
        else:
            map_count_column = 'percentage'
        # Lineage selection to color
        colour_by = c.selectbox('Colour map by', concerned_variants, index=len(concerned_variants) - 1)
        coloured_map = count_variants[count_variants.variants == colour_by]
        # Building synthetic data to set initial and end date for dataframe
        coloured_map = map_synthetic_data(coloured_map)

        # Setting up latitude and longitude columns
        longitude = []
        latitude = []
        for i in coloured_map['country']:
            if findGeocode(i) != None:
                loc = findGeocode(i)
                latitude.append(loc.latitude)
                longitude.append(loc.longitude)
            else:
                latitude.append(np.nan)
                longitude.append(np.nan)

        coloured_map["lat"] = latitude
        coloured_map["long"] = longitude
        #c1.write(coloured_map.head())
        # Filling NA values
        coloured_map = map_fill_na_values(coloured_map)

        fig_map = px.choropleth(coloured_map,
                                locations='sov_a3', color=map_count_column,
                                labels={'pangolin_africa': 'Lineage', 'counts': 'Total of Genomes (absolute)',
                                        'percentage': 'Total of Genomes (%)', 'date2': 'Date'},
                                hover_name='country',
                                hover_data=['pangolin_africa', 'counts', 'percentage'], color_continuous_scale="Reds"
                                )
        fig_map.update_layout(geo_scope="africa")
        # fig_map.update_geos(fitbounds="locations")
        fig_map.update_layout(height=600, margin={"r": 0, "t": 0, "l": 0, "b": 0},
                              legend=dict(orientation='h')
                              )
        fig_map.update_layout(title="Genomes X Variants", title_x=0.5)
        c.plotly_chart(fig_map, use_container_width=True)



def scatter_africa_map(df_africa, column):
    c = column
    coloured_map, initial_date, final_date = map_data(df_africa)
    map_count_column = 'percentage'
    countries = coloured_map['sov_a3'].unique()
    #TODO: colorir paises selecionados

    with st.container():
        # Building synthetic data to set initial and end date for dataframe
        coloured_map = map_synthetic_data(coloured_map, initial_date, final_date)

        # Filling NA values
        coloured_map = map_fill_na_values(coloured_map)

        if coloured_map[map_count_column].empty:
            c.warning("No data to show for this lineage.")
            fig_map = px.line_geo(lat=[0, 0, 0, 0], lon=[0, 0, 0, 0])
        else:
            # c1.write(coloured_map)
            coloured_map['variants'] = lineages_to_concerned_variants(coloured_map, 'variant')
            c.subheader("Genomes per lineage")

            ### variants legend
            legend_box = st.container()
            legend_box.write(custom_legend(concerned_variants, main_lineages_color_scheme, c))

            fig_map = px.scatter_geo(coloured_map, locations='sov_a3', hover_name='country',
                                     hover_data=['variant', 'counts', 'percentage'],
                                     labels={'pangolin_africa': 'Lineage', 'counts': 'Total of Genomes (absolute)',
                                             'percentage': 'Total of Genomes (%)', 'date2': 'Date'},
                                     animation_frame="date2", size='counts', animation_group='country',
                                     color='variants', size_max=100,
                                     color_discrete_map=main_lineages_color_scheme)
            fig_map.update_traces(marker=dict(
                                                size=coloured_map['counts'],
                                                line_width=5,
                                                sizeref=1,
                                                sizemode="area",
                                                reversescale=True,
                                                line=dict(width=3,
                                                          color='rgba(68, 68, 68, 0)')))
            fig_map.update_layout(geo_scope='africa')
            fig_map.update_layout(height=600, margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                  legend=dict(orientation='h'))
            fig_map.update_layout(title_y=1)
            last_frame_num = int(len(fig_map.frames) - 2)
            fig_map.layout['sliders'][0]['active'] = last_frame_num
            fig_map.update_layout(showlegend=False)
        c.plotly_chart(fig_map, use_container_width=True)