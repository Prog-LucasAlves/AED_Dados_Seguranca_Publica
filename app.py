# Bibliotecas utilizadas
import streamlit as st
from PIL import Image
import duckdb

# Configurações da página
st.set_option("deprecation.showfileUploaderEncoding", False)
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


# Leitura dos dados
def loaddata():
    con = duckdb.connect()
    data = con.execute(
        "SELECT * FROM read_parquet('./data/raw_data/GOLDEN/GOLDEN_data.parquet')"
    ).df()
    con.close()
    return data


# Visualização dos dados
def showdata():
    st.title("Dados da Segurança Pública do Estado do Rio de Janeiro")
    # Carregando os dados
    data = loaddata()
    # Mostrando os dados
    st.dataframe(data)


if __name__ == "__main__":
    showdata()
