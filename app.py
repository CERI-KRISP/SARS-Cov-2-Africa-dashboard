# Import project packages
import datetime

from config import *
from source.pages.sidebar import *
from source.pages.header import *
from source.graphs.africa_map import *
from source.graphs.variants_proportion import variants_bar_plot
from source.graphs.countries_sequences import countries_with_sequences_chart
from utils.data_process import *

# Import Python Libraries
import pandas as pd
from PIL import Image
import os

def main():
    st.set_page_config(
        page_title="SARS-COV-2 Dashboard - Genomics Africa ",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(css_changes, unsafe_allow_html=True)
    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

    ##### CHECK LAST UPDATE #####
    last_update = last_file_update('data/gisaid_data/provision.json.xz')

    ##### CHECK VARIABLE FOR INPUT ######
    if data_source == "metadata":
        df_africa = process_data_from_gisaid_metadata()
    if data_source == "GISAID_API":
        df_africa, last_update = process_data_from_gisaid_api(last_update)
    else:
        print("Invalid data source. Please, see the documentation.")

    # TODO: fazer função para contar as variantes por data e país (substituir arquivo Houriiyah)

    ## Add sidebar to the app
    st.sidebar.title("GENOMICS AFRICA")
    st.sidebar.subheader("Results Updated – %s" % last_update)

    # Sidebar filter data
    st.sidebar.markdown(" ")
    st.sidebar.header("Filter data ")
    df_africa, display_countries = filter_countries(df_africa)

    # Sidebar filter lineages
    df_africa, variant_count = filter_lineages(df_africa)

    # Couting variants
    df_count = df_africa.groupby(['country', 'variant', 'date_2weeks']).size().reset_index(name='Count')

    # Building percentage dataframe
    variants_percentage = df_count.groupby(['date_2weeks', 'variant']).agg({'Count': 'sum'})
    variants_percentage = variants_percentage.groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))
    variants_percentage = variants_percentage.reset_index()

    # Sidebar filter period
    df_africa = filter_by_period(df_africa)

    # Metrics
    show_metrics(df_africa)

    # End of sidebar
    st.sidebar.header("About")
    about_section()
    st.sidebar.header("Acknowledgment")
    acknowledgment_section(logo_path='img/gisaid_logo.png', link='https://www.gisaid.org/')

    # Add title and subtitle to the main interface of the app
    main_title(display_countries)

    ### Layout of main page
    c1, c2 = st.columns((1.5, 1.9))

    ############ First column ###############
    ############## MAP CHART ################
    c1.subheader("Continent map")
    map_option = c1.selectbox(
        'Metric',
        ('Number of genomes', 'Variant prevalence'))
    if map_option == 'Number of genomes':
        colorpath_africa_map(df_count, column=c1)
    elif map_option == 'Variant prevalence':
        scatter_africa_map(df_count, column=c1)

    ############ Second column ###############
    ####### Circulating lineages CHART ###########
    variants_bar_plot(variants_percentage, c2)

    ####### COUNTRIES WHITH SEQUENCE CHART #########
    countries_with_sequences_chart(df_count, c2)

    ########### TABLE WEEKLY VARIANT SUMMARY #########
    st.header("Variant details")
    weekly_variants_df = pd.read_csv("data/Africa_weekly_variant_summary.csv")
    with st.container():
        with st.expander("Africa weekly variant summary"):
            st.table(weekly_variants_df)

    c1_2, c2_2 = st.columns((1, 1))
    with c1_2.container():
        with c1_2.expander("Alpha variant"):
            alpha_img = Image.open("data/figures/alpha-stanford-3-1536x226.png")
            st.image(alpha_img, caption="SARS_CoV2 Alpha variant sequence")

    with c2_2.container():
        with c2_2.expander("Beta variant"):
            beta_img = Image.open("data/figures/Beta-stanford.png")
            st.image(beta_img, caption="SARS_CoV2 Beta variant sequence")

    with c1_2.container():
        with c1_2.expander("Delta variant"):
            delta_img = Image.open("data/figures/Delta-stanford.png")
            st.image(delta_img, caption="SARS_CoV2 Delta variant sequence")

    with c2_2.container():
        with c2_2.expander("Omicron variant"):
            omicron_img = Image.open("data/figures/omicron-stanford.png")
            st.image(omicron_img, caption="SARS_CoV2 Omicron variant sequence")

    with c1_2.container():
        with c1_2.expander("A.23.1 variant"):
            a231_img = Image.open("data/figures/a231-stanford.png")
            st.image(a231_img, caption="SARS_CoV2 A.23.1 variant sequence")

    with c2_2.container():
        with c2_2.expander("B.1.1.318 variant"):
            b11318_img = Image.open("data/figures/b11318-stanford.png")
            st.image(b11318_img, caption="SARS_CoV2 B.1.1.318 variant sequence")

    with c1_2.container():
        with c1_2.expander("C.1 variant"):
            c1_img = Image.open("data/figures/c1-stanford.png")
            st.image(c1_img, caption="SARS_CoV2 C.1 variant sequence")

    with c2_2.container():
        with c2_2.expander("C.1.2 variant"):
            c12_img = Image.open("data/figures/c12-stanford.png")
            st.image(c12_img, caption="SARS_CoV2 C.1.2 variant sequence")

    with c1_2.container():
        with c1_2.expander("C.36.3 variant"):
            c363_img = Image.open("data/figures/c.36.3-stanford.png")
            st.image(c363_img, caption="SARS_CoV2 C.36.3 variant sequence")

    with c2_2.container():
        with c2_2.expander("Eta variant"):
            eta_img = Image.open("data/figures/Eta-stanford.png")
            st.image(eta_img, caption="SARS_CoV2 Eta variant sequence")

if __name__ == "__main__":
    main()


