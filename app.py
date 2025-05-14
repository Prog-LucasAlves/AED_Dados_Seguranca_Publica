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

# Caminho do arquivo com as coordenadas geográficas dos municipios de RJ
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
<p style="
    color: Black;
    font-size: 30px;
    font-weight: bolder;"
> 🔍 Dashboard dos Dados da Segurança Pública do Estado do RJ </p>
"""
    st.markdown(TITLE, unsafe_allow_html=True)


def PypiAttData():
    """
    Função para exibir os dados de Atualização.
    """

    DATA = duckdb.query(
        f"""SELECT mes_nome, mes, ano
        FROM '{PATH_PARQUET}'
        ORDER BY ano DESC, mes DESC"""
    ).to_df()

    DATAATTMES = DATA.iloc[0, 0]
    DATAATTANO = DATA.iloc[0, 2]

    ATT = f"""
<p style="color:DimGrey; font-size: 14px; font-weight: bolder;"
> Atualização: {DATAATTMES} | {DATAATTANO} </p>
"""
    st.markdown(ATT, unsafe_allow_html=True)

    return DATAATTMES


def PypiInfoGeral():
    """
    Função para criar os selectbox de data(Ano) | Ocorrência.
    """
    # Colunas do Selectbox
    (col1,) = st.columns((1))

    # Selectbox Título Ocorrência
    TITULODF = duckdb.query(
        f"""SELECT descricao
        FROM '{PATH_DESCRIPTIONS}'
        ORDER BY descricao"""
    ).to_df()
    TITULO = col1.selectbox("​📝​Título da Ocorrência:", TITULODF["descricao"], key="T1")

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

    elif TITULO == "Letalidade Violenta*":
        LV = """
<p style="color:DimGrey; font-size: 14px; font-weight: bolder;"
> *Homicídio doloso + Lesão corporal seguida de morte + Latrocínio + Morte por intervenção de agente do Estado. </p>
"""
        st.markdown(LV, unsafe_allow_html=True)

    elif TITULO == "Homicídio Culposo (Trânsito)*":
        LV = """
<p style="color:DimGrey; font-size: 14px; font-weight: bolder;"
> *Atropelamento + colisão + outros. </p>
"""
        st.markdown(LV, unsafe_allow_html=True)

    return TITULO, TITULOOCORRENCIA


def PypigraphicGeral(tituloocorrencia):
    """
    Função para criar os gráficos(Barras | Mapa).
    """

    TITULOOCORRENCIA = tituloocorrencia

    # Colunas dos graficos
    col3, col4 = st.columns((1, 2))

    # Grafico de barras | Total de ocorrências por mês
    TOTALMESDF = duckdb.query(
        f"""SELECT ano AS Ano, SUM({TITULOOCORRENCIA}) AS Total
        FROM '{PATH_PARQUET}'
        GROUP BY ano
        ORDER BY ano"""
    ).to_df()

    col3.bar_chart(
        data=TOTALMESDF,
        x="Ano",
        y="Total",
        color="#3CB371",
        horizontal=True,
        width=1,
        height=380,
        use_container_width=True,
    )

    st.divider()

    # Criando Mapa

    # Criando Informação com o Total de Ocorrências por Munic
    TOTALGERALDF = duckdb.query(
        f"""SELECT ano, fmun, fmun_cod, SUM({TITULOOCORRENCIA})
        FROM '{PATH_PARQUET}'
        GROUP BY ano, fmun, fmun_cod
        """
    ).to_df()

    TOTALGERALDF.columns = ["Ano", "Município", "Município_cod", "Total"]
    TOTALGERALDF["Município_cod"] = TOTALGERALDF["Município_cod"].astype(str)
    TOTALTITULODFINDEX = TOTALGERALDF.set_index("Município_cod")["Total"]

    with col4:
        colormap = linear.YlGn_09.scale(
            TOTALGERALDF["Total"].min(), TOTALGERALDF["Total"].max()
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

    return TOTALGERALDF


def PypiMetrics(tituloocorrencia):
    """
    Função para criar as métricas do dashboard.
    """

    TITULOOCORRENCIA = tituloocorrencia

    T = """
    <p style="
    color: Black;
    font-size: 20px;
    font-weight: bolder;
    font-family: Arial, Helvetica, sans-serif; "
> 📋​Comparativo Anual de Ocorrências: 2025 | 2024 | 2023 | 2022 | 2021 </p>
"""
    st.markdown(T, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns((1, 1, 1, 1, 1))

    TOTALOC2020 = duckdb.query(
        f"""SELECT SUM({TITULOOCORRENCIA})
        FROM '{PATH_PARQUET}'
        WHERE ano = '2020'
        """
    ).to_df()

    TOTALOC2021 = duckdb.query(
        f"""SELECT SUM({TITULOOCORRENCIA})
        FROM '{PATH_PARQUET}'
        WHERE ano = '2021'
        """
    ).to_df()

    DIFFOC2021 = (TOTALOC2020 / TOTALOC2021) - 1

    col5.metric(
        label="⌛Total de Ocorrências em 2021:",
        value=f"{TOTALOC2021.iloc[0, 0]:.0f}",
        delta=f"{DIFFOC2021.iloc[0, 0]:.2%}",
    )

    TOTALOC2022 = duckdb.query(
        f"""SELECT SUM({TITULOOCORRENCIA})
        FROM '{PATH_PARQUET}'
        WHERE ano = '2022'
        """
    ).to_df()

    DIFFOC2122 = (TOTALOC2022 / TOTALOC2021) - 1

    col4.metric(
        label="⌛Total de Ocorrências em 2022:",
        value=f"{TOTALOC2022.iloc[0, 0]:.0f}",
        delta=f"{DIFFOC2122.iloc[0, 0]:.2%}",
    )

    TOTALOC2023 = duckdb.query(
        f"""SELECT SUM({TITULOOCORRENCIA})
        FROM '{PATH_PARQUET}'
        WHERE ano = '2023'
        """
    ).to_df()

    DIFFOC2322 = (TOTALOC2023 / TOTALOC2022) - 1

    col3.metric(
        label="⌛Total de Ocorrências em 2023:",
        value=f"{TOTALOC2023.iloc[0, 0]:.0f}",
        delta=f"{DIFFOC2322.iloc[0, 0]:.2%}",
    )

    TOTALOC2024 = duckdb.query(
        f"""SELECT SUM({TITULOOCORRENCIA})
        FROM '{PATH_PARQUET}'
        WHERE ano = '2024'
        """
    ).to_df()

    DIFFOC2423 = (TOTALOC2024 / TOTALOC2023) - 1

    col2.metric(
        label="⌛Total de Ocorrências em 2024:",
        value=f"{TOTALOC2024.iloc[0, 0]:.0f}",
        delta=f"{DIFFOC2423.iloc[0, 0]:.2%}",
    )

    TOATALOC2025 = duckdb.query(
        f"""SELECT SUM({TITULOOCORRENCIA})
        FROM '{PATH_PARQUET}'
        WHERE ano = '2025'
        """
    ).to_df()

    DIFFOC2524 = (TOATALOC2025 / TOTALOC2024) - 1

    col1.metric(
        label="⌛Total de Ocorrências em 2025:",
        value=f"{TOATALOC2025.iloc[0, 0]:.0f}",
        delta=f"{DIFFOC2524.iloc[0, 0]:.2%}",
    )

    st.markdown("---")


def PypiColorMetrics():
    st.markdown(
        """
<style>
div[data-testid="stMetricValue"] {
    background: no-repeat center/80% url("./image/4744315.png");

    border: 2px solid rgba(28, 131, 225, 0.1);
    padding: 5% 4% 5% 10%;
    border-radius: 15px;
    color: rgb(60,179,113);
    overflow-wrap: break-word;
}

/* breakline for metric text         */
div[data-testid="stMetricValue"] > label[data-testid="stMetricLabel"] > div {
   overflow-wrap: break-word;
   white-space: break-spaces;
   color: red;
}
</style>
""",
        unsafe_allow_html=True,
    )


def main():
    "Função principal para executar o dashboard."

    aba1, aba2, aba3 = st.tabs(["Geral", "Município", "Região"])

    with aba1:
        resulttitulo, resultocorrencia = PypiInfoGeral()
        PypigraphicGeral(resultocorrencia)
        PypiMetrics(resultocorrencia)
        PypiColorMetrics()

    with aba2:
        ...

    with aba3:
        ...


if __name__ == "__main__":
    PypiConfigPage()
    PypiTitle()
    PypiAttData()
    main()

    # resultano, resulttitulo, resultocorrencia = PypiInfoDash()
    # totalgeral = Pypigraphic(resultano, resultocorrencia)

    # PypiMetrics(resultocorrencia)
    # PypiColorMetrics()
