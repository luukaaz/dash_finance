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



#Nome do Fundo
nome_fundo = st.text_input('Qual é o nome do fundo?')
tipo_fii = st.selectbox(
    "Selecione o tipo do fundo a ser avaliado",
    ("FII's Tijolo sem Crescimento", "FII's Tijolo com Crescimento", "FII's Papel"),
    index=None,
    placeholder="Tipo do Fundo Imobiliário",
)

selecao_manual = st.checkbox("Você pretende fazer o input automaticamente? Se sim, selecione esta caixa de seleção")
st.caption(f'No modo automático pode ocorrer alguns erros devido à conexão com APIs públicas')

st.markdown('---')
if selecao_manual:
    if nome_fundo:
        
        #Busca informações de títulos do Tesouro Direto em uma API do governo.
        with st.spinner('Carregando informações...'):
            def busca_titulos_tesouro_direto():
        
            #Busca informações de títulos do Tesouro Direto em uma API do governo.
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


            papel_maiusculo = nome_fundo.upper()
            ativo = f'{papel_maiusculo}.SA'

            div_estimativa = st.checkbox('Colocar manualmente o provento do fundo')
            st.caption(f'O modo automático utiliza o último provento pago pelo fundo, estimar manualmente pode fazer sentido se o último provento pago for um valor não recorrente. Cheque no gráfico de proventos abaixo se o valor é recorrente.')

            
            papel_fii = yf.Ticker(ativo)
            dados = papel_fii.history(period = '5y', interval = '1d')
            dados_filtrados = dados[dados['Dividends'] > 0]
            dados_filtrados = dados_filtrados.iloc[-12:]
            dados_filtrados = dados_filtrados['Dividends']
            
            fig = px.bar(x=dados_filtrados.index, y=dados_filtrados.values, template = 'plotly_dark', height = 400, width = 800, title = f'Evolução de Proventos do {papel_maiusculo}')
            st.plotly_chart(fig)

            if nome_fundo:
                if div_estimativa:
                    dividendos = st.number_input("Digite o valor do provento a ser utilizado como base:")
                    provento_anual = dividendos*12

                else:
                    dividendos = dados_filtrados.tail(1)
                    provento_anual = dividendos*12
            
        
    #Prêmio de Risco
    # O Prêmio de Risco é considerado geralmente de 1.5% a 3.5% de acordo com o risco do fundo.
    premio_risco = st.number_input("Qual é o prêmio de risco do fundo imobiliário?", placeholder="prêmio de risco...")
    premio_risco_float = float(premio_risco)
    st.write('O Prêmio de Risco geralmente é considerado entre 1.5% a 3.5%, de acordo com o risco do fundo.')
    
    st.markdown('---')
    
    #Taxa de Desconto
    taxa_de_desconto = (premio_risco_float + ultimo_ipca2045)/100
    
    
    #Valor de Mercado
    market_value = dados.loc[:, 'Close'].iloc[-1]
    
    
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
    
    var_dados = float(((market_value/valor_cota) -1)*100)

    valor_cota = float(valor_cota.iloc[-1])
    
    st.write(f'O valor estimado da cota do :blue[{papel_maiusculo}] é :green[R${valor_cota:,.2f}]')
    # crie deixar o resultado de var_dados aparecer em porcentagem
    st.write(f'O valor de mercado do fundo :blue[{papel_maiusculo}] é :green[R${market_value:,.2f}], ou seja, uma diferença de :violet[{(var_dados):.2f}%] em relação ao valor estimado.' )
    
    
    fig1 = go.Figure(data=[go.Candlestick(x=dados.index,
                        open=dados['Open'],
                        high=dados['High'],
                        low=dados['Low'],
                        close=dados['Close'])])
    fig1.update_layout(title=f'Valor da cota do {papel_maiusculo} dos últimos 5 anos', xaxis_rangeslider_visible=False)
    st.plotly_chart(fig1)


else:
    papel_maiusculo = nome_fundo.upper()
    ativo = f'{papel_maiusculo}.SA'
    
    dividendos = st.number_input("Digite o valor do provento a ser utilizado como base:")
    provento_anual = dividendos*12
    
    # Prêmio de Risco
    # O Prêmio de Risco é considerado geralmente de 1.5% a 3.5% de acordo com o risco do fundo.
    premio_risco = st.number_input("Qual é o prêmio de risco do fundo imobiliário?", placeholder="prêmio de risco...")
    premio_risco_float = float(premio_risco)
    st.write('O Prêmio de Risco geralmente é considerado entre 1.5% a 3.5%, de acordo com o risco do fundo.')
    
    st.markdown('---')    
    
    #Valor de Mercado
    papel_fii = yf.Ticker(ativo)
    dados = papel_fii.history(period = '5y', interval = '1d')
    market_value = dados.loc[:, 'Close'].iloc[-1]
    
    ultimo_ipca2045 = st.number_input("Informe o valor da taxa do título do tesouro IPCA+45:")
    
    #Taxa de Desconto
    taxa_de_desconto = (premio_risco_float + ultimo_ipca2045)/100
    
    #Valor da Cota
    if tipo_fii ==  "FII's Papel":
        ipca_ultimo = st.number_input("Informe o valor do IPCA acumulado dos últimos 12 meses:")
        tx_desconto = (ultimo_ipca2045 + ipca_ultimo + premio_risco_float)
        valor_cota = (provento_anual/tx_desconto)*100
    
    elif tipo_fii ==  "FIIs Tijolo com Crescimento":
        g = 1.05
        valor_cota = npf.npv(taxa_de_desconto, [dividendos*g, dividendos*(g**2), dividendos*(g**3), dividendos*(g**4), dividendos*(g**5), (dividendos*(g**5)/taxa_de_desconto)]).round(2)
    
    else:
        valor_cota = provento_anual/taxa_de_desconto
        var_dados = ((market_value/valor_cota) -1)*100
    
    var_dados = float(((market_value/valor_cota) -1)*100)
    
    valor_cota = float(valor_cota)
    
    st.write(f'O valor estimado da cota do :blue[{papel_maiusculo}] é :green[R${valor_cota:,.2f}]')
    # crie deixar o resultado de var_dados aparecer em porcentagem
    st.write(f'O valor de mercado do fundo :blue[{papel_maiusculo}] é :green[R${market_value:,.2f}], ou seja, uma diferença de :violet[{(var_dados):.2f}%] em relação ao valor estimado.' )
    
    
