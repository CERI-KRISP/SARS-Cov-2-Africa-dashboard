# Import project packages
from config import *
from source.pages import sidebar as sd
from source.pages.header import *
from source.graphs.africa_map import *
from source.graphs.variants_proportion import variants_bar_plot
from source.graphs.countries_sequences import countries_with_sequences_chart, countries_with_sequences_chart_one_variant

# Import Python Libraries
import pandas as pd
from PIL import Image


def main():
    st.set_page_config(
        page_title="SARS-COV-2 Dashboard - Genomics Africa ",
        layout="wide",
        initial_sidebar_state="expanded",
        page_icon="img/cropped-ceri_branco-01-150x150.png"
    )

    st.markdown(css_changes, unsafe_allow_html=True)
    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

    ## Getting the data
    df_africa = load_data('data/all_data_processed.csv')

    ##### CHECK LAST UPDATE #####
    last_update = last_file_update('data/all_data_processed.csv')

    ## Add sidebar to the app
    st.sidebar.title("GENOMICS AFRICA")
    st.sidebar.subheader("Last update: %s" % last_update)

    # Sidebar filter data
    st.sidebar.markdown(" ")
    st.sidebar.header("Filter data ")

    ### Begin of filters

    # form = st.sidebar.form("Filters_form", clear_on_submit=True)

    # Filter data by countries
    countries_choice, display_countries = sd.get_countries_choice(df_africa)

    # Sidebar filter lineages
    lineages_choice = sd.get_lineages_choice(df_africa)

    # Sidebar filter period
    start_date, end_date = sd.get_dates_choice(df_africa)

    ### Auxiliar dataframes ###

    # Couting variants
    df_count = sd.build_df_count(df_africa)

    # Building percentage dataframe
    variants_percentage = sd.build_variant_percentage_df(df_count)

    ### Filter and reset buttons ###
    bt_col_1, bt_col_2 = st.sidebar.columns(2)
    if bt_col_1.button("Reset filters", key='button_reset_filters'):
        sd.reset_filters(df_africa)

    # # Button to call filtering function
    if bt_col_2.button("Filter data", key='button_filter'):
        df_africa = sd.filter_df_africa(countries_choice, lineages_choice, start_date, end_date, df_africa)
        variant_count = sd.build_variant_count_df(df_africa)
        df_count = sd.build_df_count(df_africa)
        variants_percentage = sd.build_variant_percentage_df(df_count)

    # Metrics
    sd.show_metrics(df_africa)

    # End of sidebar
    st.sidebar.header("About")
    sd.about_section()
    # st.sidebar.header("Acknowledgment")
    # sd.acknowledgment_section(logo_path='img/gisaid_logo.png', link='https://www.gisaid.org/')

    # Add title and subtitle to the main interface of the app
    main_title(display_countries)

    ### Layout of main page
    c1, c2 = st.columns((1.5, 1.9))

    ############ First column ###############
    ############## MAP CHART ################
    c1.subheader("Genomes per country")
    map_option = c1.selectbox(
        'Metric',
        ('Total of genomes', 'Genomes by variant'
         # 'Variants proportion'
         ))
    if map_option == 'Total of genomes':
        colorpath_africa_map(df_count, column=c1, color_pallet="Greens")
    elif map_option == 'Genomes by variant':
        # Multiselect to choose variants to show
        voc_selected = c1.selectbox("Choose VOC to show", concerned_variants)
        df_count_map = sd.build_df_count(df_africa[df_africa['variant'] == voc_selected])
        colorpath_africa_map(df_count_map, column=c1, color_pallet=vocs_color_pallet.get(voc_selected))
    # elif map_option == 'Variants proportion':
    #     c1.write(variants_percentage.head())
    #     scatter_africa_map(variants_percentage, column=c1, map_count_column='Count')

    ############ Second column ###############
    ####### Circulating lineages CHART ###########
    variants_bar_plot(variants_percentage, c2)

    ####### COUNTRIES WHITH SEQUENCE CHART #########
    countries_with_sequences_chart(df_count, c2)

    ########### TABLE WEEKLY VARIANT SUMMARY #########
    st.header("Variant details")
    weekly_variants_df = pd.read_csv("data/variants_summary_table.csv", usecols=['Variants', 'Lineage_sublineage',
                                                                                 'FirstSequence',
                                                                                 'Total_Confirmed', 'SamplesPast30',
                                                                                 'DaysSince'])
    weekly_variants_df = weekly_variants_df[['Variants', 'Lineage_sublineage', 'FirstSequence', 'Total_Confirmed',
                                             'SamplesPast30', 'DaysSince']]
    rename_weekly_columns = {'Lineage_sublineage': 'Lineage/sub-lineages', 'Total_Confirmed': 'Total sequences',
                          'SamplesPast30': 'Sampled and submitted last 30 days',
                          'FirstSequence': 'First sequence', 'DaysSince': 'Days since last sequence'}
    weekly_variants_df.rename(columns=rename_weekly_columns, inplace=True)
    with st.container():
        with st.expander("Africa weekly variant summary"):
            st.table(weekly_variants_df)

    c1_2, c2_2 = st.columns((1, 1))
    with c1_2.container():
        with c1_2.expander("Alpha variant"):
            alpha_img = Image.open("data/figures/alpha-stanford-3-1536x226.png")
            st.image(alpha_img, caption="SARS_CoV2 Alpha variant sequence")
            countries_with_sequences_chart_one_variant(df_count, st, variant='Alpha', start_date=start_date,
                                                       color=main_lineages_color_scheme.get('Alpha'))

    with c2_2.container():
        with c2_2.expander("Beta variant"):
            beta_img = Image.open("data/figures/Beta-stanford.png")
            st.image(beta_img, caption="SARS_CoV2 Beta variant sequence")
            countries_with_sequences_chart_one_variant(df_count, st, variant='Beta', start_date=start_date,
                                                       color=main_lineages_color_scheme.get('Beta'))

    with c1_2.container():
        with c1_2.expander("Delta variant"):
            delta_img = Image.open("data/figures/Delta-stanford.png")
            st.image(delta_img, caption="SARS_CoV2 Delta variant sequence")
            countries_with_sequences_chart_one_variant(df_count, st, variant='Delta', start_date=start_date,
                                                       color=main_lineages_color_scheme.get('Delta'))

    with c2_2.container():
        with c2_2.expander("Omicron variant"):
            omicron_img = Image.open("data/figures/omicron-stanford.png")
            st.image(omicron_img, caption="SARS_CoV2 Omicron variant sequence")
            countries_with_sequences_chart_one_variant(df_count, st, variant='Omicron', start_date=start_date,
                                                       color=main_lineages_color_scheme.get('Omicron'))

    # with c1_2.container():
    #     with c1_2.expander("A.23.1 variant"):
    #         a231_img = Image.open("data/figures/a231-stanford.png")
    #         st.image(a231_img, caption="SARS_CoV2 A.23.1 variant sequence")
    #
    # with c2_2.container():
    #     with c2_2.expander("B.1.1.318 variant"):
    #         b11318_img = Image.open("data/figures/b11318-stanford.png")
    #         st.image(b11318_img, caption="SARS_CoV2 B.1.1.318 variant sequence")
    #
    # with c1_2.container():
    #     with c1_2.expander("C.1 variant"):
    #         c1_img = Image.open("data/figures/c1-stanford.png")
    #         st.image(c1_img, caption="SARS_CoV2 C.1 variant sequence")
    #
    # with c2_2.container():
    #     with c2_2.expander("C.1.2 variant"):
    #         c12_img = Image.open("data/figures/c12-stanford.png")
    #         st.image(c12_img, caption="SARS_CoV2 C.1.2 variant sequence")
    #
    # with c1_2.container():
    #     with c1_2.expander("C.36.3 variant"):
    #         c363_img = Image.open("data/figures/c.36.3-stanford.png")
    #         st.image(c363_img, caption="SARS_CoV2 C.36.3 variant sequence")
    #
    # with c2_2.container():
    #     with c2_2.expander("Eta variant"):
    #         eta_img = Image.open("data/figures/Eta-stanford.png")
    #         st.image(eta_img, caption="SARS_CoV2 Eta variant sequence")


if __name__ == "__main__":
    main()
