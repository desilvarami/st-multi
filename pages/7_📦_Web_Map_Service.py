import ast
import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

markdown = """
Web App URL: <https://desilvarami-st-multi-streamlit-app-ge5ygf.streamlit.app/>
GitHub Repository: <https://github.com/desilvarami/st-multi/>
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
This map brings down a dataset from UNOSAT-DATAHUB. The Default layer is ETH_adm1, representing Admin Boundaries of Ethiopia. Hence the Map Center is set to Ethiopia.
"""
)

row1_col1, row1_col2 = st.columns([3, 1.3])
width = None
height = 600
layers = None

with row1_col2:

    DataHub = "https://unosat-datahub.cern.ch/geoserver/geonode/wms?"
    url = st.text_input(
        "Enter a WMS URL:", value="https://unosat-datahub.cern.ch/geoserver/geonode/wms?"
    )
    empty = st.empty()

    if url:
        options = get_layers(url)

        default = None
        if url == DataHub:
            default = "ETH_adm1"
        layers = empty.multiselect(
            "Select WMS layers to add to the map:", options, default=default
        )
       

    with row1_col1:
        m = leafmap.Map(center=(8, 40), zoom=5)

        if layers is not None:
            for layer in layers:
                m.add_wms_layer(
                    url, layers=layer, name=layer, attribution=" ", transparent=True
                )
       
        m.to_streamlit(width, height)

