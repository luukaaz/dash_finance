#Importação de Bibliotecas
import streamlit as st
import pandas as pd
import yfinance as yf
import investpy as inv
import seaborn as sns
from datetime import date
import plotly.graph_objects as go
import fundamentus as fd
import numpy as np
from bcb import sgs

with st.spinner('Baixando Informações...'):
    #Taxa Selic
    df_selic = sgs.get({'SELIC': 432})
    selic = df_selic['SELIC'].iloc[-1]
    
    #Taxa IPCA
    df_ipca = sgs.get({'IPCA': 433})
    ipca = df_ipca.iloc[-12:]
    ipca_ultimo = sum(ipca['IPCA'])
    
    #Dólar
    df_dolar = sgs.get({'DOLAR': 1})
    dolar = df_dolar['DOLAR'].iloc[-1]
    
    #Euro
    df_euro = sgs.get({'EURO': 21619})
    euro = df_euro['EURO'].iloc[-1]
    
    #IGPM
    df_igpm = sgs.get({'IGPM': 189})
    igpm = df_igpm.iloc[-12:]
    igpm_ultimo = round(sum(igpm['IGPM']), 2)
    
    #Salário Mínimo
    df_salario = sgs.get({'Salário Mínimo': 21619})
    salario = df_salario['Salário Mínimo'].iloc[-1]
    
    #PIB
    df_pib = sgs.get({'PIB': 7326})
    pib = df_pib['PIB'].iloc[-1]
    
    st.title('Início')
    
    st.markdown('---')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label=":green[Taxa Selic]", value= f'{selic}%')
        st.metric(label=":green[PIB]", value= f'{pib}%')
    
        
    with col2: 
        st.metric(label=":green[IPCA]", value= f'{ipca_ultimo}%')
        st.metric(label=":green[IGPM]", value= f'{igpm_ultimo}%')
    with col3:
        st.metric(label=":green[Dólar]", value= f'R$ {(dolar):.2f}')
        st.metric(label=":green[Euro]", value= f'R$ {(euro):.2f}')
    
    
       
    
    st.markdown('---')
    
    st.page_link("pages/Indicadores.py", label="Ver Indicadores", icon="📊")
    
    st.page_link("pages/Mercado.py", label="Ir para Mercados", icon="💰")
    
    st.page_link("pages/Valuation_FIIs.py", label="Avaliar um Fundo Imobiliário", icon="🏢")

