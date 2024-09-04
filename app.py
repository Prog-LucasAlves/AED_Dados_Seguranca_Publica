"""
Dashboard Dados Segurança Pública do RJ
"""

# Bibliotecas utilizadas
import folium.map
import streamlit as st
from PIL import Image
import duckdb
import folium
from streamlit_folium import st_folium
from branca.colormap import linear

# Diretório dos Dados
# Caminho do arquivo parquet com os dados
PATH_PARQUET = "./data/raw_data/GOLDEN/GOLDEN_data.parquet"

# Caminho do arquivo com as descrições das variáveis
PATH_DESCRIPTIONS = "./data/dict_data/tipo_ocorrencia.csv"

# Caminho do arquivo com o mapa do RJ
PATH_MAPA = "./data/map/geojs-33-mun.json"


def PypiConfigPage():
    """
    Função para configurar a página.
    """
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


def PypiTitle():
    """
    Função para exibir o título do dashboard.
    """
    TITLE = """
<p style="color:Black; font-size: 30px; font-weight: bolder;"
> Dashboard dos Dados da Segurança Pública do Estado do RJ </p>
"""
    st.markdown(TITLE, unsafe_allow_html=True)


def PypiInfoDash():
    """
    Função para criar os selectbox de data(Ano) | Ocorrência.
    """
    # Colunas do Selectbox
    col1, col2 = st.columns((1, 2))

    # Selectbox Ano
    ANODF = duckdb.query(
        f"""SELECT DISTINCT ano
        FROM '{PATH_PARQUET}'
        ORDER BY ano"""
    ).to_df()
    ANO = col1.selectbox("Selecione o Ano:", ANODF)

    # Selectbox Título Ocorrência
    TITULODF = duckdb.query(
        f"""SELECT descricao
        FROM '{PATH_DESCRIPTIONS}'
        ORDER BY descricao"""
    ).to_df()
    TITULO = col2.selectbox("Título da Ocorrência:", TITULODF)

    # Título das ocorrências
    TITULOOCORRENCIADF = duckdb.query(
        f"""SELECT tipo_ocorrencia
        FROM '{PATH_DESCRIPTIONS}'
        WHERE descricao = '{TITULO}'"""
    ).to_df()
    TITULOOCORRENCIA = TITULOOCORRENCIADF.iloc[0, 0]

    # Observação sobre o título da ocorrência
    if TITULO == "Crimes Violentos Letais Intencionais*":
        CVLI = """
<p style="color:DimGrey; font-size: 14px; font-weight: bolder;"
> *Crimes Violentos Letais Intencionais: Homicídio doloso + Lesão corporal seguida de morte + Latrocínio. </p>
"""
        st.markdown(CVLI, unsafe_allow_html=True)

    return ANO, TITULO, TITULOOCORRENCIA


def Pypigraphic(ano, tituloocorrencia):
    """
    Função para criar os gráficos(Barras | Mapa).
    """

    ANO = ano
    TITULOOCORRENCIA = tituloocorrencia

    # Colunas dos graficos
    col3, col4 = st.columns((1, 2))

    # Grafico de barras | Total de ocorrências por mês
    TOTALMESDF = duckdb.query(
        f"""SELECT mes AS Mês, SUM({TITULOOCORRENCIA}) AS Total
        FROM '{PATH_PARQUET}'
        WHERE ano = '{ANO}'
        GROUP BY mes
        ORDER BY mes"""
    ).to_df()

    col3.bar_chart(
        data=TOTALMESDF,
        x="Mês",
        y="Total",
        color="#3CB371",
        horizontal=True,
        width=1,
        height=380,
        use_container_width=True,
    )

    # Criando Mapa

    # Criando informação com o total de ocorrências por município.
    TOTALMUNICIPIODF = duckdb.query(
        f"""SELECT ano, fmun, fmun_cod, SUM({TITULOOCORRENCIA})
        FROM '{PATH_PARQUET}'
        WHERE ano = '{ANO}'
        GROUP BY ano, fmun, fmun_cod
        """
    ).to_df()

    TOTALMUNICIPIODF.columns = ["Ano", "Município", "Município_cod", "Total"]
    TOTALMUNICIPIODF["Município_cod"] = TOTALMUNICIPIODF["Município_cod"].astype(str)
    TOTALTITULODFINDEX = TOTALMUNICIPIODF.set_index("Município_cod")["Total"]

    with col4:
        colormap = linear.YlGn_09.scale(
            TOTALMUNICIPIODF["Total"].min(), TOTALMUNICIPIODF["Total"].max()
        )

        color_dict = {
            key: colormap(TOTALTITULODFINDEX[key]) for key in TOTALTITULODFINDEX.keys()
        }

        M = folium.Map(location=([-22.10, -42.48]), zoom_start=7)

        folium.GeoJson(
            PATH_MAPA,
            name="geojson",
            zoom_on_click=True,
            style_function=lambda feature: {
                "fillColor": color_dict[feature["id"]],
                "color": "black",
                "weight": 0.3,
                "fillOpacity": 0.5,
            },
        ).add_to(M)

        colormap.caption = ""
        colormap.add_to(M)

        st_folium(M, height=350, width=570)

        folium.LayerControl().add_to(M)


def PypiSidebar(ano, titulo):
    """
    Função para criar a barra lateral do dashboard.
    """

    ANO = ano
    TITULO = titulo

    st.sidebar.title("Filtros")
    st.sidebar.subheader(f"{ANO} | {TITULO}")

    st.sidebar.markdown("---")

    # Barra Lateral | Municípios
    MUNICIPIOSDF = duckdb.query(
        f"""SELECT DISTINCT fmun
        FROM '{PATH_PARQUET}'
        ORDER BY fmun"""
    ).to_df()

    MUNICIPIO = st.sidebar.selectbox("Município:", MUNICIPIOSDF)

    return MUNICIPIO


if __name__ == "__main__":
    PypiConfigPage()
    PypiTitle()
    resultano, resulttitulo, resultocorrencia = PypiInfoDash()
    Pypigraphic(resultano, resultocorrencia)
    PypiSidebar(resultano, resulttitulo)
