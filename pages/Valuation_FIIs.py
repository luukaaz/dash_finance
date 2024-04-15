ipca_url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json'

import streamlit as st
import pandas as pd
import plotly
import plotly.express as px
import yfinance as yf
import matplotlib 
from matplotlib import style
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import numpy_financial as npf

st.page_link("Dash_Finance.py", label="Início", icon="🏠")

st.title(':green[Valuation FIIs]')

st.markdown('---')

with st.spinner('Carregando informações...'):
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

    #Spread mais recente do IPCA 2045
    ultimo_ipca2045 = ipca2045['Taxa Compra Manha'][-1]
    #Taxa IPCA
    ipca_df = pd.read_json(ipca_url)
    ipca_index = ipca_df.set_index('data')
    ipca = ipca_index.iloc[-12:]
    ipca_ultimo = sum(ipca['valor'])


    #Nome do Fundo
    nome_fundo = st.text_input('Qual é o nome do fundo?')
    tipo_fii = st.selectbox(
        "Selecione o tipo do fundo a ser avaliado",
        ("FII's Tijolo sem Crescimento", "FII's Tijolo com Crescimento", "FII's Papel"),
        index=None,
        placeholder="Tipo do Fundo Imobiliário",
    )

    st.markdown('---')

    div_estimativa = st.checkbox('Colocar manualmente o provento do fundo')
    st.caption(f'O modo automático utiliza o último provento pago pelo fundo, estimar manualmente pode fazer sentido se o último provento pago for um valor não recorrente.')
    papel_maiusculo = nome_fundo.upper()
    ativo = f'{papel_maiusculo}.SA'

    #Provento
    if nome_fundo:
        if div_estimativa:
            dividendos = st.number_input("Digite o valor do provento a ser utilizado como base:")
            provento_anual = dividendos*12
            papel_fii = yf.Ticker(ativo)
            dados = papel_fii.history(period = '5y', interval = '1d')
        else:
            papel_fii = yf.Ticker(ativo)
            dados = papel_fii.history(period = '5y', interval = '1d')
            df_filtrado = dados[dados['Dividends'] > 0]
            df_filtrado = df_filtrado.iloc[-12:]
            dividendos = df_filtrado['Dividends']
            provento_anual = dividendos*12

            papel_fii = yf.Ticker(ativo)
            dados = papel_fii.history(period = '5y', interval = '1d')
            dados = dados[dados['Dividends'] > 0]
            dados_filtrados = dados.iloc[-12:]
            df = dados_filtrados['Dividends']
            
            fig = px.bar(x=df.index, y=df, template = 'plotly_dark', height = 400, width = 800)
            st.plotly_chart(fig)
        
        #Prêmio de Risco
        # O Prêmio de Risco é considerado geralmente de 1.5% a 3.5% de acordo com o risco do fundo.
        premio_risco = st.number_input("Qual é o prêmio de risco do fundo imobiliário?", placeholder="prêmio de risco...")
        premio_risco_float = float(premio_risco)
        st.write('O Prêmio de Risco geralmente é considerado entre 1.5% a 3.5%, de acordo com o risco do fundo.')
        
        st.markdown('---')
        
        #Taxa de Desconto
        taxa_de_desconto = (premio_risco_float + ultimo_ipca2045)/100
        
        
        #Valor de Mercado
        market_value = dados['Close'].iloc[-1]
        
        
        #Valor da Cota
        if tipo_fii ==  "FII's Papel":
            tx_desconto = (ultimo_ipca2045 + ipca_ultimo + premio_risco_float)
            valor_cota = (provento_anual/tx_desconto)*100
        
        elif tipo_fii ==  "FIIs Tijolo com Crescimento":
            g = 1.05
            valor_cota = npf.npv(taxa_de_desconto, [dividendos*g, dividendos*(g**2), dividendos*(g**3), dividendos*(g**4), dividendos*(g**5), (dividendos*(g**5)/taxa_de_desconto)]).round(2)
        
        else:
            valor_cota = provento_anual/taxa_de_desconto
            var_dados = ((market_value/valor_cota) -1)*100
        
        var_dados = ((market_value/valor_cota) -1)*100

        valor_cota = valor_cota.iloc[-1]
        var_dados = var_dados.iloc[-1]
        
        st.write(f'O valor estimado da cota do :blue[{papel_maiusculo}] é :green[R${valor_cota:,.2f}]')
        # crie deixar o resultado de var_dados aparecer em porcentagem
        st.write(f'O valor de mercado do fundo :blue[{papel_maiusculo}] é R${market_value:,.2f}, ou seja, uma diferença de {(var_dados):.2f}% em relação ao valor estimado.' )
        
        
        fig1 = go.Figure(data=[go.Candlestick(x=dados.index,
                            open=dados['Open'],
                            high=dados['High'],
                            low=dados['Low'],
                            close=dados['Close'])])
        fig1.update_layout(title=f'Valor da cota do {papel_maiusculo} dos últimos 5 anos', xaxis_rangeslider_visible=False)
        st.plotly_chart(fig1)
