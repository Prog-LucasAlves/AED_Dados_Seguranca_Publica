import streamlit as st
from PIL import Image

img = Image.open('https://cdn-icons-png.flaticon.com/24/1085/1085456.png')

st.beta_set_page_config(page_title='Em Construção', page_icon=img)