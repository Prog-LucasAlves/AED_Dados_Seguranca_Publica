## Análise de dados da Segurança Pública do Estado do Rio de Janeiro

## ![A](https://cdn-icons-png.flaticon.com/24/1085/1085456.png) ISP (Instituto de Segurança Pública)

- *O Instituto de Segurança Pública (ISP), criado pela Lei nº 3.329, de 28 de Dezembro 1999, é uma autarquia vinculada diretamente à Secretaria de Estado da Casa Civil. Com mais de 20 anos de existência, o ISP conta com grande conhecimento acumulado no desenvolvimento de metodologias de análise de dados relativos à Segurança Pública. Sua missão é produzir informações e disseminar pesquisas e análises com vistas a influenciar e subsidiar a implementação de políticas públicas de segurança e assegurar a participação social na construção dessas políticas.*

## ![B](https://cdn-icons-png.flaticon.com/24/1534/1534999.png) Objetivo

O objetivo desse projeto é **analisar** os dados de segurança pública do estado do Rio de Janeiro através de um *dashboard*, utilizando o **Streamlit**.

## ![C](https://cdn-icons-png.flaticon.com/24/4739/4739384.png) Funcionalidades | Dashboard

1. Filtro das ocorrências registradas por ano e por tipo de ocorrência.
   * (Gráfico de barras com o total de ocorrências por mês).
   * (Mapa de calor com o total de ocorrências por município)
2. Filtro das ocorrências registradas por **município** | Barra lateral.
3. Filtro das ocorrências registradas por **região** | Barra lateral.

![D](https://github.com/Prog-LucasAlves/AED_Dados_Seguranca_Publica/blob/main/image/Preview.png)

## ![E](https://cdn-icons-png.flaticon.com/24/9872/9872417.png) Dados

- Dados extraidos nesse *[link](https://www.ispdados.rj.gov.br/Arquivos/BaseMunicipioMensal.csv).*

- Dados já baixados estão nesta pasta(arquivo .parquet) *[data](https://github.com/Prog-LucasAlves/AED_Dados_Seguranca_Publica/tree/main/data/raw_data/GOLDEN).*

- Dicionário dos dados estão nesta pasta *[data](https://github.com/Prog-LucasAlves/AED_Dados_Seguranca_Publica/tree/main/data/dict_data).*

## ![F](https://cdn-icons-png.flaticon.com/24/752/752646.png) Tecnologias utilizadas

- Python: Linguagem de programação principal.
- Poetry: Gerenciador de dependências e ambientes virtuais para o Python.
- Pandas: Manipulação e análise de dados.
- Streamlit: Framework desenvolvido em Python que torna possível a visualização de dados para uma simples análise exploratória de um dataset.

> [!NOTE]
> Render: Plataforma para realizar o Deploy(Dashboard). [Link](https://render.com/).

## ![G](https://cdn-icons-png.flaticon.com/24/1991/1991103.png) Dashboard

- [link](https://aed-dados-seguranca-publica.onrender.com)

## ![H](https://cdn-icons-png.flaticon.com/24/3786/3786109.png) Instalação e Execução

1. Criando o diretório para o projeto.

```bash
mkdir AED_Dados_Seguranca_Publica_RJ
cd AED_Dados_Seguranca_Publica_RJ
```

[![GitHub Actions Extract](https://github.com/Prog-LucasAlves/AED_Dados_Seguranca_Publica/actions/workflows/extract.yml/badge.svg?branch=main)](https://github.com/Prog-LucasAlves/AED_Dados_Seguranca_Publica/actions/workflows/extract.yml)
