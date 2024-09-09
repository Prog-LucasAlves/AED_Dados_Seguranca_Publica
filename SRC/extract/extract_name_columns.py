# Bibliotecas utilizadas
import pandas as pd

# # Dicionário que mapeia códigos de ocorrências para suas descrições completas em português
tipo_ocorrencia = {
    "hom_doloso": "Homicídio Doloso",
    "lesao_corp_morte": "Lesão Corporal Seguida de Morte",
    "latrocinio": "Latrocínio (Roubo Seguido de Morte)",
    "cvli": "Crimes Violentos Letais Intencionais*",
    "hom_por_interv_policial": "Morte por Intervenção de Agente do Estado",
    "letalidade_violenta": "Letalidade Volenta*",
    "tentat_hom": "Tentativa de Homicídio",
    "lesao_corp_dolosa": "Lesão Corporal Dolosa",
    "estupro": "Estupro",
    "hom_culposo": "Homicídio Culposo (Trânsito)*",
    "lesao_corp_culposa": "Lesão corporal culposa (Trânsito)",
    "roubo_transeunte": "Roubo a Transeunte",
    "roubo_celular": "Roubo de Telefone Celular",
    "roubo_em_coletivo": "Roubo em Coletivo",
    "roubo_rua": "Roubo de Rua",
    "roubo_veiculo": "Roubo de Veículo",
    "roubo_carga": "Roubo de Carga",
    "roubo_comercio": "Roubo a Estabelecimento Comercial",
    "roubo_residencia": "Roubo de Residência",
    "roubo_banco": "Roubo a Banco",
    "roubo_cx_eletronico": "Roubo de Caixa Eletrônico",
    "roubo_conducao_saque": "Roubo com Condução da Vítima para Saque em Instituição Financeira",
    "roubo_apos_saque": "Roubo após Saque em Instituição Financeira",
    "roubo_bicicleta": "Roubo de Bicicleta",
    "outros_roubos": "Outros Roubos que Não os Listados Acima",
    "total_roubos": "Total de Roubos",
    "furto_veiculos": "Furto de Veículos",
    "furto_transeunte": "Furto a Transeunte",
    "furto_coletivo": "Furto em Coletivo",
    "furto_celular": "Furto de Telefone Celular",
    "furto_bicicleta": "Furto de Bicicleta",
    "outros_furtos": "Outros Furtos que Não os Listados Acima",
    "total_furtos": "Total de Furtos",
    "sequestro": "Extorsão Mediante Sequestro",
    "extorsao": "Extorsão",
    "sequestro_relampago": "Extorsão com Momentânea Privação da Liberdade",
    "estelionato": "Estelionato",
    "apreensao_drogas": "Apreensão de Drogas",
    "posse_drogas": "Número de Registros que Possuem algum Título Referente a Posse de Drogas",
    "trafico_drogas": "Número de Registros que Possuem algum Título Referente a Tráfico de Drogas",
    "apreensao_drogas_sem_autor": "Número de Registros que Possuem Algum Título Referente a Apreensão de Drogas sem Autor",
    "recuperacao_veiculos": "Recuperação de Veículo",
    "apf": "Auto de Prisão em Flagrante",
    "aaapai": "Auto de Apreensão de Adolescente por Prática de Ato Infracional",
    "cmp": "Cumprimento de Mandado de Prisão",
    "cmba": "Cumprimento de Mandado de Busca e Apreensão",
    "ameaca": "Ameaça",
    "pessoas_desaparecidas": "Pessoas Desaparecidas",
    "encontro_cadaver": "Encontro de Cadáver",
    "encontro_ossada": "Encontro de Ossada",
    "pol_militares_mortos_serv": "Policiais Militares Mortos em Serviço",
}

# Transformando em um dataframe e resetando o index
tipo_ocorrencia = pd.DataFrame.from_dict(tipo_ocorrencia, orient="index").reset_index()

# Renomeando as colunas
tipo_ocorrencia.rename(
    columns={"index": "tipo_ocorrencia", 0: "descricao"}, inplace=True
)

# Salvando em um arquivo csv
tipo_ocorrencia.to_csv("../../data/dict_data/tipo_ocorrencia.csv", sep=";", index=False)
