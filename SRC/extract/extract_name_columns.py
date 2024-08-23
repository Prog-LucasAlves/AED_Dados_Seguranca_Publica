# Bibliotecas utilizadas
import pandas as pd

# Criando dicionário com a colunas
tipo_ocorrencia = {"hom_doloso": "Homicídio doloso"}

# Transformando em um dataframe e resetando o index
tipo_ocorrencia = pd.DataFrame.from_dict(tipo_ocorrencia, orient="index").reset_index()

# Renomeando as colunas
tipo_ocorrencia.rename(
    columns={"index": "tipo_ocorrencia", 0: "descricao"}, inplace=True
)

# Salvando em um arquivo csv
tipo_ocorrencia.to_csv("../../data/dict_data/tipo_ocorrencia.csv", sep=";", index=False)
