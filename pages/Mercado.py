import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import date
import plotly.graph_objects as go
import fundamentus as fd

st.page_link("Dash_Finance.py", label="Início", icon="🏠")

st.title(':green[Mercado]')

def mercado():
    st.markdown(date.today().strftime('%d/%m/%y'))
    st.markdown('---')

    st.subheader('Índices de Mercado Mundiais')

    dict_tickers = {
                'Bovespa' : '^BVSP',
                'FTSE 100' : '^FTSE',
                'MERVAL' : '^MERV',
                'Gold' : 'GC=F',
                'S&P500' : '^GSPC',
                'DAX' : '^GDAXI',
                'HANG SENG' : '^HSI',
                'ETHEREUM' : 'ETH-USD',
                'NASDAQ' : '^IXIC',
                'NIKKEI' : '^N225',
                'Volatility' : '^VIX',
                'BITCOIN' : 'BTC-USD',
                }
    df_info = pd.DataFrame({'Ativo' : dict_tickers.keys(), 'Ticker': dict_tickers.values()})
    
    df_info['Ult. Valor'] = ''
    df_info['%'] = ''
    
    count = 0
    with st.spinner('Baixando cotações...'):
        for ticker in dict_tickers.values():
            cotacoes = yf.download(ticker, period ='5d')['Adj Close']
            variacao = ((cotacoes.iloc[-1]/cotacoes.iloc[-2])-1)*100
            df_info['Ult. Valor'][count] = round(cotacoes.iloc[-1], 2)
            df_info['%'][count] = round(variacao, 2)
            count += 1

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(df_info['Ativo'][0], value=df_info['Ult. Valor'][0], delta=str(df_info['%'][0]) + '%')
        st.metric(df_info['Ativo'][1], value=df_info['Ult. Valor'][1], delta=str(df_info['%'][1]) + '%')
        st.metric(df_info['Ativo'][2], value=df_info['Ult. Valor'][2], delta=str(df_info['%'][2]) + '%')
        st.metric(df_info['Ativo'][3], value=df_info['Ult. Valor'][4], delta=str(df_info['%'][3]) + '%')

    with col2:
        st.metric(df_info['Ativo'][4], value=df_info['Ult. Valor'][4], delta=str(df_info['%'][4]) + '%')
        st.metric(df_info['Ativo'][5], value=df_info['Ult. Valor'][5], delta=str(df_info['%'][5]) + '%')
        st.metric(df_info['Ativo'][6], value=df_info['Ult. Valor'][6], delta=str(df_info['%'][6]) + '%')
        st.metric(df_info['Ativo'][7], value=df_info['Ult. Valor'][7], delta=str(df_info['%'][7]) + '%')
    
    with col3:
        st.metric(df_info['Ativo'][8], value=df_info['Ult. Valor'][8], delta=str(df_info['%'][8]) + '%')
        st.metric(df_info['Ativo'][9], value=df_info['Ult. Valor'][9], delta=str(df_info['%'][9]) + '%')
        st.metric(df_info['Ativo'][10], value=df_info['Ult. Valor'][10], delta=str(df_info['%'][10]) + '%')
        st.metric(df_info['Ativo'][11], value=df_info['Ult. Valor'][11], delta=str(df_info['%'][11]) + '%')
    st.markdown('---')

    st.subheader('Histórico do Mercado')

    lista_indices = ['IBOV', 'S&P500', 'NASDAQ', 'BITCOIN']
    lista_periodo = ['5 anos', '1 ano', '1 dia']

    indice = st.selectbox('Selecione o Índice', lista_indices)
    periodo_var = st.selectbox('Selecione o período', lista_periodo)
    if periodo_var == '1 ano':
        periodo_var = '1y'
        intervalo = '1d'
    if periodo_var == '5 anos':
        periodo_var = '5y'
        intervalo = '1d'
    if periodo_var == '1 dia':
        periodo_var = '1d'
        intervalo = '5m'

    if indice == 'IBOV':
        indice_diario = yf.download('^BVSP', period = periodo_var, interval = intervalo)
    if indice == 'S&P500':
        indice_diario = yf.download('^GSPC', period = periodo_var, interval = intervalo)
    if indice == 'NASDAQ':
        indice_diario = yf.download('^IXIC', period = periodo_var, interval = intervalo)
    if indice == 'BITCOIN':
        indice_diario = yf.download('BTC-USD', period = periodo_var, interval = intervalo)

    fig = go.Figure(data=[go.Candlestick(x=indice_diario.index,
                        open=indice_diario['Open'],
                        high=indice_diario['High'],
                        low=indice_diario['Low'],
                        close=indice_diario['Close'])])
    fig.update_layout(title=indice, xaxis_rangeslider_visible=False)

    st.plotly_chart(fig)

mercado()
