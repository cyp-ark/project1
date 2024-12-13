import folium
import streamlit as st

from streamlit_folium import st_folium

# center on Liberty Bell, add marker
m = folium.Map(location=[37.527115069277635, 126.9207860008731], zoom_start=16)
folium.Marker(
    [37.527115069277635, 126.9207860008731], popup="KDB산업은행 본사", tooltip="KDB산업은행 본사"
).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)