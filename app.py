import streamlit as st
from PIL import Image

img = Image.open('./image/4744315.png')

st.beta_set_page_config(page_title='Em Construção', page_icon=img)