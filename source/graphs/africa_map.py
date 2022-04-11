import json

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import geopandas as gpd

from utils.functions import *
from utils.dicts import *


@st.cache(allow_output_mutation=True)
def map_data(df):
    # function to map countrys to country code and gets initial and final dates from the set

    # dropping white spaces in country column
    df['country'] = df['country'].str.lstrip()
    df['country'] = df['country'].str.rstrip()
    # Reading Africa map and joing with africa_df information
    gdf = gpd.read_file('data/africa.geojson')
    df_map = gdf.merge(df, left_on="sovereignt", right_on="country", how="outer")
    df_map = df_map[
        ['date_2weeks', 'country', 'variant', 'sovereignt', 'sov_a3', 'Count']]

    # filling missing country codes
    df_map['sov_a3'] = df_map['sov_a3'].astype(str)
    temp_codes = []
    for index, row in df_map.iterrows():
        if row['sov_a3'] == 'nan':
            temp_codes.append(missing_country_codes[row['country']])
        else:
            temp_codes.append(row['sov_a3'])
    df_map['sov_a3'] = temp_codes
    # TODO: write test to check if doesn't have any empty value in sov_a3 column

    df_map['date_2weeks'] = pd.to_datetime(df_map['date_2weeks'], errors='coerce', format='%Y-%m-%d', yearfirst=True)
    initial_date = df_map['date_2weeks'].min()
    initial_date = initial_date.strftime('%Y-%m-%d')
    final_date = df_map['date_2weeks'].max()
    final_date = final_date.strftime('%Y-%m-%d')

    # Drop NA values
    df_map.dropna(subset=['country', 'date_2weeks'], inplace=True)

    # convert column date to str
    df_map['date_2weeks'] = df_map['date_2weeks'].dt.strftime('%Y-%m-%d')

    return df_map, initial_date, final_date


@st.cache(allow_output_mutation=True)
def count_variants_per_country(df_map):
    countries_codes = df_map[['country', 'sov_a3']]
    countries_codes.drop_duplicates(inplace=True)

    ## count strains per country - by total
    count_variants = df_map.groupby(['country', 'variant', 'date_2weeks'], as_index=False).size().rename(
        columns={'size': 'Count'})
    count_variants = count_variants.merge(countries_codes, on='country', how='left')

    ## count strains per country - by percentage of each lineage in the country
    count_variants['percentage'] = 100 * count_variants['Count'] / count_variants.groupby('country')[
        'Count'].transform(
        'sum')
    return count_variants


# review if we need this function
def count_cumulative_genomes_per_country(df_map):
    countries_codes = df_map[['country', 'sov_a3']]
    countries_codes.drop_duplicates(inplace=True)

    ## count cumulative genomes per country - by total
    count_genomes = df_map.groupby(['country', 'date_2weeks'], as_index=False).size().rename(
        columns={'size': 'Count'})
    count_genomes = count_genomes.merge(countries_codes, on='country', how='left')

    ## count cumulative genomes per country - by total of genomes produced
    count_genomes['percentage'] = 100 * count_genomes['Count'] / count_genomes.groupby('country')[
        'Count'].transform(
        'sum')
    return count_genomes


def insert_lat_long_columns(df):
    # Setting up latitude and longitude columns
    longitude = []
    latitude = []
    for i in df['country']:
        if findGeocode(i) != None:
            loc = findGeocode(i)
            latitude.append(loc.latitude)
            longitude.append(loc.longitude)
        else:
            latitude.append(np.nan)
            longitude.append(np.nan)

    df["lat"] = latitude
    df["long"] = longitude
    return df


@st.cache(allow_output_mutation=True)
def map_synthetic_data_variant(df, initial_date, final_date):
    coloured_map = df
    synthetic_data = []
    for index, row in coloured_map.groupby('country')[['variant', 'sov_a3']].agg(
            'first').reset_index().iterrows():
        synthetic_data.append([row['country'], row['variant'], initial_date, np.NAN, row['sov_a3'], np.NAN])
        synthetic_data.append([row['country'], row['variant'], final_date, np.NAN, row['sov_a3'], np.NAN])
    synthetic_data = pd.DataFrame(synthetic_data,
                                  columns=['country', 'variant', 'date_2weeks', 'Count', 'sov_a3', 'percentage'])
    # converting to datetime format
    coloured_map['date_2weeks'] = pd.to_datetime(df['date_2weeks'], format='%Y-%m-%d', yearfirst=True)
    synthetic_data['date_2weeks'] = pd.to_datetime(df['date_2weeks'], format='%Y-%m-%d', yearfirst=True)
    coloured_map = coloured_map.append(synthetic_data).sort_values(by=['date_2weeks'])
    # changing datetime to str
    coloured_map['date_2weeks'] = coloured_map['date_2weeks'].dt.strftime('%Y-%m-%d')
    return coloured_map


@st.cache(allow_output_mutation=True)
def map_synthetic_data(df, initial_date, final_date):
    """
    This function adds initial and final data for all countries and fill with NA the dates without information
    :param df:
    :param initial_date:
    :param final_date:
    :return: df to be used in colored map graphs containing same dates to all countries
    """
    coloured_map = df
    synthetic_data = []
    # working with columns: country, date_2weeks, counts, sov_a3
    for index, row in coloured_map.groupby('country')[['sov_a3']].agg(
            'first').reset_index().iterrows():
        synthetic_data.append([row['country'], initial_date, np.NAN, row['sov_a3']])
        synthetic_data.append([row['country'], final_date, np.NAN, row['sov_a3']])
    synthetic_data = pd.DataFrame(synthetic_data,
                                  columns=['country', 'date_2weeks', 'Count', 'sov_a3'])

    # converting to datetime format
    coloured_map['date_2weeks'] = pd.to_datetime(df['date_2weeks'], format='%Y-%m-%d', yearfirst=True)
    synthetic_data['date_2weeks'] = pd.to_datetime(df['date_2weeks'], format='%Y-%m-%d', yearfirst=True)
    coloured_map = coloured_map.append(synthetic_data).sort_values(by=['date_2weeks'])

    # adding missing dates to be filled by cumsum
    dates_set = coloured_map['date_2weeks'].unique()
    new_data = {'country': [], 'date_2weeks': [], 'Count': [], 'sov_a3': []}
    for country, df_country in coloured_map.groupby('country'):
        country_dates = df_country['date_2weeks'].unique()
        for item in dates_set:
            if item not in country_dates:
                new_data['country'].append(country)
                new_data['date_2weeks'].append(item)
                new_data['Count'].append(0)
                new_data['sov_a3'].append(df_country['sov_a3'].iloc[0])
    new_data = pd.DataFrame(new_data)
    coloured_map = coloured_map.append(new_data)

    # Drop NA values
    coloured_map.dropna(subset=['country', 'date_2weeks'], inplace=True)

    # changing datetime to str
    coloured_map['date_2weeks'] = coloured_map['date_2weeks'].dt.strftime('%Y-%m-%d')
    return coloured_map


@st.cache(allow_output_mutation=True)
def map_fill_na_values(df, map_count_column):
    coloured_map = df
    counts = []
    # converting to datetime format
    coloured_map['date_2weeks'] = pd.to_datetime(df['date_2weeks'], format='%Y-%m-%d', yearfirst=True)
    min_country_dates = coloured_map.groupby('country').agg({'date_2weeks': 'min'}).reset_index()

    for index, row in coloured_map.iterrows():
        min_date = min_country_dates['date_2weeks'].loc[min_country_dates['country'] == row['country']].min()
        if (row['date_2weeks'] == min_date) and np.isnan(row[map_count_column]) == True:
            counts.append(0)
        else:
            counts.append(row[map_count_column])
    coloured_map[map_count_column] = counts
    coloured_map_aux = coloured_map.sort_values(by=['country', 'date_2weeks'])
    coloured_map_aux[map_count_column] = coloured_map_aux[map_count_column].fillna(method='ffill')
    coloured_map = coloured_map_aux.sort_values(by='date_2weeks')
    # changing datetime to str
    coloured_map['date_2weeks'] = coloured_map['date_2weeks'].dt.strftime('%Y-%m-%d')

    #dropping NA dates
    coloured_map.dropna(subset=['date_2weeks'], inplace=True)
    return coloured_map


# TODO: Map to show number of cumulative genomes in total
def colorpath_africa_map(df_africa, column, color_pallet):
    # df_africa is a dataframe with the number for each variant per country and per day
    c = column
    # gdf = gpd.read_file('data/africa.geojson')

    df_map, initial_date, final_date = map_data(df_africa)

    # adding synthetic data to fill date gaps
    df_map = map_synthetic_data(df_map, initial_date, final_date)

    # dropping columns we don't need
    # df_map.drop(['variant', 'sovereignt'], axis=1, inplace=True)

    # cumulative count column
    df_map = df_map.sort_values(by='date_2weeks')
    df_map['cum_counts'] = df_map[['country', 'Count']].groupby('country').cumsum()

    # Building hover text
    temp_text = []
    for index, row in df_map.iterrows():
        temp_text.append('<b>{}</b> <br><br>{:.0f} genomes <br> from {} to {}'.format(row['country'], row['cum_counts'],
                                                                                      initial_date, row['date_2weeks']))
    df_map['hover_text'] = temp_text

    with st.container():
        # Figure title
        # c.markdown("##### Cumulative genomes produced since {}".format(initial_date))
        fig_map = px.choropleth(df_map,
                                locations='sov_a3', color='cum_counts',
                                hover_name='country', animation_frame="date_2weeks",
                                color_continuous_scale=color_pallet,
                                range_color=[0, max(df_map['cum_counts'])],
                                labels={'cum_counts': 'Number of genomes', 'date_2weeks': 'Date'},
                                custom_data=['country', 'cum_counts', 'date_2weeks'],
                                title="Cumulative genomes produced since {}".format(initial_date)
                                )
        fig_map.update_layout(geo_scope="africa")
        fig_map.update_geos(visible=False, showcoastlines=True, showcountries=True, showlakes=True, showland=True,
                            showrivers=True, showsubunits=True, subunitcolor='#3E8989')
        fig_map.update_layout(height=600, margin={"r": 0, "t": 0, "l": 0, "b": 0},
                              legend=dict(orientation='h')
                              )
        fig_map.update_layout(title_y=0.2)

        # creating standardize hover template
        custom_hovertemplate = '<b>%{customdata[0]} </b><br><br>' + \
                               '%{customdata[1]} genomes <br>from 2020-01-15' + \
                               ' to %{customdata[2]}<br>'

        fig_map.update_traces(hovertemplate=custom_hovertemplate)
        for frame in fig_map.frames:
            for data in frame.data:
                data.hovertemplate = custom_hovertemplate

        # starting animation from the last frame
        fig_map2 = go.Figure()
        for tr in fig_map.frames[-1].data:
            fig_map2.add_trace(tr)

        fig_map2.layout = fig_map.layout
        fig_map2.frames = fig_map.frames
        fig_map2.layout['sliders'][0]['active'] = len(fig_map.frames) - 1
        c.plotly_chart(fig_map2, use_container_width=True)


# TODO: refatorar esse mapa com aprendizados do mapa acima
def scatter_africa_map(df_africa, column):
    c = column
    coloured_map, initial_date, final_date = map_data(df_africa)

    map_count_column = 'percentage'
    countries = coloured_map['sov_a3'].unique()
    # TODO: colorir paises selecionados

    with st.container():
        # Building synthetic data to set initial and end date for dataframe
        coloured_map = map_synthetic_data_variant(coloured_map, initial_date, final_date)

        # Filling NA values
        coloured_map = map_fill_na_values(coloured_map, map_count_column)

        if coloured_map[map_count_column].empty:
            c.warning("No data to show for this lineage.")
            fig_map = px.line_geo(lat=[0, 0, 0, 0], lon=[0, 0, 0, 0])
        else:
            # c1.write(coloured_map)
            c.subheader("Genomes per lineage")

            ### variants legend
            legend_box = st.container()
            legend_box.write(custom_legend(concerned_variants, main_lineages_color_scheme, c))

            fig_map = px.scatter_geo(coloured_map, locations='sov_a3', hover_name='country',
                                     hover_data=['variant', map_count_column],
                                     labels={'percentage': 'Percentage of genomes', 'date_2weeks': 'Date'},
                                     animation_frame="date_2weeks", size=map_count_column, animation_group='country',
                                     color='variant', size_max=100,
                                     color_discrete_map=main_lineages_color_scheme
                                     )
            fig_map.update_traces(marker=dict(
                size=coloured_map[map_count_column],
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
            fig_map.layout['sliders'][0]['active'] = int(len(fig_map.frames))
            fig_map.update_layout(showlegend=False)
        c.plotly_chart(fig_map, use_container_width=True)
