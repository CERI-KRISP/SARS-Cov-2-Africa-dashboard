import streamlit as st
import plotly.express as px
from utils.dicts import main_lineages_color_scheme, concerned_variants
from datetime import datetime
#TODO consertar esse gráfico pra calcular porcentagem para todas as variantes



def variants_bar_plot(variants_percentage, column):
    c = column
    with st.container():
        c.subheader("Circulating lineages and variants")
        variants_percentage.sort_values(by=['variant'], inplace=True)
        # variants_percentage_aux = variants_percentage[variants_percentage.variant == 'Other Lineages']
        # variants_percentage = variants_percentage[variants_percentage.variant != 'Other Lineages']
        # variants_percentage.sort_values(by=['Count'], ascending=False, inplace=True)
        # variants_percentage = variants_percentage.append(variants_percentage_aux)
        fig = px.bar(variants_percentage, x='date_2weeks', y='Count',
                     color='variant', color_discrete_map=main_lineages_color_scheme,
                     barmode='relative',
                     custom_data=['variant', 'Count', 'date_2weeks'],
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
        c.plotly_chart(fig, use_container_width=True)
