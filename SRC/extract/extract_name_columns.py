# Bibliotecas utilizadas
import pandas as pd

# Criando dicionário com a colunas
tipo_ocorrencia = {
    "hom_doloso": "Homicídio doloso",
    "lesao_corp_morte": "Lesão corporal seguida de morte",
    "latrocinio": "Latrocínio (roubo seguido de morte)",
    "cvli": "Crimes Violentos Letais Intencionais*",
    "hom_por_interv_policial": "Morte por intervenção de agente do Estado",
    "letalidade_violenta": "Letalidade violenta*",
}

# Transformando em um dataframe e resetando o index
tipo_ocorrencia = pd.DataFrame.from_dict(tipo_ocorrencia, orient="index").reset_index()

# Renomeando as colunas
tipo_ocorrencia.rename(
    columns={"index": "tipo_ocorrencia", 0: "descricao"}, inplace=True
)

# Salvando em um arquivo csv
tipo_ocorrencia.to_csv("../../data/dict_data/tipo_ocorrencia.csv", sep=";", index=False)
