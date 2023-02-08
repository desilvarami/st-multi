import ast
import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

markdown = """
Web App URL: <https://template.streamlit.app>
GitHub Repository: <https://github.com/giswqs/streamlit-multipage-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)


@st.cache
def get_layers(url):
    options = leafmap.get_wms_layers(url)
    return options


st.title("DataHub WMS")
st.markdown(
    """
This app is a demonstration of loading Web Map Service (WMS) layers. Simply enter the URL of the WMS service 
in the text box below and press Enter to retrieve the layers. Go to https://apps.nationalmap.gov/services to find 
some WMS URLs if needed.
"""
)

row1_col1, row1_col2 = st.columns([3, 1.3])
width = None
height = 600
layers = None

with row1_col2:

    esa_landcover = "https://services.terrascope.be/wms/v2"
    url = st.text_input(
        "Enter a WMS URL:", value="https://services.terrascope.be/wms/v2"
    )
    empty = st.empty()

    if url:
        options = get_layers(url)

        default = None
        if url == esa_landcover:
            default = "WORLDCOVER_2020_MAP"
        layers = empty.multiselect(
            "Select WMS layers to add to the map:", options, default=default
        )
       

    with row1_col1:
        m = leafmap.Map(center=(36.3, 0), zoom=2)

        if layers is not None:
            for layer in layers:
                m.add_wms_layer(
                    url, layers=layer, name=layer, attribution=" ", transparent=True
                )
       
        m.to_streamlit(width, height)

