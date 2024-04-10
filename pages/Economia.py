selic_url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados?formato=json'
ipca_url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json'
dolar_url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=json'
euro_url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.21619/dados?formato=json'
igpm_url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.189/dados?formato=json'
sal_url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.1619/dados?formato=json'
pib_url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.7326/dados?formato=json'

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


st.page_link("Dash_Finance.py", label="Início", icon="🏠")

st.title(':green[Indicadores Econômicos]')

with st.spinner('Baixando Informações...'):
    #Taxa Selic
    selic_df = pd.read_json(selic_url)
    selic_index = selic_df.set_index('data')
    selic_valor = selic_index['valor']
    selic = selic_valor.iloc[-1]
    
    #Taxa IPCA
    ipca_df = pd.read_json(ipca_url)
    ipca_index = ipca_df.set_index('data')
    ipca = ipca_index.iloc[-12:]
    ipca_valor = ipca_index['valor']
    ipca_ultimo = sum(ipca['valor'])

    #Dólar
    dolar_df = pd.read_json(dolar_url)
    dolar_index = dolar_df.set_index('data')
    dolar_valor = dolar_index['valor']
    dolar = dolar_index.iloc[-1]
    
    #Euro
    euro_df = pd.read_json(euro_url)
    euro_index = euro_df.set_index('data')
    euro_valor = euro_index['valor']
    euro = euro_index.iloc[-1]
    
    #IGPM
    igpm_df = pd.read_json(igpm_url)
    igpm_index = igpm_df.set_index('data')
    igpm_valor = igpm_index['valor']
    igpm = igpm_index.iloc[-12:]
    igpm_ultimo = sum(igpm['valor'])
    
    #PIB
    pib_df = pd.read_json(pib_url)
    pib_index = pib_df.set_index('data')
    pib_valor = pib_index['valor']
    pib = (pib_index.iloc[-1])
    
    
    st.markdown('---')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label=":green[Taxa Selic]", value= f'{selic}%')
        st.metric(label=":green[PIB]", value= f'{float(pib):.2f}%')
    with col2: 
        st.metric(label=":green[IPCA]", value= f'{ipca_ultimo}%')
        st.metric(label=":green[IGPM]", value= f'{igpm_ultimo}%')
    with col3:
        st.metric(label=":green[Dólar]", value= f'R$ {float(dolar):.2f}')
        st.metric(label=":green[Euro]", value= f'R$ {float(euro):.2f}')


st.markdown('---')


indicador = st.selectbox(
    "Selecione o indicador a ser analisado",
    ("Selic", "IPCA", "Dólar", "IGPM"),
    index=None,
    placeholder="Indicador Econômico",
)

if indicador == "Selic":
    df = selic_valor
if indicador == "IPCA":
    df = ipca_valor.iloc[-240:]
if indicador == "Dólar":
    df = dolar_valor.iloc[-240:]
if indicador == "IGPM":
    df = igpm_valor.iloc[-240:]




if indicador: 
    fig = px.line(x=df.index, y = df, title= 'HIstórico do Indicador Econômico', height=400)
    st.plotly_chart(fig)

 