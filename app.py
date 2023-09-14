import streamlit as st
from PIL import Image

img = Image.open('https://cdn-icons-png.flaticon.com/128/2827/2827410.png')

st.beta_set_page_config(page_title='Em Construção', page_icon=img)