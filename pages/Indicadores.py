import streamlit as st
import pandas as pd
import yfinance as yf
import investpy as inv
import seaborn as sns
from datetime import date
import plotly.graph_objects as go
import fundamentus as fd
import yfinance as yf
import numpy as np
from plotly.subplots import make_subplots


st.page_link("Dash_Finance.py", label="Início", icon="🏠")

st.title(':green[Indicadores]')

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
            st.write('**Setor:**', info_papel1['Setor'][0])
            st.write('**Subsetor:**', info_papel1['Subsetor'][0])
            st.write('**Cotação:**', f'R${float(info_papel1["Cotacao"][0]):,.2f}')

            st.write('**:green[Performance]**')
            if 'Receita_Liquida_12m' in info_papel1.columns:
                st.write('**Receita Líquida - 12 Meses:**', f'R${float(info_papel1['Receita_Liquida_12m'][0]):,.0f}')
            else:
                st.write('**Receita Líquida - 12 Meses:**', f'R${float(info_papel1['Rec_Servicos_12m'][0]):,.0f}')
            st.write('**Lucro Líquido - 12 Meses:**', f'R${float(info_papel1["Lucro_Liquido_12m"][0]):,.0f}')
            st.write('**ROE:**', f'{info_papel1["ROE"][0]}%')
            st.write('**ROIC:**', f'{info_papel1["ROIC"][0]}%')
            st.write('**Liquidez Corrente**', f'{info_papel1["Liquidez_Corr"][0]}')
            
            st.write('**:green[Valuation]**')
            st.write('**Valor de Mercado:**', f'R$ {float(info_papel1["Valor_de_mercado"][0]):,.0f}')
            st.write('**P/L:**', f' {float(info_papel1["PL"][0])/100:,.2f}')
            st.write('**P/VP:**', f' {float(info_papel1["PVP"][0])/100:,.2f}')
            st.write('**EV/EBITDA:**', f' {info_papel1["EV_EBITDA"][0]}')
            st.write('**Dividend Yield:**', f'{info_papel1["Div_Yield"][0]}')

            st.write('**:green[Balanço Patrimonial]**')
            st.write('**Patrimônio Líquido:**', f'R${float(info_papel1["Patrim_Liq"][0]):,.0f}')
            st.write('**Ativo:**', f'R$ {float(info_papel1["Ativo"][0]):,.0f}')
            if 'Disponibilidades' in info_papel1.columns:
                st.write('**Disponibilidades**', f'R${float(info_papel1['Disponibilidades'][0]):,.0f}')
            else:
                st.write('**Depositos:**', f'R${float(info_papel1['Depositos'][0]):,.0f}')
            if 'Ativo_Circulante' in info_papel1.columns:
                st.write('**Ativo Circulante:**', f'R${float(info_papel1["Ativo_Circulante"][0]):,.0f}')
            else:
                st.write('**Ativo Circulante:**', '')
            if 'Div_Bruta' in info_papel1.columns:
                st.write('**Dívida Bruta:**', f'R${float(info_papel1["Div_Bruta"][0]):,.0f}')
            else:
                st.write('**Dívida Bruta:**', f'R$ {info_papel1["Div_Br_Patrim"][0]:}')
            if 'Div_Liquida' in info_papel1.columns:
                st.write('**Dívida Líquida:**', f'R$ {float(info_papel1["Div_Liquida"][0]):,.0f}')
            else:
                st.write('**Dívida Líquida:**', 'R$')

    ativo1 = f'{papel1}.SA'
    ativo1_hist = yf.download(ativo1, period = '5y', interval = '1d')

    fig1 = go.Figure(data=[go.Candlestick(x=ativo1_hist.index,
                            open=ativo1_hist['Open'],
                            high=ativo1_hist['High'],
                            low=ativo1_hist['Low'],
                            close=ativo1_hist['Close'])])
    fig1.update_layout(title=ativo1, xaxis_rangeslider_visible=False)
    st.plotly_chart(fig1)


if comparar:   
    with st.spinner('Baixando Informações...'):
        with col2:
            with st.expander('**:green[Ativo 2]**', expanded = True):
                papel2 = st.selectbox('**Selecione o Segundo Papel**', lista_tickers)
                info_papel2 = fd.get_detalhes_papel(papel2)
                st.write('**:green[Informações Gerais]**')
                st.write('**Empresa:**', info_papel2['Empresa'][0])
                st.write('**Setor:**', info_papel2['Setor'][0])
                st.write('**Subsetor:**', info_papel2['Subsetor'][0])
                st.write('**Cotação:**', f'R$ {float(info_papel2["Cotacao"][0]):,.2f}')
                st.write('**:green[Performance]**')
                if 'Receita_Liquida_12m' in info_papel2.columns:
                    st.write('**Receita Líquida - 12 Meses:**', f'R${float(info_papel2['Receita_Liquida_12m'][0]):,.0f}')
                else:
                    st.write('**Receita Líquida - 12 Meses:**', f'R${float(info_papel2['Rec_Servicos_12m'][0]):,.0f}')
                st.write('**Lucro Líquido - 12 Meses:**', f'R${float(info_papel1["Lucro_Liquido_12m"][0]):,.0f}')
                st.write('**ROE:**', f'{info_papel2["ROE"][0]}%')
                st.write('**ROIC:**', f'{info_papel2["ROIC"][0]}%')
                st.write('**Liquidez Corrente**', f'{info_papel2["Liquidez_Corr"][0]}')
                
                st.write('**:green[Valuation]**')
                st.write('**Valor de Mercado:**', f'R$ {float(info_papel2["Valor_de_mercado"][0]):,.0f}')
                st.write('**P/L:**', f' {float(info_papel2["PL"][0])/100:,.2f}')
                st.write('**P/VP:**', f' {float(info_papel2["PVP"][0])/100:,.2f}')
                st.write('**EV/EBITDA:**', f' {info_papel2["EV_EBITDA"][0]}')
                st.write('**Dividend Yield:**', f'{info_papel2["Div_Yield"][0]}')

                st.write('**:green[Balanço Patrimonial]**')
                st.write('**Patrimônio Líquido:**', f'R$ {float(info_papel2["Patrim_Liq"][0]):,.0f}')
                st.write('**Ativo:**', f'R$ {float(info_papel2["Ativo"][0]):,.0f}')
                if 'Disponibilidades' in info_papel2.columns:
                    st.write('**Disponibilidades**', f'R$ {float(info_papel2['Disponibilidades'][0]):,.0f}')
                else:
                    st.write('**Depositos:**', f'R$ {float(info_papel2['Depositos'][0]):,.0f}')
                if 'Ativo_Circulante' in info_papel2.columns:
                    st.write('**Ativo Circulante:**', f'R$ {float(info_papel2["Ativo_Circulante"][0]):,.0f}')
                else:
                    st.write('**Ativo Circulante:**', '')
                if 'Div_Bruta' in info_papel2.columns:
                    st.write('**Dívida Bruta:**', f'R$ {float(info_papel2["Div_Bruta"][0]):,.0f}')
                else:
                    st.write('**Dívida Bruta:**', f'R$ {info_papel2["Div_Br_Patrim"][0]:}')
                if 'Div_Liquida' in info_papel2.columns:
                    st.write('**Dívida Líquida:**', f'R$ {float(info_papel2["Div_Liquida"][0]):,.0f}')
                else:
                    st.write('**Dívida Líquida:**', 'R$')
    
        ativo2 = f'{papel2}.SA'
        ativo2_hist = yf.download(ativo2, period = '5y', interval = '1d')

        fig2 = go.Figure(data=[go.Candlestick(x=ativo2_hist.index,
                                open=ativo2_hist['Open'],
                                high=ativo2_hist['High'],
                                low=ativo2_hist['Low'],
                                close=ativo2_hist['Close'])])
        fig2.update_layout(title=ativo2, xaxis_rangeslider_visible=False)
        st.plotly_chart(fig2)    



#Gráficos de Desempenho da empresa

st.subheader(f'Gráficos de Desempenho')
option = st.selectbox(
   "Selecione o período para visualizar os gráficos?",
   ("Anualmente", "Trimestralmente"),
   index=None,
   placeholder="período",
)

if option == "Anualmente":
    frequencia = 'yearly'
else:
    frequencia = 'quarterly'

ativo_sa = f'{papel1}.SA'
ativo = yf.Ticker(ativo_sa)
balance = ativo.get_incomestmt(freq= frequencia)
balanco = pd.DataFrame(balance)
balanco = balanco[balanco.columns[::-1]]

#balanço patrimonial
balanco_pat = ativo.get_balance_sheet(freq= frequencia)
balanco_pat = pd.DataFrame(balanco_pat)
balanco_pat = balanco_pat/1000
balanco_pat = balanco_pat[balanco_pat.columns[::-1]]


#Receita Bruta
revenue = balanco.loc['TotalRevenue']

#EBITDA ou Dívida Líquida
if 'EBITDA' in balanco.columns:
    ebitda = balanco.loc['EBITDA']/revenue
    ebitda_title = 'Margem EBITDA'
else: 
    ebitda = balanco_pat.loc['NetDebt']
    ebitda_title = 'Dívida Líquida'
# Lucro 
net = balanco.loc['NetIncome']

#Margem Líquida
margem = net/revenue



fig = make_subplots (rows= 2, 
                     cols =2,
                     row_heights= [5,5],
                     column_widths=[3,3],
                     subplot_titles= ('Receita Bruta', ebitda_title, 'Lucro Líquido', 'Margem Líquida'),
                     shared_xaxes = False)
fig.add_trace(go.Bar(name = 'Receita Bruta', x = revenue.index, y = revenue), row = 1, col =1)
if 'EBITDA' in balanco.columns:
    fig.add_trace(go.Bar(name = 'Margem EBITDA', x = ebitda.index, y = ebitda), row = 1, col =2)
else:
    fig.add_trace(go.Bar(name = 'Dívida Líquida', x = ebitda.index, y = ebitda), row = 1, col =2)
fig.add_trace(go.Bar(name = 'Lucro Líquido', x = net.index, y = net), row = 2, col =1)
fig.add_trace(go.Bar(name = 'Margem Líquida', x = margem.index, y = margem), row = 2, col =2)
fig.update_layout(title_text = f'Análise de Desempenho da {papel1}',
                  template = 'plotly_dark',
                  showlegend=False,
                  height = 500,
                  width=800)
st.plotly_chart(fig)



if comparar:
    ativo2_sa = f'{papel2}.SA'
    ativo2 = yf.Ticker(ativo2_sa)
    balance2 = ativo2.get_incomestmt(freq= frequencia)
    balanco2 = pd.DataFrame(balance)
    balanco2 = balanco[balanco.columns[::-1]]

    #balanço patrimonial
    balanco_pat2 = ativo.get_balance_sheet(freq= frequencia)
    balanco_pat2 = pd.DataFrame(balanco_pat2)
    balanco_pat2 = balanco_pat2/1000
    balanco_pat2 = balanco_pat2[balanco_pat.columns[::-1]]

    #Receita Bruta
    revenue2 = balanco.loc['TotalRevenue']

    #EBITDA ou Dívida Líquida
    if 'EBITDA' in balanco2.columns:
        ebitda2 = balanco2.loc['EBITDA']/revenue
        ebitda_title2 = 'Margem EBITDA'
    else: 
        ebitda2 = balanco_pat2.loc['NetDebt']
        ebitda_title2 = 'Dívida Líquida'

    # Lucro 
    net2 = balanco.loc['NetIncome']

    #Margem Líquida
    margem2 = net2/revenue2



    fig2 = make_subplots (rows= 2, 
                        cols =2,
                        row_heights= [5,5],
                        column_widths=[3,3],
                        subplot_titles= ('Receita Bruta', ebitda_title2, 'Lucro Líquido', 'Margem Líquida'),
                        shared_xaxes = False)
    fig2.add_trace(go.Bar(name = 'Receita Bruta', x = revenue2.index, y = revenue2), row = 1, col =1)
    if 'EBITDA' in balanco.columns:
        fig.add_trace(go.Bar(name = 'Margem EBITDA', x = ebitda2.index, y = ebitda2), row = 1, col =2)
    else:
        fig.add_trace(go.Bar(name = 'Dívida Líquida', x = ebitda2.index, y = ebitda2), row = 1, col =2)
    fig2.add_trace(go.Bar(name = 'Lucro Líquido', x = net2.index, y = net), row = 2, col =1)
    fig2.add_trace(go.Bar(name = 'Margem Líquida', x = margem2.index, y = margem2), row = 2, col =2)
    fig2.update_layout(title_text = f'Análise de Desempenho da {papel2}',
                    template = 'plotly_dark',
                    showlegend=False,
                    height = 500,
                    width=800)

    st.plotly_chart(fig2)
