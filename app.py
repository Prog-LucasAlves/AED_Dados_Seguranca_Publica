import streamlit as st
from PIL import Image
from streamlit_folium import st_folium
import folium

img = Image.open('./image/4744315.png')

st.set_page_config(
    page_title='Em Construção', 
    page_icon=img,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })

st.title('APP Em Construção')

map = folium.Map(
    location=[23.54,  334.53], 
    zoom_start=4, 
    scrollWheelZoom=False, 
    tiles='CartoDB positron')

# call to render Folium map in Streamlit
st_data = st_folium(map, width=700, height=450)