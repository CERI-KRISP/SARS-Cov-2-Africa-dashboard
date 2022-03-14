import streamlit as st
from utils.functions import remote_css

# Config variables
GISAID_URL = 'https://www.epicov.org/epi3/3p/genafricadash/export/provision.json.xz'
GISAID_USERNAME = 'HouriiyahTegally'
GISAID_PASSWORD = 'vWXSlf3SqLSa'

## Hidding superior menu and edditing footer

css_changes = """
<style>
#MainMenu {
    visibility:hidden;
    }
footer{
    visibility:visible;
    }
footer:after{
    content: ' using GISAID data.'
</style>
"""