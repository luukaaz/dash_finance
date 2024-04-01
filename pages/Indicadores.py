import streamlit as st
import pandas as pd
import yfinance as yf
import investpy as inv
import seaborn as sns
import matplotlib
from datetime import date
import plotly.graph_objects as go
import fundamentus as fd

st.page_link("Dash_Finance.py", label="Início", icon="🏠")

st.title(':green[Indicadores]')

def indicadores():
    st.markdown(date.today().strftime('%d/%m/%y'))

    st.markdown('---')

    lista_tickers = fd.list_papel_all()

    comparar = st.checkbox('Comparar 2 ativos')

    col1, col2 = st.columns(2)

    with st.spinner('Baixando Informações...'):
        with col1:
            with st.expander('**:green[Ativo 1]**', expanded = True):
                papel1 = st.selectbox('**Selecione o Papel**', lista_tickers)
                info_papel1 = fd.get_detalhes_papel(papel1)
                st.write('**:green[Informações Gerais]**')
                st.write('**Empresa:**', info_papel1['Empresa'][0])
                st.write('**:Setor**', info_papel1['Setor'][0])
                st.write('**Subsetor:**', info_papel1['Subsetor'][0])
                st.write('**Valor de Mercado:**', f'R$ {info_papel1["Valor_de_mercado"][0]:,.2f}')
                st.write('**:green[Performance]**')
                st.write('**Patrimônio Líquido:**', f'R${float(info_papel1["Patrim_Liq"][0]):,.2f}')
                st.write('**Receita Líquida - 12 Meses:**', f'R$ {float(info_papel1["Receita_Liquida_12m"][0]):,.2f}')
                st.write('**Lucro Líquido - 12 Meses:**', f'R$ {float(info_papel1["Lucro_Liquido_12m"][0]):,.2f}')
                st.write('**Dívida Bruta:**', f'R$ {float(info_papel1["Div_Bruta"][0]):,.2f}')
                st.write('**P/L:**', f' {float(info_papel1["PL"][0])/100:,.2f}')
                st.write('**Dividend Yield:**', f'{info_papel1["Div_Yield"][0]}')

    if comparar:   
        with st.spinner('Baixando Informações...'):
            with col2:
                with st.expander('**:green[Ativo 2]**', expanded = True):
                    papel2 = st.selectbox('**Selecione o Segundo Papel**', lista_tickers)
                    info_papel2 = fd.get_detalhes_papel(papel2)
                    st.write('**:green[Informações Gerais]**')
                    st.write('**Empresa:**', info_papel2['Empresa'][0])
                    st.write('**:Setor**', info_papel2['Setor'][0])
                    st.write('**Subsetor:**', info_papel2['Subsetor'][0])
                    st.write('**Valor de Mercado:**', f'R$ {info_papel2["Valor_de_mercado"][0]:,.2f}')
                    st.write('**:green[Performance]**')
                    st.write('**Patrimônio Líquido:**', f'R${float(info_papel2["Patrim_Liq"][0]):,.2f}')
                    st.write('**Receita Líquida - 12 Meses:**', f'R$ {float(info_papel2["Receita_Liquida_12m"][0]):,.2f}')
                    st.write('**Lucro Líquido - 12 Meses:**', f'R$ {float(info_papel2["Lucro_Liquido_12m"][0]):,.2f}')
                    st.write('**Dívida Bruta:**', f'R$ {float(info_papel2["Div_Bruta"][0]):,.2f}')
                    st.write('**P/L:**', f' {float(info_papel2["PL"][0])/100:,.2f}')
                    st.write('**Dividend Yield:**', f'{info_papel2["Div_Yield"][0]}')

indicadores()