import streamlit as st
from PIL import Image

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