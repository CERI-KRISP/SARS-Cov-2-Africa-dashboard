import streamlit as st

from utils.functions import get_img_with_href


def main_title(display_countries):
    st.markdown("<h1 style='text-align: center; color: #bd3133;'>SARS-COV-2 AFRICA DASHBOARD</h1>",
                unsafe_allow_html=True)
    logo = get_img_with_href('img/gisaid_logo.png','https://www.gisaid.org/')

    st.markdown("<p style='text-align: center;'>Enable by data from"+logo+"</p>",
                unsafe_allow_html=True)

    st.markdown("<h5 style='text-align: center;'>Showing results from %s </h5>" % display_countries,
                unsafe_allow_html=True)