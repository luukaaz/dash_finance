import streamlit as st
import pandas as pd
import plotly
import plotly.express as px
import yfinance as yf
import matplotlib 
from matplotlib import style
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import ssl

st.page_link("Dash_Finance.py", label="Início", icon="🏠")

st.title(':green[Valuation FIIs]')

def Valuation_FIIs():
    pd.set_option("display.max_colwidth", 150)
    pd.set_option("display.min_rows", 20)

    plt.style.use('dark_background')
    plt.rcParams['figure.figsize'] = (18,8)

    ssl._create_default_https_context = ssl._create_unverified_context

    def busca_titulos_tesouro_direto():
        url = 'https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/PrecoTaxaTesouroDireto.csv'
        df  = pd.read_csv(url, sep=';', decimal=',')
        df['Data Vencimento'] = pd.to_datetime(df['Data Vencimento'], dayfirst=True)
        df['Data Base']       = pd.to_datetime(df['Data Base'], dayfirst=True)
        multi_indice = pd.MultiIndex.from_frame(df.iloc[:, :3])
        df = df.set_index(multi_indice).iloc[: , 3:]  
        return df

    titulos = busca_titulos_tesouro_direto()
    titulos.sort_index(inplace=True)

    ipca2045 = titulos.loc[('Tesouro IPCA+', '2045-05-15')]

    #Taxa mais recente do IPCA 2045
    ultimo_ipca2045 = ipca2045['Taxa Compra Manha'][-1]

    #Nome do Fundo
    nome_fundo = st.text_input('Qual é o nome do fundo?')


    #Prêmio de Risco
    # O Prêmio de Risco é considerado geralmente de 1.5% a 3.5% de acordo com o risco do fundo.
    premio_risco = st.number_input("Qual é o prêmio de risco do fundo imobiliário?", placeholder="prêmio de risco...")
    premio_risco_float = float(premio_risco)
    st.write('O Prêmio de Risco é considerado geralmente de 1.5% a 3.5% de acordo com o risco do fundo.')

    #Taxa de Desconto
    taxa_de_desconto = (premio_risco_float + ultimo_ipca2045)/100

    #Provento
    provento = st.number_input("Qual é o valor do provento mensal?", placeholder="provento...")
    provento_float = float(provento)
    provento_anual = provento_float*12

    #Valor da Cota
    with st.spinner('Calculando...'):
        valor_cota = provento_anual/taxa_de_desconto
        st.write(f'O valor estimado da cota do {nome_fundo} é: R${valor_cota:,.2f}')
Valuation_FIIs()
