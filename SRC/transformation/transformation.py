# Importando as bibliotecas necessárias
import pandas as pd


def carregardados():
    # Local onde estão os dados
    path = "../../data/raw_data/SILVER/"

    # Lendo os dados salvos
    dados = pd.read_parquet(f"{path}SILVER_data.parquet")
    return dados


def transformardados():
    # Carregando os dados e removendo valores nulos
    dados = carregardados()
    dados.dropna(inplace=True)

    # Criando uma coluna com o nome do mês
    dados["mes_nome"] = ""
    dados.loc[dados["mes"] == 1, "mes_nome"] = "Janeiro"
    dados.loc[dados["mes"] == 2, "mes_nome"] = "Fevereiro"
    dados.loc[dados["mes"] == 3, "mes_nome"] = "Março"
    dados.loc[dados["mes"] == 4, "mes_nome"] = "Abril"
    dados.loc[dados["mes"] == 5, "mes_nome"] = "Maio"
    dados.loc[dados["mes"] == 6, "mes_nome"] = "Junho"
    dados.loc[dados["mes"] == 7, "mes_nome"] = "Julho"
    dados.loc[dados["mes"] == 8, "mes_nome"] = "Agosto"
    dados.loc[dados["mes"] == 9, "mes_nome"] = "Setembro"
    dados.loc[dados["mes"] == 10, "mes_nome"] = "Outubro"
    dados.loc[dados["mes"] == 11, "mes_nome"] = "Novembro"
    dados.loc[dados["mes"] == 12, "mes_nome"] = "Dezembro"

    # Carregando os dados com os nomes e coordenadas dos municípios brasileiros
    name_coordinates = pd.read_csv("../../data/map/name_coordinates.csv", sep=';')

    # Concatenando os dados das coordenadas
    dados = dados.merge(name_coordinates, how="left")

    # Local onde serão salvos os dados transformados
    path = "../../data/raw_data/GOLDEN/"

    # Salvando os dados transformados
    dados.to_parquet(f"{path}GOLDEN_data.parquet", index=False)


if __name__ == "__main__":
    transformardados()
