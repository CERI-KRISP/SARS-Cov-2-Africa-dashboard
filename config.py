import streamlit as st
from utils.functions import remote_css

#Fill data_source variable with 'GISAID_API' if you are going to use GISAID feed data or 'metadata' to use a metadata file
data_source = "GISAID_API"

# Setup GISAID variables if you are using GISAID feed data
GISAID_URL = 'https://www.epicov.org/epi3/3p/genafricadash/export/provision.json.xz'
GISAID_USERNAME = 'HouriiyahTegally'
GISAID_PASSWORD = 'vWXSlf3SqLSa'

## Hidding superior menu and edditing footer

css_changes = """
<style>
#MainMenu {
    visibility:visible;
    }
footer{
    visibility:visible;
    }
footer:after{
    content: ' using GISAID data.'
</style>
"""