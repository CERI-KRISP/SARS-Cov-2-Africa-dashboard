import streamlit as st
from utils.functions import remote_css

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