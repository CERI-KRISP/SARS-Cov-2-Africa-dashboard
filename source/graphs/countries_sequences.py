import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import timedelta, datetime

from utils.dicts import main_lineages_color_scheme


def countries_with_sequences_chart(df_count, column):
    c = column
    df_country_lineages = df_count.copy()

    df_country_lineages['date_initial'] = pd.to_datetime(df_country_lineages['date_2weeks']) - timedelta(days=14)
    df_country_lineages['date_initial'] = df_country_lineages['date_initial'].dt.strftime('%Y-%m-%d')

    with st.container():
        c.subheader("Sequence data available per country")
        country_lineages = px.scatter(df_country_lineages.sort_values(by='variant', ascending=False), x="date_2weeks",
                                      y="country", color="variant", custom_data=['country','variant', 'date_2weeks', 'Count'],
                                     color_discrete_map=main_lineages_color_scheme)
        country_lineages.update_traces(marker=dict(size=13, line=dict(width=0.5, color='#E5ECF6')))
        country_lineages.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="right",
            x=1
        ), legend_title_text="Variants")
        country_lineages.update_layout(title=dict(y=1), yaxis={'categoryorder': 'category descending'})
        country_lineages.update_yaxes(title="Country")
        country_lineages.update_xaxes(title="Date", range=[df_country_lineages['date_2weeks'].min(), datetime.today()])

        # creating standardize hover template
        custom_hovertemplate = '<b>Country: %{customdata[0]} </b><br><br>' + \
                               'Variant: %{customdata[1]} <br>Date: %{customdata[2]} <br>' +\
                                'Genomes: %{customdata[3]} <br>'

        country_lineages.update_traces(hovertemplate=custom_hovertemplate)

        for frame in country_lineages.frames:
            for data in frame.data:
                data.hovertemplate = custom_hovertemplate

        c.plotly_chart(country_lineages, use_container_width=True)


def countries_with_sequences_chart_one_variant(df_count, column, variant, start_date):
    c = column
    df_country_lineages = df_count[df_count['variant'] == variant]

    df_country_lineages['date_initial'] = pd.to_datetime(df_country_lineages['date_2weeks']) - timedelta(days=14)
    df_country_lineages['date_initial'] = df_country_lineages['date_initial'].dt.strftime('%Y-%m-%d')

    with st.container():
        country_lineages = px.scatter(df_country_lineages.sort_values(by='variant', ascending=False), x="date_2weeks",
                                      y="country", color="variant", custom_data=['country','variant', 'date_2weeks', 'Count'],
                                      color_discrete_sequence=['#6c757d'])
        country_lineages.update_traces(marker=dict(size=13, line=dict(width=0.5, color='#E5ECF6')))
        country_lineages.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="right",
            x=1
        ), legend_title_text="Variants")
        country_lineages.update_layout(title=dict(y=1), yaxis={'categoryorder': 'category descending'})
        country_lineages.update_yaxes(title="Country")
        country_lineages.update_xaxes(title="Date", range=[start_date, datetime.today()])

        # creating standardize hover template
        custom_hovertemplate = '<b>Country: %{customdata[0]} </b><br><br>' + \
                               'Variant: %{customdata[1]} <br>Date: %{customdata[2]} <br>' + \
                               'Genomes: %{customdata[3]} <br>'

        country_lineages.update_traces(hovertemplate=custom_hovertemplate)

        for frame in country_lineages.frames:
            for data in frame.data:
                data.hovertemplate = custom_hovertemplate

        c.plotly_chart(country_lineages, use_container_width=True)