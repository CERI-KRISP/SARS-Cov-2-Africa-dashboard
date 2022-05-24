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