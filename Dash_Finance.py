#Importação de Bibliotecas
import streamlit as st
import pandas as pd
import yfinance as yf
import investpy as inv
import seaborn as sns
import matplotlib
from datetime import date
import plotly.graph_objects as go
import fundamentus as fd




st.title('Início')
st.markdown('---')


st.page_link("pages/Indicadores.py", label="Ver Indicadores", icon="📊")

st.page_link("pages/Mercado.py", label="Ir para Mercado", icon="💼")

st.page_link("pages/Valuation_FIIs.py", label="Avaliar um Fundo Imobiliário", icon="💰")



