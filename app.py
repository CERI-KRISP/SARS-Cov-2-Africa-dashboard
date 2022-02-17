# Import project packages

from config import *
from source.pages.sidebar import *
from source.pages.header import *
from source.graphs.africa_map import *
from source.graphs.variants_proportion import variants_bar_plot
from source.graphs.countries_sequences import countries_with_sequences_chart

# Import Python Libraries
import pandas as pd
from PIL import Image


def main():
    st.set_page_config(
        page_title="SARS-COV-2 Dashboard - Genomics Africa ",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(css_changes, unsafe_allow_html=True)
    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

    ##### INPUTS ######
    df_africa_path = "./data/africa.csv"
    df_africa = pd.read_csv(df_africa_path)
    df_africa = df_africa[df_africa.pangolin_lineage2 != 'None']

    # Add variant name columns
    df_africa['variant'] = df_africa['pangolin_lineage2']
    df_africa.replace({"variant": variant_names}, inplace=True)
    df_africa['variant'] = lineages_to_concerned_variants(df_africa, 'variant')
    last_update = "17 February 2022"

    ## Add sidebar to the app
    st.sidebar.title("GENOMICS AFRICA")
    st.sidebar.subheader("Results Updated – %s" % last_update)

    # Sidebar filter data
    st.sidebar.markdown(" ")
    st.sidebar.header("Filter data ")
    df_africa, display_countries = filter_countries(df_africa)

    # Sidebar filter lineages
    df_africa, variant_count = filter_lineages(df_africa)

    # Building percentage dataframe
    variants_percentage = df_africa.groupby(['date2', 'variant']).agg({'Count': 'sum'})
    variants_percentage = variants_percentage.groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))
    variants_percentage = variants_percentage.reset_index()

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
    scatter_africa_map(df_africa, column=c1)

    ############ Second column ###############
    ####### TOP 20 CHART ###########
    variants_bar_plot(variants_percentage, c2)

    ####### COUNTRIES WHITH SEQUENCE CHART #########
    countries_with_sequences_chart(df_africa, c2)

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


