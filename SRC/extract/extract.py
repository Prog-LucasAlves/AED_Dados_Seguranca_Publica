# Importando as bibliotecas necessárias
import pandas as pd


# Função para extrair e salvar os dados
def extractandload():
    # Local aonde será salvo os dados coletados
    path = "../../data/raw_data/SILVER/"
    # URL dos dados que serão coletados
    csv = "http://www.ispdados.rj.gov.br/Arquivos/BaseMunicipioMensal.csv"
    # Lendo os dados e salvando em um arquivo parquet
    rawDados = pd.read_csv(csv, encoding="ISO-8859-1", engine="python", sep=";")
    rawDados.to_parquet(f"{path}SILVER_data.parquet", index=False)


if __name__ == "__main__":
    extractandload()
