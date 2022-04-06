import streamlit as st
import plotly.express as px

from utils.dicts import main_lineages_color_scheme


def countries_with_sequences_chart(df_africa, column):
    c = column
    df_country_lineages = df_africa.copy()

    with st.container():
        c.subheader("Sequence data available per country")
        country_lineages = px.scatter(df_country_lineages, x="date_2weeks", y="country", color="variant",
                                     color_discrete_map=main_lineages_color_scheme)
        country_lineages.update_traces(marker=dict(size=15, line=dict(width=0.5, color='#E5ECF6')))
        country_lineages.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="right",
            x=1
        ), legend_title_text="Variants")
        country_lineages.update_layout(title=dict(y=1), yaxis={'categoryorder': 'category descending'})
        c.plotly_chart(country_lineages, use_container_width=True)