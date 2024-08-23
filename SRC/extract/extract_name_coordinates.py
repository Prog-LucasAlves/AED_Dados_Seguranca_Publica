# Bibliotecas utilizadas
import json
import pandas as pd


def extractnamecoordinates():
    """
    Função para extrair os nomes dos municípios e suas coordenadas.
    """
    # Caminho do arquivo com as coordenadas dos municípios
    file_map = "../../data/map/geojs-33-mun.json"

    # Carregando os dados
    data = json.load(open(file_map, encoding="utf-8"))

    # Listas aonde seram armazendos os dados
    name = []
    coordinates = []

    # Percorrendo todo arquivo json e coletando os dados
    for i in range(len(data["features"])):
        name.append(data["features"][i]["properties"]["name"])
        coordinates.append(data["features"][i]["geometry"]["coordinates"][0][0])

    # Organizando os dados coletados
    map = {"fmun": name, "coordinates": coordinates}

    # Convertendo em um dataframe do pandas
    map_df = pd.DataFrame(map)

    # Salvando em um arquivo csv
    map_df.to_csv("../../data/map/name_coordinates.csv", sep=";", index=False)


def extractcolumcoordinates():
    """
    Função para extrair as coordenadas dos municípios.

    """
    # Caminho do arquivo csv com as coordenadas dos municípios
    file_map = "../../data/map/name_coordinates.csv"

    # Carregando os dados do arquivo csv
    mapa = pd.read_csv(file_map, sep=";")

    # Separando as colunas de latitude e longitude
    maplatlon = mapa["coordinates"].str.split(n=1, expand=True)

    # Criando as colunas do dataframe
    maplatlon.columns = ["lat", "lon"]

    # Concatenando os dados
    mapa = pd.concat([mapa, maplatlon], axis=1)

    # Removendo coluna
    mapa.drop("coordinates", axis=1, inplace=True)

    # Renomeando as colunas do dataframe
    mapa.rename(columns={"lat": "latitude", "lon": "longitude"}, inplace=True)

    # Removendo caracteres
    mapa["latitude"] = mapa["latitude"].str.replace("[", "")
    mapa["latitude"] = mapa["latitude"].str.replace(",", "")
    mapa["longitude"] = mapa["longitude"].str.replace("]", "")

    # Salvando em um arquivo csv
    mapa.to_csv("../../data/map/name_coordinates.csv", sep=";", index=False)


if __name__ == "__main__":
    extractnamecoordinates()
    extractcolumcoordinates()
