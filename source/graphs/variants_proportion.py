import streamlit as st
import plotly.express as px
from utils.dicts import main_lineages_color_scheme, concerned_variants
from datetime import datetime, timedelta
import pandas as pd

#TODO consertar esse gráfico pra calcular porcentagem para todas as variantes

def variants_bar_plot(variants_percentage, column):
    c = column
    variants_percentage['date_initial'] = pd.to_datetime(variants_percentage['date_2weeks']) - timedelta(days=14)
    variants_percentage['date_initial'] = variants_percentage['date_initial'].dt.strftime('%Y-%m-%d')
    variants_percentage['Count'] = variants_percentage['Count'].astype(int)

    with st.container():
        c.subheader("Circulating lineages and variants")
        fig = px.bar(variants_percentage, x='date_2weeks', y='Count',
                     color='variant', color_discrete_map=main_lineages_color_scheme,
                     barmode='overlay',
                     custom_data=['variant', 'Count', 'date_initial', 'date_2weeks'],
                     labels={'variant': 'Lineage', 'Count': 'Percentage', 'date_2weeks': 'Date'})
        fig.update_yaxes(title="Proportion of Genomes")
        fig.update_xaxes(title="Date", range=[variants_percentage['date_2weeks'].min(), datetime.today()])
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.9,
            xanchor="right",
            x=1
        ), legend_title_text="Lineages", height=450)
        fig.update_layout(title=dict(y=1))
        # fig.update_layout(xaxis={'overlaying': "free"})

        # creating standardize hover template
        custom_hovertemplate = '<b>Lineage: %{customdata[0]} </b><br><br>' + \
                               '%{customdata[1]}% of genomes <br>from %{customdata[2]}' + \
                               ' to %{customdata[3]}<br>'

        fig.update_traces(hovertemplate=custom_hovertemplate)

        for frame in fig.frames:
            for data in frame.data:
                data.hovertemplate = custom_hovertemplate

        c.plotly_chart(fig, use_container_width=True)
