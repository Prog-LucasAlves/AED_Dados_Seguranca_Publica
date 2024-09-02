# Bibliotecas utilizadas
import folium.map
import streamlit as st
from PIL import Image
import duckdb
import folium
from streamlit_folium import st_folium
from branca.colormap import linear

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
<p style="color:Black; font-size: 30px; font-weight: bolder;"
> Dashboard dos Dados da Segurança Pública do Estado do RJ </p>
"""
st.markdown(title, unsafe_allow_html=True)

# Colunas do dashboard
col1, col2 = st.columns((1, 2))

with col1:
    # Carregando as datas(ano)
    ano_df = duckdb.query(
        f"""SELECT DISTINCT ano
        FROM '{path_parquet}'
        ORDER BY ano"""
    ).to_df()
    ano = st.selectbox("Selecione o Ano", ano_df)

with col2:
    # Carregando as descrições das ocorrências
    titulo_df = duckdb.query(
        f"""SELECT descricao
        FROM '{path_descricoes}'
        ORDER BY descricao"""
    ).to_df()
    titulo = st.selectbox("Titulo", titulo_df)


# Criando informação com o total de ocorrências(Geral)
titulo_ocorrencia = duckdb.query(
    f"""SELECT tipo_ocorrencia
    FROM '{path_descricoes}'
    WHERE descricao = '{titulo}'"""
).to_df()
titulo_ocorrencia = titulo_ocorrencia.iloc[0, 0]

# Criando informação com o total de ocorrências por município no mapa
total_titulo_map = duckdb.query(
    f"""SELECT ano, fmun, fmun_cod, SUM({titulo_ocorrencia})
    FROM '{path_parquet}'
    WHERE ano = '{ano}'
    GROUP BY ano, fmun, fmun_cod
    """
).to_df()

total_titulo_map.columns = ["Ano", "Município", "Município_cod", "Total"]
total_titulo_map["Município_cod"] = total_titulo_map["Município_cod"].astype(str)
total_titulo_map_index = total_titulo_map.set_index("Município_cod")["Total"]

with col1:
    # Grafico de barras | Total de ocorrências por Mês
    total_mes = duckdb.query(
        f"""SELECT mes AS Mês, SUM({titulo_ocorrencia}) AS Total
        FROM '{path_parquet}'
        WHERE ano = '{ano}'
        GROUP BY mes
        """
    ).to_df()

    st.bar_chart(
        data=total_mes,
        x="Mês",
        y="Total",
        color="#3CB371",
        horizontal=True,
        # width=1,
        # height=380,
        # use_container_width=True,
    )

with col2:
    # Criando Mapa
    path_mapa = "./data/map/geojs-33-mun.json"

    colormap = linear.YlGn_09.scale(
        total_titulo_map["Total"].min(), total_titulo_map["Total"].max()
    )

    color_dict = {
        key: colormap(total_titulo_map_index[key])
        for key in total_titulo_map_index.keys()
    }

    m = folium.Map(location=([-22.42, -42.48]), zoom_start=7)

    folium.GeoJson(
        path_mapa,
        name="geojson",
        zoom_on_click=True,
        style_function=lambda feature: {
            "fillColor": color_dict[feature["id"]],
            "color": "black",
            "weight": 0.3,
            "fillOpacity": 0.5,
        },
    ).add_to(m)

    colormap.caption = ""
    colormap.add_to(m)

    st_folium(m, height=350, width=570)

    folium.LayerControl().add_to(m)

# Metricas

col1, col2, col3 = st.columns(3)

total_ocorrencias_2024 = duckdb.query(
    f"""SELECT SUM({titulo_ocorrencia}) AS Total
    FROM '{path_parquet}'
    WHERE ano = '2024'
    """
).to_df()

metricas_2024 = total_ocorrencias_2024["Total"].sum()
metricas_2024 = int(metricas_2024)
M1 = (metricas_2024 / total_titulo_map["Total"].sum()) - 1
col1.metric(
    label="Total de Ocorrências em 2024:",
    value=f"{metricas_2024:.0f}",
    delta=f"{M1:.2%}",
)

col2.metric(
    label=f"Total de Ocorrências em {ano}:",
    value=f"{total_titulo_map['Total'].sum():.0f}",
)

st.markdown("---")

# Observação
with st.expander("**Observação:**", expanded=True):
    if titulo == "Crimes Violentos Letais Intencionais*":
        CVLI = """
<p style="color:Black; font-size: 15px; font-weight: bolder;"
> *Crimes Violentos Letais Intencionais: Homicídio doloso + Lesão corporal seguida de morte + Latrocínio. </p>
"""
        st.markdown(CVLI, unsafe_allow_html=True)

    elif titulo == "Letalidade violenta*":
        LV = """
<p style="color:Black; font-size: 15px; font-weight: bolder;"
> *Letalidade violenta: Homicídio doloso + Lesão corporal seguida de morte + Latrocínio + Morte por intervenção de agente do Estado. </p>
"""
        st.markdown(LV, unsafe_allow_html=True)

st.markdown("---")

# ########## Barra Lateral ###########
st.sidebar.title("Filtros")
st.sidebar.subheader(f"{ano} | {titulo}")

# Barra Lateral | Total de Ocorrências
total_ocorrencias = total_titulo_map["Total"].sum()
total_ocorrencias = int(total_ocorrencias)

st.sidebar.markdown("---")

# Barra Lateral | Municípios
municipios_df = duckdb.query(
    f"""SELECT DISTINCT fmun
    FROM '{path_parquet}'
    ORDER BY fmun"""
).to_df()

municipio = st.sidebar.selectbox("Município:", municipios_df)

# Barra Lateral | Municípios | Total de Ocorrências
total_municipio_df = duckdb.query(
    f"""SELECT SUM({titulo_ocorrencia})
    FROM '{path_parquet}'
    WHERE fmun = '{municipio}'
    AND ano = '{ano}'
    """
).to_df()

total_municipio = st.sidebar.text(
    f"Total de Ocorrências: {total_municipio_df.iloc[0, 0]:.0f}"
)

represent_municipio = total_municipio_df.iloc[0, 0] / total_ocorrencias

represent_municipio_select = st.sidebar.text(
    f"Representatividade: {represent_municipio:.2%}"
)

st.sidebar.markdown("---")

# Barra Lateral | Região
regiao_df = duckdb.query(
    f"""SELECT DISTINCT regiao
    FROM '{path_parquet}'
    ORDER BY regiao
    """
).to_df()

regiao = st.sidebar.selectbox("Região:", regiao_df)

# Barra Lateral | Região | Total de Ocorrências
total_regiao_df = duckdb.query(
    f"""SELECT SUM({titulo_ocorrencia})
    FROM '{path_parquet}'
    WHERE regiao = '{regiao}'
    AND ano = '{ano}'
    """
).to_df()

total_regiao = st.sidebar.text(
    f"Total de Ocorrências: {total_regiao_df.iloc[0, 0]:.0f}"
)

represent_regiao = total_regiao_df.iloc[0, 0] / total_ocorrencias

represent_regiao_select = st.sidebar.text(f"Representatividade: {represent_regiao:.2%}")
# ########## Barra Lateral ###########
