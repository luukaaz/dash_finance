# URLs das APIs do Banco Central para obtenção de dados econômicos
selic_url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados?formato=json'
ipca_url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json'
dolar_url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=json'
euro_url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.21619/dados?formato=json'
igpm_url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.189/dados?formato=json'
sal_url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.1619/dados?formato=json'
pib_url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.7326/dados?formato=json'

# Importa as bibliotecas necessárias para o projeto
import streamlit as st
import pandas as pd
import yfinance as yf
import investpy as inv
import seaborn as sns
from datetime import date
import plotly.graph_objects as go
import fundamentus as fd
import numpy as np
import plotly.express as px

# Cria um link para direcionar o usuário à página inicial do aplicativo
st.page_link("Dash_Finance.py", label="Início", icon="🏠")

# Define o título da página
st.title(':green[Indicadores Econômicos]')

# Exibe um spinner (indicador de carregamento) enquanto as informações são baixadas
with st.spinner('Baixando Informações...'):
    # Obtém a taxa Selic a partir da URL e processa os dados
    selic_df = pd.read_json(selic_url)
    selic_index = selic_df.set_index('data')
    selic_valor = selic_index['valor']
    selic = selic_valor.iloc[-1]
    
    # Obtém a taxa IPCA a partir da URL e processa os dados
    ipca_df = pd.read_json(ipca_url)
    ipca_index = ipca_df.set_index('data')
    ipca = ipca_index.iloc[-12:]
    ipca_valor = ipca_index['valor']
    ipca_ultimo = sum(ipca['valor'])

    # Obtém a cotação do Dólar a partir da URL e processa os dados
    dolar_df = pd.read_json(dolar_url)
    dolar_index = dolar_df.set_index('data')
    dolar_valor = dolar_index['valor']
    dolar = dolar_index.iloc[-1]
    
    # Obtém a cotação do Euro a partir da URL e processa os dados
    euro_df = pd.read_json(euro_url)
    euro_index = euro_df.set_index('data')
    euro_valor = euro_index['valor']
    euro = euro_index.iloc[-1]
    
    # Obtém a taxa IGPM a partir da URL e processa os dados    
    igpm_df = pd.read_json(igpm_url)
    igpm_index = igpm_df.set_index('data')
    igpm_valor = igpm_index['valor']
    igpm = igpm_index.iloc[-12:]
    igpm_ultimo = sum(igpm['valor'])
    
    # Obtém o valor do PIB a partir da URL e processa os dados
    pib_df = pd.read_json(pib_url)
    pib_index = pib_df.set_index('data')
    pib_valor = pib_index['valor']
    pib = (pib_index.iloc[-1])
    
    # Adiciona uma linha horizontal como separador
    st.markdown('---')

    # Cria três colunas para exibir as métricas econômicas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label=":green[Taxa Selic]", value= f'{selic}%')
        st.metric(label=":green[PIB]", value= f'{float(pib):.2f}%')
    with col2: 
        st.metric(label=":green[IPCA]", value= f'{(ipca_ultimo):.2f}%')
        st.metric(label=":green[IGPM]", value= f'{(igpm_ultimo):.2f}%')
    with col3:
        st.metric(label=":green[Dólar]", value= f'R$ {float(dolar):.2f}')
        st.metric(label=":green[Euro]", value= f'R$ {float(euro):.2f}')

# Adiciona uma linha horizontal como separador
st.markdown('---')

# Cria um menu suspenso para selecionar o indicador a ser analisado
indicador = st.selectbox(
    "Selecione o indicador a ser analisado",
    ("Selic", "IPCA", "Dólar", "IGPM"),
    index=None,
    placeholder="Indicador Econômico",
)

# Seleciona os dados com base no indicador escolhido
if indicador == "Selic":
    df = selic_valor
if indicador == "IPCA":
    df = ipca_valor.iloc[-240:]
if indicador == "Dólar":
    df = dolar_valor.iloc[-240:]
if indicador == "IGPM":
    df = igpm_valor.iloc[-240:]



# Cria e exibe um gráfico de linha do histórico do indicador econômico selecionado
if indicador: 
    fig = px.line(x=df.index, y = df, title= 'HIstórico do Indicador Econômico', height=400)
    st.plotly_chart(fig)

 
