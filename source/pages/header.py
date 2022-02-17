import streamlit as st

def main_title(display_countries):
    st.markdown("<h1 style='text-align: center; color: #FF7557;'>SARS-COV-2 AFRICA DASHBOARD</h1>",
                unsafe_allow_html=True)

    st.markdown("<h5 style='text-align: center;'>Showing results from %s </h5>" % display_countries,
                unsafe_allow_html=True)