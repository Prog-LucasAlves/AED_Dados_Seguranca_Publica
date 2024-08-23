# Bibliotecas utilizadas
# import folium.map
import streamlit as st
from PIL import Image
import duckdb
# import folium
# from streamlit_folium import st_folium

# Configurações da página
img = Image.open("./image/4744315.png")

st.set_page_config(
    page_title="Em Construção",
    page_icon=img,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.extremelycoolapp.com/help",
        "Report a bug": "https://www.extremelycoolapp.com/bug",
        "About": "# This is a header. This is an *extremely* cool app!",
    },
)

# Caminho do arquivo parquet com os dados
path_parquet = "./data/raw_data/GOLDEN/GOLDEN_data.parquet"

# Caminho do arquivo com as descrições das variáveis
path_descricoes = "./data/dict_data/tipo_ocorrencia.csv"

# Título do dashboard
title = """
<p style="color:Black; font-size: 40px; font-weight: bolder;"
> Dashboard dos Dados da Segurança Pública do Estado do RJ </p>
"""
st.markdown(title, unsafe_allow_html=True)

# Colunas do dashboard
col1, col2, col3 = st.columns(3)

with col1:
    # Carregando as datas(ano)
    ano_df = duckdb.query(
        f"""SELECT DISTINCT ano
        FROM '{path_parquet}'
        ORDER BY ano"""
    ).to_df()
    ano = st.selectbox("Selecione o Ano", ano_df)

with col2:
    # Carregando o arquivo das descrições das variáveis
    titulo_df = duckdb.query(
        f"""SELECT descricao
        FROM '{path_descricoes}'"""
    ).to_df()
    titulo = st.selectbox("Titulo", titulo_df)

with col3:
    # Criando informação com o total de ocorrencias(Geral)
    titulo_ocorrencia = duckdb.query(
        f"""SELECT tipo_ocorrencia
        FROM '{path_descricoes}'
        WHERE descricao = '{titulo}'"""
    ).to_df()
    titulo_ocorrencia = titulo_ocorrencia.iloc[0, 0]
    st.markdown("TOTAL DE OCORRÊNCIAS")

    total_titulo_df = duckdb.query(
        f"""SELECT SUM({titulo_ocorrencia})
        FROM '{path_parquet}'"""
    ).to_df()
    total_titulo_df = total_titulo_df.iloc[0, 0]
    total_titulo = st.markdown(f"{total_titulo_df:.0f}")

# Criando Mapa
path_mapa = "./data/map/geojs-33-mun.json"

# m = folium.Map(location=([-22.42, -42.48]), zoom_start=7)

# style = lambda x: {"color": "#000000", "fillOpacity": 0, "weight": 1}

# folium.GeoJson(path_mapa, style_function=style).add_to(m)

# st_folium(m, height=350, width=790)

"""
folium.Choropleth(
    geo_data=d).add_to(m)
st_map = st_folium(m, height=350, width=750)
"""
