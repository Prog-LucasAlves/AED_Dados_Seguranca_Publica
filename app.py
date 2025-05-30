"""
Dashboard Dados Segurança Pública do RJ
"""

# Bibliotecas utilizadas
import streamlit as st
from PIL import Image
import duckdb
import altair as alt
import pandas as pd

# Diretório dos Dados
# Caminho do arquivo parquet com os dados
PATH_PARQUET = "./data/raw_data/GOLDEN/GOLDEN_data.parquet"

# Caminho do arquivo com as descrições das variáveis
PATH_DESCRIPTIONS = "./data/dict_data/tipo_ocorrencia.csv"

# Caminho do arquivo com os nomes dos municipios
PATH_MUNICIPIOS = "./data/dict_data/municipio.csv"

# Caminho do arquivo com os nomes das regiões
PATH_REGIOES = "./data/dict_data/regiao.csv"


def PypiConfigPage():
    """
    Função para configurar a página.
    """
    img = Image.open("./image/4744315.png")

    st.set_page_config(
        page_title="Dados da Segurança Pública do Estado do RJ",
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
<p style="color:DimGrey; font-size: 18px; font-weight: bolder;"
> Atualização: {DATAATTMES} | {DATAATTANO} </p>
"""
    st.markdown(ATT, unsafe_allow_html=True)

    return DATAATTMES


def PypiInfoGeral():
    """
    Função para criar os selectbox de | Ocorrência.
    """
    # CSS para reduzir o tamanho do selectbox
    st.markdown(
        """
        <style>
        div[data-baseweb="select"] {
            max-width: 600px;
            font-size: 17px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # CSS para o titulo do selectbox
    st.markdown(
        """
        <style>
        div[data-testid="stSelectbox"] label p {
            font-size: 17px !important;
            font-weight: bold !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Colunas do Selectbox
    (col1,) = st.columns([0.4])

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
    Função para criar os gráficos(Barras | Heatmap).
    """

    # CSS espaçamento entre os gráficos
    st.markdown(
        """
        <style>
        div[data-testid="stVerticalBlock"] {
        padding-right: 60px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    TITULOOCORRENCIA = tituloocorrencia

    # Colunas dos graficos
    (col1, col2, col3) = st.columns([1, 1, 1])

    # Grafico de barras | Total de ocorrências por ano
    TOTALANODF = duckdb.query(
        f"""SELECT ano AS Ano, SUM({TITULOOCORRENCIA}) AS Total
        FROM '{PATH_PARQUET}'
        GROUP BY ano
        ORDER BY ano"""
    ).to_df()

    TOTALANODF["Total_fmt"] = TOTALANODF["Total"].apply(
        lambda x: f"{x:,.0f}".replace(",", ".")
    )
    MEDIAMESDF = TOTALANODF["Total"].mean()
    x_scale = alt.Scale(domain=[0, TOTALANODF["Total"].max() * 1.1])

    chart = (
        alt.Chart(TOTALANODF)
        .mark_bar(color="#3CB371")
        .encode(
            x=alt.X(
                "Total:Q",
                axis=alt.Axis(
                    title="Total de Ocorrências",
                    format=",.0f",
                    labelExpr="replace(datum.label, ',', '.')",
                    labelFontSize=14,
                    titleFontSize=18,
                ),
            ),
            y=alt.Y(
                "Ano:O",
                sort=None,
                axis=alt.Axis(
                    labelFontSize=14,
                    titleFontSize=18,
                ),
            ),
        )
        + alt.Chart(TOTALANODF)
        .mark_text(
            align="center",
            baseline="middle",
            dx=-25,
            color="black",
            fontSize=14,
        )
        .encode(
            x="Total:Q",
            y=alt.Y("Ano:O", sort=None),
            text=alt.Text("Total_fmt:N"),
        )
        + alt.Chart(pd.DataFrame({"media": [MEDIAMESDF]}))
        .mark_rule(
            color="#d62728",
            strokeWidth=2,
            strokeDash=[5, 5],
        )
        .encode(x=alt.X("media:Q", scale=x_scale, title=""))
        + alt.Chart(pd.DataFrame({"media": [MEDIAMESDF]}))
        .mark_text(
            text=f"Média de Ocorrências: {MEDIAMESDF:,.0f}".replace(",", "."),
            color="#d62728",
            fontSize=14,
            dx=0,
            dy=-10,
        )
        .encode(
            x=alt.X("media:Q", scale=x_scale, title=""),
            y=alt.value(0),
        )
    ).properties(height=400, width=800)

    col1.altair_chart(chart, use_container_width=True, key="chart1")

    # Grafico de heatmap | Total de ocorrências por mes e ano

    TOTALMESANODF = duckdb.query(
        f"""SELECT mes, ano, SUM({TITULOOCORRENCIA}) AS Total
        FROM '{PATH_PARQUET}'
        GROUP BY mes, ano
        ORDER BY ano, mes"""
    ).to_df()

    TOTALMESANODF["Total_fmt"] = TOTALMESANODF["Total"].apply(
        lambda x: f"{x:,.0f}".replace(",", ".")
    )
    TOTALMESANODF["Total_bin"] = pd.cut(
        TOTALMESANODF["Total"],
        bins=[0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000],
        labels=[
            "0 - 1.000",
            "1.001 - 2.000",
            "2.001 - 3.000",
            "3.001 - 4.000",
            "4.001 - 5.000",
            "5.001 - 6.000",
            "6.001 - 7.000",
            "7.001 - 8.000",
            "8.001 - 9.000",
            "9.001 - 10.000",
        ],
    )

    chart = (
        alt.Chart(TOTALMESANODF)
        .mark_rect()
        .encode(
            x=alt.X(
                "mes:O",
                title="Mês",
                axis=alt.Axis(
                    labelAngle=0,
                    labelFontSize=14,
                    titleFontSize=18,
                ),
            ),
            y=alt.Y(
                "ano:O",
                title="Ano",
                axis=alt.Axis(
                    labelFontSize=14,
                    titleFontSize=18,
                ),
            ),
            color=alt.Color(
                "Total_bin:N",
                scale=alt.Scale(scheme="greens"),
                title="Total de Ocorrências",
                legend=alt.Legend(
                    labelFontSize=14,
                    titleFontSize=18,
                    orient="right",
                    titleOrient="top",
                    titlePadding=10,
                    labelPadding=5,
                ),
            ),
            tooltip=[
                alt.Tooltip("ano:O", title="Ano"),
                alt.Tooltip("mes:O", title="Mês"),
                alt.Tooltip("Total:N", title="Total"),
            ],
        )
        .properties(height=400, width=800)
    )

    col2.altair_chart(chart, use_container_width=True, key="chart2")

    # Grafico de linha  | Total de ocorrências por mes e ano

    chart = (
        alt.Chart(TOTALMESANODF)
        .mark_line(point=True)
        .encode(
            x=alt.X(
                "mes:O",
                title="Mês",
                axis=alt.Axis(
                    labelAngle=0,
                    labelFontSize=14,
                    titleFontSize=18,
                ),
            ),
            y=alt.Y(
                "Total:Q",
                title="Total de Ocorrências",
                axis=alt.Axis(
                    format=",.0f",
                    labelExpr="replace(datum.label, ',', '.')",
                    formatType="number",
                    labelFontSize=14,
                    titleFontSize=18,
                ),
            ),
            color=alt.Color("ano:O", title="Ano", scale=alt.Scale(scheme="greens")),
            tooltip=["ano", "mes", "Total"],
        )
        .properties(height=400, width=800)
    )

    col3.altair_chart(chart, use_container_width=True, key="chart3")

    st.divider()


def PypiMetricsGeral(titulo, tituloocorrencia):
    """
    Função para criar as métricas do dashboard.
    """

    TITULO = titulo
    TITULOOCORRENCIA = tituloocorrencia

    T = f"""
    <p style="
    font-size: 20px;
    font-weight: bolder;"
> 📋​Comparativo Anual de Ocorrências |
        <span style="color:#d62728">{TITULO.upper()}</span> | : 2025 | 2024 | 2023 | 2022 | 2021 </p>
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
        value=f"{TOTALOC2021.iloc[0, 0]:,.0f}".replace(",", "."),
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
        value=f"{TOTALOC2022.iloc[0, 0]:,.0f}".replace(",", "."),
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
        value=f"{TOTALOC2023.iloc[0, 0]:,.0f}".replace(",", "."),
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
        value=f"{TOTALOC2024.iloc[0, 0]:,.0f}".replace(",", "."),
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
        value=f"{TOATALOC2025.iloc[0, 0]:,.0f}".replace(",", "."),
        delta=f"{DIFFOC2524.iloc[0, 0]:.2%}",
    )

    st.markdown("---")


def PypiInfoMunicipio():
    """
    Função para criar os selectbox de | Município e Ocorrencias.
    """

    # CSS para reduzir o tamanho do selectbox
    st.markdown(
        """
        <style>
        div[data-baseweb="select"] {
            max-width: 600px;
            font-size: 17px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # CSS para o titulo do selectbox
    st.markdown(
        """
        <style>
        div[data-testid="stSelectbox"] label p {
            font-size: 17px !important;
            font-weight: bold !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Colunas do Selectbox
    (col1, col2) = st.columns([1, 1])

    # Selectbox Título Ocorrência
    TITULODFM = duckdb.query(
        f"""SELECT descricao
        FROM '{PATH_DESCRIPTIONS}'
        ORDER BY descricao"""
    ).to_df()
    TITULOM = col1.selectbox(
        "​📝​Título da Ocorrência:", TITULODFM["descricao"], key="T2"
    )

    # Título das ocorrências
    TITULOOCORRENCIADF = duckdb.query(
        f"""SELECT tipo_ocorrencia
        FROM '{PATH_DESCRIPTIONS}'
        WHERE descricao = '{TITULOM}'"""
    ).to_df()

    TITULOOCORRENCIA = TITULOOCORRENCIADF.iloc[0, 0]

    # Selectbox Município
    MUNICIPIODFM = duckdb.query(
        f"""SELECT DISTINCT descricao
        FROM '{PATH_MUNICIPIOS}'
        ORDER BY descricao"""
    ).to_df()

    MUNICIPIOM = col2.selectbox("​🗺️​Município:", MUNICIPIODFM["descricao"], key="T3")

    # Titulo do município
    MUNICIPIOOCORRENCIADF = duckdb.query(
        f"""SELECT DISTINCT tipo_ocorrencia
        FROM '{PATH_MUNICIPIOS}'
        WHERE descricao = '{MUNICIPIOM}'"""
    ).to_df()

    TITULOMUNICIPIO = MUNICIPIOOCORRENCIADF.iloc[0, 0]

    # Observação sobre o título da ocorrência
    if TITULOM == "Crimes Violentos Letais Intencionais*":
        CVLI = """
<p style="color:DimGrey; font-size: 14px; font-weight: bolder;"
> *Crimes Violentos Letais Intencionais: Homicídio doloso + Lesão corporal seguida de morte + Latrocínio. </p>
"""
        st.markdown(CVLI, unsafe_allow_html=True)

    elif TITULOM == "Letalidade Violenta*":
        LV = """
<p style="color:DimGrey; font-size: 14px; font-weight: bolder;"
> *Homicídio doloso + Lesão corporal seguida de morte + Latrocínio + Morte por intervenção de agente do Estado. </p>
"""
        st.markdown(LV, unsafe_allow_html=True)

    elif TITULOM == "Homicídio Culposo (Trânsito)*":
        LV = """
<p style="color:DimGrey; font-size: 14px; font-weight: bolder;"
> *Atropelamento + colisão + outros. </p>
"""
        st.markdown(LV, unsafe_allow_html=True)

    return TITULOOCORRENCIA, TITULOMUNICIPIO, TITULOM


def PypigraphicMunicipio(titulo, municipio):
    """
    Função para criar os gráficos(Barras | Heatmap) para o município.
    """

    # CSS espaçamento entre os gráficos
    st.markdown(
        """
        <style>
        div[data-testid="stVerticalBlock"] {
        padding-right: 60px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    TITULO = titulo
    MUNICIPIO = municipio

    # Colunas dos graficos
    (col1, col2, col3) = st.columns([1, 1, 1])

    # Grafico de barras | Total de ocorrências por ano e município
    TOTALANOMUNICIPIODF = duckdb.query(
        f"""SELECT ano AS Ano, SUM({TITULO}) AS Total
        FROM '{PATH_PARQUET}'
        WHERE fmun = '{MUNICIPIO}'
        GROUP BY ano"""
    ).to_df()

    TOTALANOMUNICIPIODF["Total_fmt"] = TOTALANOMUNICIPIODF["Total"].apply(
        lambda x: f"{x:,.0f}".replace(",", ".")
    )

    MEDIAMUNICIPIODF = TOTALANOMUNICIPIODF["Total"].mean()
    x_scale = alt.Scale(domain=[0, TOTALANOMUNICIPIODF["Total"].max() * 1.1])

    chart = (
        alt.Chart(TOTALANOMUNICIPIODF)
        .mark_bar(color="#3CB371")
        .encode(
            x=alt.X(
                "Total:Q",
                axis=alt.Axis(
                    title="Total de Ocorrências",
                    format=",.0f",
                    labelExpr="replace(datum.label, ',', '.')",
                    labelFontSize=14,
                    titleFontSize=18,
                ),
            ),
            y=alt.Y(
                "Ano:O",
                sort=None,
                axis=alt.Axis(
                    labelFontSize=14,
                    titleFontSize=18,
                ),
            ),
        )
        + alt.Chart(TOTALANOMUNICIPIODF)
        .mark_text(
            align="right",
            baseline="middle",
            dx=0,
            color="black",
            fontSize=14,
        )
        .encode(
            x="Total:Q",
            y=alt.Y("Ano:O", sort=None),
            text=alt.Text("Total_fmt:N"),
        )
        + alt.Chart(pd.DataFrame({"media": [MEDIAMUNICIPIODF]}))
        .mark_rule(
            color="#d62728",
            strokeWidth=2,
            strokeDash=[5, 5],
        )
        .encode(x=alt.X("media:Q", scale=x_scale, title=""))
        + alt.Chart(pd.DataFrame({"media": [MEDIAMUNICIPIODF]}))
        .mark_text(
            text=f"Média de Ocorrências: {MEDIAMUNICIPIODF:,.0f}".replace(",", "."),
            color="#d62728",
            fontSize=14,
            dx=0,
            dy=-10,
        )
        .encode(
            x=alt.X("media:Q", scale=x_scale, title=""),
            y=alt.value(0),
        )
    ).properties(height=400, width=800)

    col1.altair_chart(chart, use_container_width=True, key="chart4")

    # Grafico de heatmap | Total de ocorrências por mes e ano
    TOTALANOMESMUNICIPIODF = duckdb.query(
        f"""SELECT mes, ano, SUM({TITULO}) AS Total
        FROM '{PATH_PARQUET}'
        WHERE fmun = '{MUNICIPIO}'
        GROUP BY mes, ano
        ORDER BY ano, mes"""
    ).to_df()

    TOTALANOMESMUNICIPIODF["Total_fmt"] = TOTALANOMESMUNICIPIODF["Total"].apply(
        lambda x: f"{x:,.0f}".replace(",", ".")
    )
    MAXTOTAL = TOTALANOMESMUNICIPIODF["Total"].max()
    BINS = list(range(0, int(MAXTOTAL + 1000), 50))
    LABELS = [f"{i+1} - {i+50}" if i > 0 else "0 - 50" for i in BINS[:-1]]

    TOTALANOMESMUNICIPIODF["Total_bin"] = pd.cut(
        TOTALANOMESMUNICIPIODF["Total"], bins=BINS, labels=LABELS, include_lowest=True
    )

    TOTALANOMESMUNICIPIODF["Total_bin"] = TOTALANOMESMUNICIPIODF[
        "Total_bin"
    ].cat.add_categories("Fora do intervalo")
    TOTALANOMESMUNICIPIODF["Total_bin"] = TOTALANOMESMUNICIPIODF["Total_bin"].fillna(
        "Fora do intervalo"
    )

    chart = (
        alt.Chart(TOTALANOMESMUNICIPIODF)
        .mark_rect()
        .encode(
            x=alt.X(
                "mes:O",
                title="Mês",
                axis=alt.Axis(
                    labelAngle=0,
                    labelFontSize=14,
                    titleFontSize=18,
                ),
            ),
            y=alt.Y(
                "ano:O",
                title="Ano",
                axis=alt.Axis(
                    labelFontSize=14,
                    titleFontSize=18,
                ),
            ),
            color=alt.Color(
                "Total_bin:N",
                scale=alt.Scale(scheme="greens"),
                sort=LABELS + ["Fora do intervalo"],
                title="Total de Ocorrências",
                legend=alt.Legend(
                    labelFontSize=14,
                    titleFontSize=18,
                    orient="right",
                    titleOrient="top",
                    titlePadding=10,
                    labelPadding=5,
                ),
            ),
            tooltip=[
                alt.Tooltip("ano:O", title="Ano"),
                alt.Tooltip("mes:O", title="Mês"),
                alt.Tooltip("Total:N", title="Total"),
            ],
        )
        .properties(height=400, width=800)
    )

    col2.altair_chart(chart, use_container_width=True, key="chart5")

    chart = (
        alt.Chart(TOTALANOMESMUNICIPIODF)
        .mark_boxplot(color="seagreen")
        .encode(
            x=alt.X(
                "mes:O",
                title="Mês",
                axis=alt.Axis(labelAngle=0, labelFontSize=14, titleFontSize=18),
            ),
            y=alt.Y(
                "Total:Q",
                title="Total de Ocorrências",
                axis=alt.Axis(
                    labelFontSize=14,
                    titleFontSize=18,
                ),
            ),
            tooltip=["ano", "mes", "Total"],
        )
    ).properties(width=800, height=400)

    col3.altair_chart(chart, use_container_width=True, key="chart6")


def PypiMetricsMunicipio(titulo, municipio, titulo2):
    """
    Função para criar as métricas do dashboard.
    """

    TITULO = titulo
    MUNICIPIO = municipio
    TITULO2 = titulo2

    T = f"""
    <p style="
    font-size: 20px;
    font-weight: bolder;"
> 📋​Comparativo Anual de Ocorrências |
        <span style="color:#d62728">{TITULO2.upper()}</span> | : 2025 | 2024 | 2023 | 2022 | 2021 </p>
    """
    st.markdown(T, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns((1, 1, 1, 1, 1))

    TOTALOC2020 = duckdb.query(
        f"""SELECT SUM({TITULO})
        FROM '{PATH_PARQUET}'
        WHERE ano = '2020' AND fmun = '{MUNICIPIO}'
        """
    ).to_df()

    TOTALOC2021 = duckdb.query(
        f"""SELECT SUM({TITULO})
        FROM '{PATH_PARQUET}'
        WHERE ano = '2021' AND fmun = '{MUNICIPIO}'
        """
    ).to_df()

    DIFFOC2021 = (TOTALOC2021 / TOTALOC2020) - 1

    col5.metric(
        label="⌛Total de Ocorrências em 2021:",
        value=f"{TOTALOC2021.iloc[0, 0]:,.0f}".replace(",", "."),
        delta=f"{DIFFOC2021.iloc[0, 0]:.2%}",
    )

    TOTALOC2022 = duckdb.query(
        f"""SELECT SUM({TITULO})
        FROM '{PATH_PARQUET}'
        WHERE ano = '2022' AND fmun = '{MUNICIPIO}'
        """
    ).to_df()

    DIFFOC2122 = (TOTALOC2022 / TOTALOC2021) - 1

    col4.metric(
        label="⌛Total de Ocorrências em 2022:",
        value=f"{TOTALOC2022.iloc[0, 0]:,.0f}".replace(",", "."),
        delta=f"{DIFFOC2122.iloc[0, 0]:.2%}",
    )

    TOTALOC2023 = duckdb.query(
        f"""SELECT SUM({TITULO})
        FROM '{PATH_PARQUET}'
        WHERE ano = '2023' AND fmun = '{MUNICIPIO}'
        """
    ).to_df()

    DIFFOC2322 = (TOTALOC2023 / TOTALOC2022) - 1

    col3.metric(
        label="⌛Total de Ocorrências em 2023:",
        value=f"{TOTALOC2023.iloc[0, 0]:,.0f}".replace(",", "."),
        delta=f"{DIFFOC2322.iloc[0, 0]:.2%}",
    )

    TOTALOC2024 = duckdb.query(
        f"""SELECT SUM({TITULO})
        FROM '{PATH_PARQUET}'
        WHERE ano = '2024' AND fmun = '{MUNICIPIO}'
        """
    ).to_df()

    DIFFOC2423 = (TOTALOC2024 / TOTALOC2023) - 1

    col2.metric(
        label="⌛Total de Ocorrências em 2024:",
        value=f"{TOTALOC2024.iloc[0, 0]:,.0f}".replace(",", "."),
        delta=f"{DIFFOC2423.iloc[0, 0]:.2%}",
    )

    TOATALOC2025 = duckdb.query(
        f"""SELECT SUM({TITULO})
        FROM '{PATH_PARQUET}'
        WHERE ano = '2025' AND fmun = '{MUNICIPIO}'
        """
    ).to_df()

    DIFFOC2524 = (TOATALOC2025 / TOTALOC2024) - 1

    col1.metric(
        label="⌛Total de Ocorrências em 2025:",
        value=f"{TOATALOC2025.iloc[0, 0]:,.0f}".replace(",", "."),
        delta=f"{DIFFOC2524.iloc[0, 0]:.2%}",
    )

    st.markdown("---")


def PypiInfoRegiao():
    """
    Função para criar os selectbox de | Região e Ocorrencias.
    """

    # CSS para reduzir o tamanho do selectbox
    st.markdown(
        """
        <style>
        div[data-baseweb="select"] {
            max-width: 600px;
            font-size: 17px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # CSS para o titulo do selectbox
    st.markdown(
        """
        <style>
        div[data-testid="stSelectbox"] label p {
            font-size: 17px !important;
            font-weight: bold !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Colunas do Selectbox
    (col1, col2) = st.columns([1, 1])

    # Selectbox Título Ocorrência
    TITULODFM = duckdb.query(
        f"""SELECT descricao
        FROM '{PATH_DESCRIPTIONS}'
        ORDER BY descricao"""
    ).to_df()
    TITULOM = col1.selectbox(
        "​📝​Título da Ocorrência:", TITULODFM["descricao"], key="T4"
    )

    # Título das ocorrências
    TITULOOCORRENCIADF = duckdb.query(
        f"""SELECT tipo_ocorrencia
        FROM '{PATH_DESCRIPTIONS}'
        WHERE descricao = '{TITULOM}'"""
    ).to_df()

    TITULOOCORRENCIA = TITULOOCORRENCIADF.iloc[0, 0]

    # Selectbox regiao
    REGIAODFM = duckdb.query(
        f"""SELECT DISTINCT descricao
        FROM '{PATH_REGIOES}'
        ORDER BY descricao"""
    ).to_df()

    REGIAOM = col2.selectbox("​🗺️​Região:", REGIAODFM, key="T5")

    # Titulo do município
    REGIAOOCORRENCIADF = duckdb.query(
        f"""SELECT DISTINCT tipo_ocorrencia
        FROM '{PATH_REGIOES}'
        WHERE descricao = '{REGIAOM}'"""
    ).to_df()

    TITULOREGIAO = REGIAOOCORRENCIADF.iloc[0, 0]

    # Observação sobre o título da ocorrência
    if TITULOM == "Crimes Violentos Letais Intencionais*":
        CVLI = """
<p style="color:DimGrey; font-size: 14px; font-weight: bolder;"
> *Crimes Violentos Letais Intencionais: Homicídio doloso + Lesão corporal seguida de morte + Latrocínio. </p>
"""
        st.markdown(CVLI, unsafe_allow_html=True)

    elif TITULOM == "Letalidade Violenta*":
        LV = """
<p style="color:DimGrey; font-size: 14px; font-weight: bolder;"
> *Homicídio doloso + Lesão corporal seguida de morte + Latrocínio + Morte por intervenção de agente do Estado. </p>
"""
        st.markdown(LV, unsafe_allow_html=True)

    elif TITULOM == "Homicídio Culposo (Trânsito)*":
        LV = """
<p style="color:DimGrey; font-size: 14px; font-weight: bolder;"
> *Atropelamento + colisão + outros. </p>
"""
        st.markdown(LV, unsafe_allow_html=True)

    return TITULOOCORRENCIA, TITULOREGIAO, TITULOM


def PypigraphicRegiao(titulo, regiao):
    """
    Função para criar os gráficos(Barras | Heatmap) para a Regiaão.
    """

    # CSS espaçamento entre os gráficos
    st.markdown(
        """
        <style>
        div[data-testid="stVerticalBlock"] {
        padding-right: 60px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    TITULO = titulo
    REGIAO = regiao

    # Colunas dos graficos
    (col1, col2, col3) = st.columns([1, 1, 1])

    # Grafico de barras | Total de ocorrências por ano e município
    TOTALANOMUNICIPIODF = duckdb.query(
        f"""SELECT ano AS Ano, SUM({TITULO}) AS Total
        FROM '{PATH_PARQUET}'
        WHERE regiao = '{REGIAO}'
        GROUP BY ano"""
    ).to_df()

    TOTALANOMUNICIPIODF["Total_fmt"] = TOTALANOMUNICIPIODF["Total"].apply(
        lambda x: f"{x:,.0f}".replace(",", ".")
    )

    MEDIAMUNICIPIODF = TOTALANOMUNICIPIODF["Total"].mean()
    x_scale = alt.Scale(domain=[0, TOTALANOMUNICIPIODF["Total"].max() * 1.1])

    chart = (
        alt.Chart(TOTALANOMUNICIPIODF)
        .mark_bar(color="#3CB371")
        .encode(
            x=alt.X(
                "Total:Q",
                axis=alt.Axis(
                    title="Total de Ocorrências",
                    format=",.0f",
                    labelExpr="replace(datum.label, ',', '.')",
                    labelFontSize=14,
                    titleFontSize=18,
                ),
            ),
            y=alt.Y(
                "Ano:O",
                sort=None,
                axis=alt.Axis(
                    labelFontSize=14,
                    titleFontSize=18,
                ),
            ),
        )
        + alt.Chart(TOTALANOMUNICIPIODF)
        .mark_text(
            align="right",
            baseline="middle",
            dx=0,
            color="black",
            fontSize=14,
        )
        .encode(
            x="Total:Q",
            y=alt.Y("Ano:O", sort=None),
            text=alt.Text("Total_fmt:N"),
        )
        + alt.Chart(pd.DataFrame({"media": [MEDIAMUNICIPIODF]}))
        .mark_rule(
            color="#d62728",
            strokeWidth=2,
            strokeDash=[5, 5],
        )
        .encode(x=alt.X("media:Q", scale=x_scale, title=""))
        + alt.Chart(pd.DataFrame({"media": [MEDIAMUNICIPIODF]}))
        .mark_text(
            text=f"Média de Ocorrências: {MEDIAMUNICIPIODF:,.0f}".replace(",", "."),
            color="#d62728",
            fontSize=14,
            dx=0,
            dy=-10,
        )
        .encode(
            x=alt.X("media:Q", scale=x_scale, title=""),
            y=alt.value(0),
        )
    ).properties(height=400, width=800)

    col1.altair_chart(chart, use_container_width=True, key="chart4")


def PypiMetricsRegiao(titulo, municipio, titulo2):
    """
    Função para criar as métricas do dashboard.
    """

    TITULO = titulo
    REGIAO = municipio
    TITULO2 = titulo2

    T = f"""
    <p style="
    font-size: 20px;
    font-weight: bolder;"
> 📋​Comparativo Anual de Ocorrências |
        <span style="color:#d62728">{TITULO2.upper()}</span> | : 2025 | 2024 | 2023 | 2022 | 2021 </p>
    """
    st.markdown(T, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns((1, 1, 1, 1, 1))

    TOTALOC2020 = duckdb.query(
        f"""SELECT SUM({TITULO})
        FROM '{PATH_PARQUET}'
        WHERE ano = '2020' AND regiao = '{REGIAO}'
        """
    ).to_df()

    TOTALOC2021 = duckdb.query(
        f"""SELECT SUM({TITULO})
        FROM '{PATH_PARQUET}'
        WHERE ano = '2021' AND regiao = '{REGIAO}'
        """
    ).to_df()

    DIFFOC2021 = (TOTALOC2021 / TOTALOC2020) - 1

    col5.metric(
        label="⌛Total de Ocorrências em 2021:",
        value=f"{TOTALOC2021.iloc[0, 0]:,.0f}".replace(",", "."),
        delta=f"{DIFFOC2021.iloc[0, 0]:.2%}",
    )

    TOTALOC2022 = duckdb.query(
        f"""SELECT SUM({TITULO})
        FROM '{PATH_PARQUET}'
        WHERE ano = '2022' AND regiao = '{REGIAO}'
        """
    ).to_df()

    DIFFOC2122 = (TOTALOC2022 / TOTALOC2021) - 1

    col4.metric(
        label="⌛Total de Ocorrências em 2022:",
        value=f"{TOTALOC2022.iloc[0, 0]:,.0f}".replace(",", "."),
        delta=f"{DIFFOC2122.iloc[0, 0]:.2%}",
    )

    TOTALOC2023 = duckdb.query(
        f"""SELECT SUM({TITULO})
        FROM '{PATH_PARQUET}'
        WHERE ano = '2023' AND regiao = '{REGIAO}'
        """
    ).to_df()

    DIFFOC2322 = (TOTALOC2023 / TOTALOC2022) - 1

    col3.metric(
        label="⌛Total de Ocorrências em 2023:",
        value=f"{TOTALOC2023.iloc[0, 0]:,.0f}".replace(",", "."),
        delta=f"{DIFFOC2322.iloc[0, 0]:.2%}",
    )

    TOTALOC2024 = duckdb.query(
        f"""SELECT SUM({TITULO})
        FROM '{PATH_PARQUET}'
        WHERE ano = '2024' AND regiao = '{REGIAO}'
        """
    ).to_df()

    DIFFOC2423 = (TOTALOC2024 / TOTALOC2023) - 1

    col2.metric(
        label="⌛Total de Ocorrências em 2024:",
        value=f"{TOTALOC2024.iloc[0, 0]:,.0f}".replace(",", "."),
        delta=f"{DIFFOC2423.iloc[0, 0]:.2%}",
    )

    TOATALOC2025 = duckdb.query(
        f"""SELECT SUM({TITULO})
        FROM '{PATH_PARQUET}'
        WHERE ano = '2025' AND regiao = '{REGIAO}'
        """
    ).to_df()

    DIFFOC2524 = (TOATALOC2025 / TOTALOC2024) - 1

    col1.metric(
        label="⌛Total de Ocorrências em 2025:",
        value=f"{TOATALOC2025.iloc[0, 0]:,.0f}".replace(",", "."),
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
    border-radius: 30px;
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
    """
    Função principal para executar o dashboard.
    """
    # CSS Alter tamanho da fonte
    st.markdown(
        """
        <style>
        /* Estilizar o texto das tabs */
        div[data-testid="stTabs"] button p {
            font-size: 16px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    aba1, aba2, aba3 = st.tabs(["Geral", "Município", "Região"])

    with aba1:
        resulttitulo, resultocorrencia = PypiInfoGeral()
        PypigraphicGeral(resultocorrencia)
        PypiMetricsGeral(resulttitulo, resultocorrencia)
        PypiColorMetrics()

    with aba2:
        resulttitulo, resultocorrencia, resulttitulo2 = PypiInfoMunicipio()
        PypigraphicMunicipio(resulttitulo, resultocorrencia)
        PypiMetricsMunicipio(resulttitulo, resultocorrencia, resulttitulo2)

    with aba3:
        resulttitulo, resultocorrencia, resulttitulo2 = PypiInfoRegiao()
        PypigraphicRegiao(resulttitulo, resultocorrencia)
        PypiMetricsRegiao(resulttitulo, resultocorrencia, resulttitulo2)


if __name__ == "__main__":
    PypiConfigPage()
    PypiTitle()
    PypiAttData()
    main()
